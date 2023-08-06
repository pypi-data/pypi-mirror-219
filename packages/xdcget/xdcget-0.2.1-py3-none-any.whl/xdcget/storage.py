"""
release caching and exporting of release files
"""
import os
import copy
import shutil
import toml
from contextlib import contextmanager
from dataclasses import dataclass
from zipfile import ZipFile, ZIP_DEFLATED

import requests


def do_request(url, auth=None, exc=True):
    r = requests.get(url, auth=auth)
    if exc and not r.ok:
        r.raise_for_status()
    return r


class NoReleases(Exception):
    def __init__(self, url):
        self.url = url


def get_latest_remote_release(xdcsource):
    r = do_request(xdcsource.latest_release_api_url, auth=xdcsource.auth, exc=False)
    if r.status_code == 404:
        raise NoReleases(xdcsource.latest_release_api_url)
    elif not r.ok:
        r.raise_for_status()

    json = r.json()
    tag_name = json["tag_name"]
    # we could look at lots of metadata in this json
    # but we just try grab the xdc file
    for asset in json["assets"]:
        name = asset["name"]
        if name.endswith(".xdc"):
            url = asset["browser_download_url"]
            date = asset["created_at"]
            return RemoteRelease(name, tag_name, url, date=date)


@dataclass
class RemoteRelease:
    name: str
    tag_name: str
    url: str
    date: str

    def download(self):
        r = do_request(self.url)
        r.raise_for_status()
        return r


def perform_update(config, out):
    for api_def in config.api_defs:
        s = api_def.get_current_rate_limit(requests)
        if s:
            out(s)

    retrieved = changed = num_all_problems = 0
    config.cache_dir.mkdir(exist_ok=True, parents=True)

    with app_index_writer(config=config) as app_index:
        for xdc_source in config.iter_xdc_sources():
            try:
                remote_release = get_latest_remote_release(xdc_source)
            except NoReleases as e:
                out.red(f"NO RELEASES: {e.url}\n")
                num_all_problems += 1
                continue

            old_index_release = app_index.get_release(xdc_source.app_id)
            index_release = app_index.set_release_from_remote(
                xdc_source.app_id, remote_release
            )
            if old_index_release != index_release:
                changed += 1

            cache_path = config.cache_dir.joinpath(index_release.cache_relname)
            rel = index_release
            if True:
                s = f"got release: [{rel.app_id}] "
                s += " ".join([remote_release.name, rel.tag_name, rel.date])
                out(s)
                out(f"        url: {rel.url}")
            if cache_path.exists():
                out(f"     cached: {cache_path}")
            else:
                r = remote_release.download()
                cache_path.write_bytes(r.content)
                retrieved += 1
                out(f"     stored: {cache_path}", green=True)
            for problem in check_xdc_consistency(cache_path, xdc_source):
                out.red(problem)
                num_all_problems += 1
            out("")

        out.green(
            f"{app_index.get_num_apps()} apps checked from {config.app_index_path}"
        )
        out.green(f"{changed} apps had newer versions")
        out.green(f"{retrieved} '.xdc' release files retrieved")
        if num_all_problems > 0:
            out.red(f"{num_all_problems} problems found")
        else:
            out.green("all good, no problems detected in .xdc files")


def check_xdc_consistency(xdc_path, xdc_source):
    MAX_SUMMARY_CHARS = 30
    MIN_DETAILS_CHARS = 40

    zf = ZipFile(xdc_path)
    icon_found = False
    for fname in zf.namelist():
        if fname.lower().endswith("manifest.toml"):
            content = zf.read(fname)
            manifest = toml.loads(content.decode("utf-8"))
            manifest_sc = manifest.get("source_code_url")
            if manifest_sc:
                sc = xdc_source.source_def.source_code_url
                if sc != manifest_sc:
                    yield f"warn: manifest {manifest_sc} != {sc}"
            description = xdc_source.description
            if not description:
                yield "error: 'description' field not in sources.ini"
            else:
                lines = description.strip().split("\n")
                if len(lines[0]) > MAX_SUMMARY_CHARS:
                    extra = len(lines[0]) - MAX_SUMMARY_CHARS
                    yield f"error: description summary {extra} chars too much"
                if lines[0][-1:] == ".":
                    yield "error: description summary ends with '.'"
                if len(lines) < 2:
                    yield "error: description misses detail lines"
                else:
                    joint = " ".join(lines[1:])
                    if len(joint) < MIN_DETAILS_CHARS:
                        yield "error: description details have less than 40 chars"

            if "app_id" in manifest:
                yield f"error: manifest has app_id {manifest['app_id']}, ignoring"
            if "version" in manifest:
                yield "error: manifest has 'version', ignoring"
        elif fname.lower() in ("icon.png", "icon.jpg"):
            icon_found = True

    if not icon_found:
        yield "error: no 'icon.png' or 'icon.jpg' in .xdc file"


