from __future__ import annotations

import logging
import sys

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib
from pathlib import Path
from typing import TYPE_CHECKING

import click

from capsula._monitor import MonitorConfig, MonitoringHandlerCli
from capsula.capture import CaptureConfig
from capsula.capture import capture as capture_core

if TYPE_CHECKING:
    from collections.abc import Iterable


@click.group()
@click.option(
    "--directory",
    "-C",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True, path_type=Path),
    default=Path.cwd(),
    help="The working directory to use. Defaults to the current directory.",
)
@click.option(
    "--log-level",
    "-l",
    type=click.Choice(
        [
            "CRITICAL",
            # "FATAL", # FATAL is an alias for CRITICAL
            "ERROR",
            # "WARN", # WARN is an alias for WARNING
            "WARNING",
            "INFO",
            "DEBUG",
            "NOTSET",
        ],
    ),
    default="INFO",
    help="The log level to use. Defaults to INFO.",
)
@click.pass_context
def main(
    ctx: click.Context,
    directory: Path,
    log_level: str,
) -> None:
    ctx.ensure_object(dict)
    logging.basicConfig(level=logging.getLevelNamesMapping()[log_level])

    ctx.obj["directory"] = directory
    click.echo(f"directory: {ctx.obj['directory']}")
    capsula_config_path: Path = ctx.obj["directory"] / "capsula.toml"
    with capsula_config_path.open("rb") as capsula_config_file:
        capsula_config = tomllib.load(capsula_config_file)

    ctx.obj["capsula_config"] = capsula_config


@main.command()
@click.pass_context
def capture(ctx: click.Context) -> None:
    """Capture the context."""
    capsula_capture_config = CaptureConfig(**ctx.obj["capsula_config"]["capture"])
    capsula_capture_config.root_directory = ctx.obj["directory"]
    capture_core(config=capsula_capture_config)


@main.command()
@click.option(
    "--item",
    "-i",
    "items",
    multiple=True,
    default=(),
    help="The item to monitor defined in the capsula.toml file.",
)
@click.argument("args", nargs=-1)
@click.pass_context
def monitor(ctx: click.Context, items: Iterable[str], args: tuple[str]) -> None:
    """Monitor execution."""
    capture_config = CaptureConfig(**ctx.obj["capsula_config"]["capture"])
    capture_config.root_directory = ctx.obj["directory"]
    capture_core(config=capture_config)

    monitor_config = MonitorConfig(**ctx.obj["capsula_config"]["monitor"])
    handler = MonitoringHandlerCli(capture_config=capture_config, monitor_config=monitor_config)
    pre_run_info = handler.setup(args)
    handler.run_and_teardown(pre_run_info=pre_run_info, items=items)
