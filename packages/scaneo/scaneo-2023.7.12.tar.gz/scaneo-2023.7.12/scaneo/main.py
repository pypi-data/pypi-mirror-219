import typer
import os
import sys
from pathlib import Path

# Add the cli directory to the Python path
scaneo_cli_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scaneo_cli_dir))

app = typer.Typer()


@app.command()
def run(
    port: int = typer.Option(8000, help="Port to run the server on"),
    reload: bool = typer.Option(False, help="Reload the server when files change"),
    host: str = typer.Option("localhost", help="Host to run the server on"),
    data: Path = typer.Option(None, help="Path to data directory"),
    env: Path = typer.Option(
        ".env",
        help="Path to environment file with credentials to cloud bucket: URL, ACCESS_KEY, SECRET_KEY, BUCKET, REGION",
    ),
):
    # we run the cli from some directory, but run the api from the directory where this file is
    # operation done by the api will have the same working directory as the one from which the cli is run
    # pass environment variable to the api before the command, parse in api settings object
    cmd = f"uvicorn api:app --port {port} --host {host} {'--reload' if reload else ''} --app-dir {os.path.dirname(os.path.realpath(__file__))}"
    if env.exists():
        cmd += f" --env-file {env}"
    else:
        typer.echo(f"Environment file {env} not found.")
        if not data:
            raise typer.Exit(
                "Data directory not specified. Either specify a data directory or an environment file with credentials to a cloud bucket."
            )
        cmd = f"DATA={data} {cmd}"
    os.system(cmd)


if __name__ == "__main__":
    app()
