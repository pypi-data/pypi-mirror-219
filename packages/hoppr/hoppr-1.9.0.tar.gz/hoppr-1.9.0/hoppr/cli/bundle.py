"""
`bundle` subcommand for `hoptctl`
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from typer import Argument, Option, Typer

from hoppr import __version__, main

app = Typer(
    context_settings={"help_option_names": ['-h', '--help']},
    help="Run the stages specified in the transfer config file on the content specified in the manifest",
    invoke_without_command=True,
    no_args_is_help=True,
    rich_markup_mode="markdown",
    subcommand_metavar="",
)


@app.callback()
def bundle(
    # pylint: disable=unused-argument
    # pylint: disable=too-many-arguments
    manifest_file: Path = Argument(
        "manifest.yml",
        help="Path to manifest file",
        expose_value=True,
    ),
    credentials_file: Optional[Path] = Option(
        None,
        "-c",
        "--credentials",
        help="Specify credentials config for services",
        envvar="HOPPR_CREDS_CONFIG",
    ),
    transfer_file: Path = Option(
        "transfer.yml",
        "-t",
        "--transfer",
        help="Specify transfer config",
        envvar="HOPPR_TRANSFER_CONFIG",
    ),
    log_file: Optional[Path] = Option(
        None,
        "-l",
        "--log",
        help="File to which log will be written",
        envvar="HOPPR_LOG_FILE",
    ),
    verbose: bool = Option(
        False,
        "-v",
        "--debug",
        "--verbose",
        help="Enable debug output",
    ),
    strict_repos: bool = Option(
        True,
        "--strict/--no-strict",
        help="Utilize only manifest repositories for package collection",
        envvar="HOPPR_STRICT_REPOS",
    ),
    create_attestations: bool = Option(
        False,
        "-a",
        "--attest",
        help="Generate in-toto attestations",
        envvar="HOPPR_ATTESTATION",
    ),
    functionary_key_path: Optional[Path] = Option(
        None,
        "-fk",
        "--functionary-key",
        help="Path to key used to sign in-toto layout",
        envvar="HOPPR_FUNCTIONARY_KEY",
    ),
    functionary_key_prompt: bool = Option(
        False,
        "-p",
        "--prompt",
        help="Prompt user for project owner key's password",
        envvar="HOPPR_PROJECT_OWNER_KEY_PROMPT",
    ),
    functionary_key_password: str = Option(
        None,
        "-fk-pass",
        "--project-owner-key-password",
        help="Password for project owner key",
        envvar="HOPPR_PROJECT_OWNER_KEY_PASSWORD",
    ),
    previous_delivery: Optional[Path] = Option(
        None,
        "-pd",
        "--previous-delivery",
        help="Path to manifest or tar bundle representing a previous delivery",
        envvar="HOPPR_PREVIOUS_DELIVERY",
    ),
):  # pragma: no cover
    """
    Run the stages specified in the transfer config
    file on the content specified in the manifest
    """
    main.bundle(**locals())
