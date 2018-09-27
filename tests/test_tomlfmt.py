from unittest import mock
import os

import pytest

import tomlfmt

here = os.path.dirname(__file__)
pyproject_toml = os.path.join(os.path.dirname(here), "pyproject.toml")


@pytest.fixture
def no_write():
    """utility for verifying that no files are written"""

    def open_no_write(path, mode="r"):
        assert mode == "r"
        return open(path, mode)

    with mock.patch.object(tomlfmt, "open", open_no_write):
        yield


def test_tomlfmt(capsys, no_write):
    tomlfmt.main([pyproject_toml])
    out, err = capsys.readouterr()
    assert out == open(pyproject_toml).read()


def test_no_files():
    with pytest.raises(ValueError):
        tomlfmt.format()


def test_inplace(capsys, tmpdir):
    path = tmpdir.join("test.toml")
    with path.open("w") as w:
        with open(os.path.join(here, "test.toml")) as r:
            w.write(r.read())

    tomlfmt.format(str(path), inplace=True)
    out, err = capsys.readouterr()
    assert "✅" in err
    assert out == ""

    with path.open("r") as f:
        result = f.read()

    with open(os.path.join(here, "test.good.toml")) as f:
        expected = f.read()

    assert result == expected


def test_no_change_no_write(capsys, tmpdir, no_write):
    path = tmpdir.join("test.toml")
    with path.open("w") as w:
        with open(os.path.join(here, "test.good.toml")) as r:
            w.write(r.read())

    tomlfmt.format(str(path), inplace=True)
    out, err = capsys.readouterr()
    assert "🎉" in err
    assert out == ""

    with path.open("r") as f:
        result = f.read()

    with open(os.path.join(here, "test.good.toml")) as f:
        expected = f.read()

    assert result == expected


def test_no_write_bad(capsys, no_write):
    tomlfmt.format(__file__, inplace=True)
    out, err = capsys.readouterr()
    assert "❌" in err
    assert out == ""


def test_no_out_bad(capsys, no_write):
    tomlfmt.format(__file__, inplace=True)
    out, err = capsys.readouterr()
    assert out == ""
    assert "❌" in err
