from argparse import ArgumentTypeError
from pathlib import Path
import pytest

from tuxrun.utils import (
    NoProgressIndicator,
    ProgressIndicator,
    TTYProgressIndicator,
    notnone,
    pathnone,
    pathurlnone,
)


def test_progress_class(mocker):
    mocker.patch("sys.stderr.isatty", return_value=True)
    assert isinstance(ProgressIndicator.get("test"), TTYProgressIndicator)

    mocker.patch("sys.stderr.isatty", return_value=False)
    assert isinstance(ProgressIndicator.get("test"), NoProgressIndicator)


def test_notnone():
    assert notnone(None, "fallback") == "fallback"
    assert notnone("", "fallback") == ""
    assert notnone("hello", "fallback") == "hello"


def test_pathurlnone():
    assert pathurlnone(None) is None
    assert pathurlnone("https://example.com/kernel") == "https://example.com/kernel"
    assert pathurlnone(__file__) == f"file://{Path(__file__).expanduser().resolve()}"

    with pytest.raises(ArgumentTypeError) as exc:
        pathurlnone("ftp://example.com/kernel")
    assert exc.match("Invalid scheme 'ftp'")

    with pytest.raises(ArgumentTypeError) as exc:
        pathurlnone("file:///should-not-exists")
    assert exc.match("/should-not-exists no such file or directory")


def test_pathnone():
    assert pathnone(None) is None
    assert pathnone(__file__) == Path(__file__).expanduser().resolve()

    with pytest.raises(ArgumentTypeError) as exc:
        pathnone("/should-not-exists")
    assert exc.match("/should-not-exists no such file or directory")