def perform_status(config, out):
    app_index = get_app_index(config)

    num_releases = num_cached = 0
    for index_release in app_index.iter_releases():
        ver = index_release.version
        tag = index_release.tag_name
        date = index_release.date
        out(f"[{index_release.app_id}] version={ver} tag={tag} date={date}")
        out(f"url={index_release.url}")
        cache_path = config.cache_dir.joinpath(index_release.cache_relname)
        if cache_path.exists():
            num_cached += 1
            out(f"cached at: {cache_path}")
        else:
            out(f"not cached: {cache_path}", red=True)
        out("")
        num_releases += 1

    if num_releases == 0:
        out.red("app_index is empty: initial 'update' is needed")
        raise SystemExit(1)

    out.green(f"{num_releases} apps found in index at {config.app_index_path}")
    out.green(f"{num_cached} apps are cached in {config.cache_dir}")


class IndexRelease:
    def __init__(
        self,
        app_id,
        version,
        tag_name,
        url,
        date,
        description,
        source_code_url="",
    ):
        self.app_id = app_id
        self.version = version
        self.tag_name = tag_name
        self.url = url
        self.date = date
        self.cache_relname = f"{app_id}-{tag_name}.xdc"
        self.description = description
        self.source_code_url = source_code_url

    def __eq__(self, other):
        return self.__dict__ == getattr(other, "__dict__", None)

    def toml_data(self):
        return self.__dict__.copy()


class AppIndex:
    def __init__(self, data, config):
        self._data = data
        self.config = config

    def get_num_apps(self):
        return len(self._data)

    def _set_release(self, index_release: IndexRelease):
        assert "." not in index_release.app_id
        self._data[index_release.app_id] = index_release.toml_data()

    def set_release_from_remote(self, app_id, remote_release):
        cur = self.get_release(app_id)
        rel = remote_release
        version = 1
        if cur is not None:
            # if a different release is available, increment version
            if cur.url == rel.url and cur.tag_name == rel.tag_name:
                version = cur.version
            else:
                version = cur.version + 1

        source = self.config.get_xdc_source(app_id)
        index_release = IndexRelease(
            app_id=app_id,
            version=version,
            tag_name=rel.tag_name,
            url=rel.url,
            date=remote_release.date,
            description=source.description,
            source_code_url=source.source_def.source_code_url,
        )
        self._set_release(index_release)
        return index_release

    def get_release(self, app_id):
        release = self._data.get(app_id)
        if release is not None:
            assert app_id == release["app_id"]
            if "cache_relname" in release:
                del release["cache_relname"]
            return IndexRelease(**release)

    def get_next_release_version(self, app_id):
        rel = self.get_release(app_id)
        return (rel.version + 1) if rel else 1

    def iter_releases(self):
        return (self.get_release(app_id) for app_id in self._data)


def get_app_index(config):
    if config.app_index_path.exists():
        with config.app_index_path.open("r") as f:
            lock_data = toml.load(f)
    else:
        lock_data = {}
    return AppIndex(lock_data, config)


@contextmanager
def app_index_writer(config):
    path = config.app_index_path
    if path.exists():
        with path.open("r") as f:
            lock_data = toml.load(f)
    else:
        lock_data = {}
    new_data = copy.deepcopy(lock_data)
    app_index = AppIndex(new_data, config=config)

    yield app_index

    if new_data != lock_data:
        tmp = path.parent.joinpath(path.name + ".tmp")
        with tmp.open("w") as f:
            toml.dump(new_data, f)
        os.rename(tmp, path)


def perform_export(config, out):
    config.export_dir.mkdir(exist_ok=True, parents=True)
    app_index = get_app_index(config)
    num = 0
    for index_release in app_index.iter_releases():
        path = export_to_xdcstore(config, index_release)
        out(f"exported: {path}")
        out(f"          app_id={index_release.app_id} version={index_release.version}")
        num += 1

    if num == 0:
        out.red("No apps to export, did you run 'update' first?")
        raise SystemExit(1)
    dest = config.export_dir.joinpath(config.app_index_path.name)
    shutil.copy(config.app_index_path, dest)
    out.green(f"Exported store metadata for {num} apps to {dest})")


def export_to_xdcstore(config, index_release):
    # XXX needs more tests -- better at unit test level, avoiding network-IO
    cache_path = config.cache_dir.joinpath(index_release.cache_relname)
    xdc_source = config.get_xdc_source(index_release.app_id)
    assert xdc_source is not None, index_release.app_id
    zf = ZipFile(cache_path)
    new_zf_path = config.export_dir.joinpath(index_release.cache_relname)
    new_zf = ZipFile(new_zf_path.open("wb"), compression=ZIP_DEFLATED, mode="w")
    for fname in zf.namelist():
        content = zf.read(fname)
        if fname == "manifest.toml":
            manifest = toml.loads(content.decode("utf-8"))
            manifest["app_id"] = index_release.app_id
            manifest["version"] = index_release.version
            manifest["date"] = index_release.date
            manifest["description"] = xdc_source.description
            # override possibly wrong source_code_urls
            # we know exactly where we are getting the source from
            # so let's just use it.
            manifest["source_code_url"] = index_release.source_code_url

            content = toml.dumps(manifest).encode("utf-8")
        new_zf.writestr(fname, data=content)
    new_zf.close()
    return new_zf_path
