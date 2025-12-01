
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.sustiai import __version__, get_db_connection


def test_package_version():
    assert isinstance(__version__, str) and __version__.count('.') >= 1

