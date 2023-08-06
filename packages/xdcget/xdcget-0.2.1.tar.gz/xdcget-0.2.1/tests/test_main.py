import os
import pytest
from xdcget.main import (
    main,
    get_parser,
)


class TestCmdline:
    def test_parser(self):
        parser = get_parser()
        with pytest.raises(SystemExit):
            parser.parse_args([])
        init = parser.parse_args(["init"])
        update = parser.parse_args(["update"])
        assert init and update

    def test_init(self, tmpdir):
        tmpdir.chdir()
        main(["init"])
        assert tmpdir.join("xdcget.ini").exists()
        assert tmpdir.join("sources.ini").exists()

    def test_init_not_overwrite(self, tmpdir):
        tmpdir.chdir()
        main(["init"])
        with pytest.raises(SystemExit):
            main(["init"])

    def test_update_from_different_dir(self, config_example1, tmp_path):
        p = tmp_path.joinpath("somewhere")
        p.mkdir()
        os.chdir(p)
        main(["--toml", "../xdcget.ini", "update"])

    def test_export_empty(self, config_example1, tmp_path):
        os.chdir(tmp_path)
        with pytest.raises(SystemExit):
            main(["export"])

    def test_status_empty(self, config_example1, tmp_path):
        os.chdir(tmp_path)
        with pytest.raises(SystemExit):
            main(["status"])

    def test_update_status_export(self, capfd, config_example1, tmp_path):
        os.chdir(tmp_path)
        main(["update"])
        main(["status"])
        main(["export"])
        p = config_example1.export_dir.joinpath("sources.lock")
        assert p.exists()
        assert len(p.read_text()) > 50
