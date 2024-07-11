from pathlib import Path
from tempfile import TemporaryDirectory

from beaver_linter.utils import chunked, find_projects


def test_find_projects():
    with TemporaryDirectory() as tempdir:
        base_path = Path(tempdir)
        project1 = base_path / "project1"
        project2 = base_path / "project2"
        project3 = base_path / "project3"
        key_file_name = "key_file.txt"

        # Create directories and key files
        project1.mkdir()
        (project1 / key_file_name).touch()

        project2.mkdir()
        (project2 / key_file_name).touch()

        project3.mkdir()
        (project3 / "some_other_file.txt").touch()

        result = find_projects(base_path, key_file_name)

        assert sorted(result) == sorted([project1, project2])


def test_chunked():
    # Test with list
    data = [1, 2, 3, 4, 5, 6, 7]
    chunk_size = 3
    expected = [[1, 2, 3], [4, 5, 6], [7]]

    result = list(chunked(data, chunk_size))

    assert result == expected

    # Test with string
    data = "abcdefgh"
    chunk_size = 2
    expected = ["ab", "cd", "ef", "gh"]

    result = list(chunked(data, chunk_size))

    assert result == expected

    # Test with empty list
    data = []
    chunk_size = 3
    expected = []

    result = list(chunked(data, chunk_size))

    assert result == expected
