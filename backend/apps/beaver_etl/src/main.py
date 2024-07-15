from src.clients import get_client
from src.parsers import get_parser
from src.services import get_service
from src.settings import get_settings


def main() -> None:
    settings = get_settings()
    client = get_client(
        api_url=settings.service_url, token=settings.api_secret_token
    )
    parser = get_parser(
        path_to_main=settings.relative_path_to_main,
        path_to_pyproject_toml=settings.relative_path_to_pyproject_toml,
        path_to_readme=settings.relative_path_to_readme,
    )
    service = get_service(parser=parser, client=client)
    service.process(
        path_dataset=settings.path_to_dataset,
        chunk_size=settings.chunk_size,
    )


if __name__ == "__main__":
    main()
