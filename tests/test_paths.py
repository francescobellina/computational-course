from pathlib import Path

import pytest

from computational_course.paths import find_project_root


def test_find_project_root_from_a_subfolder():
    root = find_project_root(Path(__file__).resolve().parent)
    assert (root / "pyproject.toml").exists()
    assert (root / "src" / "computational_course").is_dir()


def test_find_project_root_fails_outside_a_project(tmp_path):
    with pytest.raises(FileNotFoundError):
        find_project_root(tmp_path)
