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
        beaver_file=settings.beaver_file,
        path_to_dataset=settings.path_to_dataset,
    )
    service = get_service(
        parser=parser, client=client, beaver_file=settings.beaver_file
    )

    service.process(
        path_dataset=settings.path_to_dataset,
        chunk_size=settings.chunk_size,
    )


if __name__ == "__main__":
    main()
