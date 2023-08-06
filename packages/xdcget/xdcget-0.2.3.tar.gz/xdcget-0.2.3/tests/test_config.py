from pathlib import Path
import pytest

from xdcget.config import line_writer, read_config, parse_sources_ini, InvalidAppId
from xdcget.main import main


class TestConfig:
    def test_init_and_read_config_basics(self, tmpdir):
        tmpdir.chdir()
        main(["init"])
        config = read_config(Path("xdcget.ini"))
        assert config.export_dir == Path("export_dir").absolute()
        assert config.cache_dir == Path("cache_dir").absolute()
        cb = config.api_defs[0]
        assert cb.root_url == "https://codeberg.org"
        assert cb.api_url == "https://codeberg.org/api/v1/"
        gh = config.api_defs[1]
        assert gh.root_url == "https://github.com"
        assert gh.api_url == "https://api.github.com/"

    def test_iter_xdc_sources(self, config_example1):
        xdc1, xdc2 = config_example1.iter_xdc_sources()
        assert xdc1.source_def.source_code_url == "https://github.com/webxdc/checklist"
        assert xdc1.source_def.app_id == "webxdc-checklist"
        assert xdc1.auth
        assert xdc2.source_def.source_code_url == "https://codeberg.org/webxdc/poll"
        assert xdc2.source_def.app_id == "webxdc-poll"
        assert xdc2.auth

    def test_latest_release_api_url(self, config_example1):
        repo1, repo2 = config_example1.iter_xdc_sources()
        assert (
            repo1.latest_release_api_url
            == "https://api.github.com/repos/webxdc/checklist/releases/latest"
        )
        assert (
            repo2.latest_release_api_url
            == "https://codeberg.org/api/v1/repos/webxdc/poll/releases/latest"
        )


class TestSourcesIni:
    @pytest.mark.parametrize("app_id", ["A-b", "a-b-", "-a-b", "0a", "Aa", "a.b"])
    def test_app_id_fails(self, tmp_path, app_id):
        sources_ini_path = tmp_path.joinpath("sources.ini")
        with line_writer(sources_ini_path) as w:
            w(f"[{app_id}]")
            w('source_code_url = "https://github.com/webxdc/checklist"')
        with pytest.raises(InvalidAppId):
            parse_sources_ini(sources_ini_path)

    @pytest.mark.parametrize("app_id", ["a", "a-b", "a-b-c", "a0", "a0-b"])
    def test_app_id_ok(self, tmp_path, app_id):
        sources_ini_path = tmp_path.joinpath("sources.ini")
        with line_writer(sources_ini_path) as w:
            w(f"[{app_id}]")
            w('source_code_url = "https://github.com/webxdc/checklist"')
        parse_sources_ini(sources_ini_path)
