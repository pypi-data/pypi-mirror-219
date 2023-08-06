import typer
from typing_extensions import Annotated
from pathlib import Path
from geovisio_cli import sequence, exception, model, auth, utils, __version__
from rich import print
from rich.panel import Panel
from typing import Optional
import os


app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"GeoVisio command-line client ([blue bold]v{__version__}[/blue bold])")
        utils.check_if_lastest_version()
        raise typer.Exit()


@app.callback(help=f"GeoVisio command-line client (v{__version__})")
def common(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show GeoVisio command-line client version and exit",
        ),
    ] = None,
):
    pass


@app.command()
def upload(
    path: Path = typer.Argument(..., help="Local path to your sequence folder"),
    api_url: str = typer.Option(..., help="GeoVisio endpoint URL"),
    user: str = typer.Option(
        default=None,
        hidden=True,
        help="""DEPRECATED: GeoVisio user name if the geovisio instance needs it.
If none is provided and the geovisio instance requires it, the username will be asked during run.
""",
        envvar="GEOVISIO_USER",
    ),
    password: str = typer.Option(
        default=None,
        hidden=True,
        help="""DEPRECATED: GeoVisio password if the geovisio instance needs it.
If none is provided and the geovisio instance requires it, the password will be asked during run.
Note: is is advised to wait for prompt without using this variable.
""",
        envvar="GEOVISIO_PASSWORD",
    ),
    wait: bool = typer.Option(default=False, help="Wait for all pictures to be ready"),
    isBlurred: bool = typer.Option(
        False,
        "--is-blurred/--is-not-blurred",
        help="Define if sequence is already blurred or not",
    ),
    title: Optional[str] = typer.Option(
        default=None,
        help="Collection title. If not provided, the title will be the directory name.",
    ),
    token: Optional[str] = typer.Option(
        default=None,
        help="""GeoVisio token if the geovisio instance needs it.

If none is provided and the geovisio instance requires it, the token will be asked during run.
Note: is is advised to wait for prompt without using this variable.
""",
    ),
    sort_method: Optional[sequence.SortMethod] = typer.Option(
        default="time-asc",
        help="Strategy used for sorting your pictures. Either by filename or EXIF time, in ascending or descending order.",
    ),
):
    """Processes and sends a given sequence on your GeoVisio API"""

    def cmd():
        if user or password:
            raise exception.CliException(
                "user/password authentication have been deprecated, use a token or `geovisio login` instead"
            )
        geovisio = model.Geovisio(url=api_url, token=token)
        sequence.upload(
            path,
            geovisio,
            wait=wait,
            alreadyBlurred=isBlurred,
            title=title,
            sortMethod=sort_method,
        )

    _run_command(cmd, "importing collection")


@app.command()
def test_process(
    path: Path = typer.Argument(..., help="Local path to your sequence folder"),
    title: Optional[str] = typer.Option(
        default=None,
        help="Collection title. If not provided, the title will be the directory name.",
    ),
    sort_method: Optional[sequence.SortMethod] = typer.Option(
        default="time-asc",
        help="Strategy used for sorting your pictures. Either by filename or EXIF time, in ascending or descending order.",
    ),
):
    """(For testing) Generates a TOML file with metadata used for upload"""

    def cmd():
        sequence.process(path, title, sortMethod=sort_method)
        outputFile = os.path.join(path, sequence.SEQUENCE_TOML_FILE)
        print(
            "✅ [green]Metadata file saved to: [bold]" + outputFile + "[/bold][/green]"
        )

    _run_command(cmd, "processing collection")


@app.command()
def collection_status(
    id: Optional[str] = typer.Option(default=None, help="Id of the collection"),
    api_url: Optional[str] = typer.Option(default=None, help="GeoVisio endpoint URL"),
    location: Optional[str] = typer.Option(
        default=None, help="Full url of the collection"
    ),
    wait: bool = typer.Option(default=False, help="wait for all pictures to be ready"),
):
    """
    Print the status of a collection.\n
    Either a --location should be provided, with the full location url of the collection
    or only the --id combined with the --api-url
    """

    def cmd():
        if location is None:
            if api_url is None or id is None:
                raise exception.CliException(
                    "The way to identify the collection should be either with --location or with --id combined with --api-url"
                )
            l = f"{api_url}/api/collections/{id}"
        else:
            l = location

        mySequence = sequence.Sequence(id=id, location=l)
        sequence.display_sequence_status(mySequence)

        if wait:
            sequence.wait_for_sequence(mySequence)

    _run_command(cmd, "getting collection status")


@app.command(
    help=f"""
    Authenticate into the given instance, and save credentials in a configuration file.

    This will generate credentials, and ask the user to visit a page to associate those credentials to the user's account.

    The credentials will be stored in {auth.get_config_file_path()}
    """
)
def login(
    api_url: str = typer.Option(..., help="GeoVisio endpoint URL"),
):
    return _run_command(
        lambda: auth.create_auth_credentials(model.Geovisio(url=api_url)),
        "authenticating",
    )


def _run_command(command, command_name_for_error):
    try:
        utils.check_if_lastest_version()
        command()
    except exception.CliException as e:
        print(
            Panel(
                f"{e}",
                title=f"[red]Error while {command_name_for_error}",
                border_style="red",
            )
        )
        return 1
