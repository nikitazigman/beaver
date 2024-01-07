import json
import os

from beaver_api.api.server import VERSION
from beaver_api.api.server import app as server
from beaver_api.api.server import run_dev_server as dev_server

import typer
from fastapi.openapi.utils import get_openapi


app = typer.Typer()


@app.command(
    name="schema",
    help="Command to generate a fresh openapi schema based on app routes"
)
def generate_schema():
    schema = json.dumps(get_openapi(
        title="BeaverAPI",
        version=VERSION,
        description="BeaverAPI openapi specification",
        routes=server.routes,
    ))
    filepath = os.path.join(os.getcwd(), "docs", "openapi-schema", f"openapi_{VERSION}.json")
    with open(filepath, "w") as file:
        file.write(schema)
        file.flush()


@app.command(
    name="dev-server",
    help="Command to run a dev server that is easy to debug"
)
def run_dev_server():
    dev_server()
