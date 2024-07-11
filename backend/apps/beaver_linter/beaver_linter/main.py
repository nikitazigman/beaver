from beaver_linter.parsers import get_parser
from beaver_linter.services import get_service
from beaver_linter.settings import get_settings


def main() -> None:
    settings = get_settings()
    parser = get_parser(
        path_to_main=settings.relative_path_to_main,
        path_to_pyproject_toml=settings.relative_path_to_pyproject_toml,
        path_to_readme=settings.relative_path_to_readme,
    )
    service = get_service(parser=parser)
    service.process(path_dataset=settings.path_to_dataset)


if __name__ == "__main__":
    main()
