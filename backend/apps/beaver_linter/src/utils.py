from collections.abc import Generator
from pathlib import Path


def find_projects(path: Path, key_file: str) -> list[Path]:
    projects_paths: list[Path] = []

    def _recursion(path: Path) -> None:
        if path.joinpath(key_file).exists():
            projects_paths.append(path)
            return

        for project in path.iterdir():
            if project.is_dir():
                _recursion(project)

    _recursion(path)

    return projects_paths


def chunked[T](iterable: T, chunk_size: int) -> Generator[T, None, None]:
    """Yield successive n-sized chunks from iterable."""
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i : i + chunk_size]
