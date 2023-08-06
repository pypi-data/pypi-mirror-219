from typing import Optional

import typer

# from predibase.cli_commands import create
# from predibase.cli_commands import list
# from predibase.cli_commands import run
from predibase.cli_commands import delete, deploy, prompt, settings
from predibase.cli_commands.settings import load_settings, save_local_settings
from predibase.cli_commands.utils import set_defaults_from_settings

app = typer.Typer(help="Predibase CLI commands")

app.add_typer(deploy.app, name="deploy", help="Deploy Predibase resources")
app.add_typer(delete.app, name="delete", help="Delete Predibase resources")
app.add_typer(prompt.app, name="prompt", help="Prompt Predibase models")
app.add_typer(settings.app, name="settings", help="Configure Predibase settings")


@app.command(help="Initialize default model repository and engine")
def init(
    repository_name: Optional[str] = typer.Option(
        None,
        "--repository-name",
        "-r",
        help="The optional model repository name",
    ),
    engine_name: Optional[str] = typer.Option(None, "--engine-name", "-e", help="The optional engine name"),
):
    save_local_settings({k: v for k, v in dict(repo=repository_name or "", engine=engine_name or "").items() if v})


def main():
    set_defaults_from_settings(load_settings())
    app()


if __name__ == "__main__":
    main()
