#!/usr/bin/env python3
"""
Serena CLI - Command Line Interface for the Serena coding agent toolkit
"""

import glob
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
from sensai.util import logging

from serena.agent import SerenaAgent, SerenaConfig
from serena.config.context_mode import SerenaAgentContext, SerenaAgentMode
from serena.constants import DEFAULT_CONTEXT, DEFAULT_MODES, SERENA_LOG_FORMAT
from serena.util.exception import show_fatal_exception_safe
from serena.util.logging import MemoryLogHandler

log = logging.getLogger(__name__)


def _open_in_editor(file_path: str) -> None:
    """Open a file in the default editor."""
    if sys.platform == "win32":
        os.startfile(file_path)
    elif sys.platform == "darwin":
        subprocess.run(["open", file_path])
    else:
        subprocess.run(["xdg-open", file_path])


class ProjectType(click.ParamType):
    """Custom click parameter type for project paths."""
    
    name = "project"
    
    def convert(self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]) -> str:
        if isinstance(value, str):
            return value
        self.fail(f"{value!r} is not a valid project path", param, ctx)


class AutoRegisteringGroup(click.Group):
    """A click group that automatically registers commands from modules."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._auto_register_commands()
    
    def _auto_register_commands(self) -> None:
        """Automatically register commands from the commands module."""
        try:
            from serena.commands import *  # noqa: F403, F401
        except ImportError:
            pass  # Commands module not available


@click.group(cls=AutoRegisteringGroup)
@click.option(
    "--verbose", "-v", 
    is_flag=True, 
    help="Enable verbose logging"
)
@click.option(
    "--debug", 
    is_flag=True, 
    help="Enable debug logging"
)
@click.option(
    "--log-file", 
    type=click.Path(), 
    help="Log to file instead of stderr"
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, debug: bool, log_file: Optional[str]) -> None:
    """Serena - AI-powered coding agent toolkit."""
    # Configure logging
    level = logging.DEBUG if debug else (logging.INFO if verbose else logging.WARNING)
    
    if log_file:
        logging.basicConfig(
            level=level,
            filename=log_file,
            format=SERENA_LOG_FORMAT
        )
    else:
        logging.basicConfig(
            level=level,
            stream=sys.stderr,
            format=SERENA_LOG_FORMAT
        )
    
    # Store configuration in context
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["debug"] = debug
    ctx.obj["log_file"] = log_file


@cli.command()
def version() -> None:
    """Show the version of Serena."""
    from serena import serena_version
    click.echo(f"Serena {serena_version()}")


@cli.command()
@click.option(
    "--project", "-p",
    type=ProjectType(),
    help="Project directory or name"
)
@click.option(
    "--context", "-c",
    default=DEFAULT_CONTEXT,
    help="Context configuration to use"
)
def init(project: Optional[str], context: str) -> None:
    """Initialize a new Serena project."""
    if not project:
        project = os.getcwd()
    
    project_path = Path(project).resolve()
    
    if not project_path.exists():
        project_path.mkdir(parents=True, exist_ok=True)
    
    config_file = project_path / ".serena" / "config.json"
    config_file.parent.mkdir(exist_ok=True)
    
    config = {
        "project_name": project_path.name,
        "project_path": str(project_path),
        "context": context,
        "modes": DEFAULT_MODES,
        "created_at": str(Path().ctime())
    }
    
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    click.echo(f"Initialized Serena project in {project_path}")
    click.echo(f"Configuration saved to {config_file}")


@cli.command()
@click.option(
    "--project", "-p",
    type=ProjectType(),
    help="Project directory or name"
)
@click.option(
    "--context", "-c",
    default=DEFAULT_CONTEXT,
    help="Context configuration to use"
)
@click.option(
    "--mode", "-m",
    multiple=True,
    help="Agent modes to enable"
)
def start(project: Optional[str], context: str, mode: List[str]) -> None:
    """Start the Serena agent."""
    try:
        if not project:
            project = os.getcwd()
        
        # Load configuration
        agent_context = SerenaAgentContext.load(context)
        modes = [SerenaAgentMode.load(m) for m in (mode or DEFAULT_MODES)]
        
        config = SerenaConfig(
            project_path=project,
            context=agent_context,
            modes=modes
        )
        
        # Create and start agent
        agent = SerenaAgent(config)
        
        click.echo(f"Starting Serena agent for project: {project}")
        click.echo(f"Context: {context}")
        click.echo(f"Modes: {[m.name for m in modes]}")
        
        # This would start the agent in interactive mode
        # For now, just show that it's configured
        click.echo("Agent configured successfully!")
        
    except Exception as e:
        show_fatal_exception_safe(e)
        sys.exit(1)


@cli.command()
@click.option(
    "--project", "-p",
    type=ProjectType(),
    help="Project directory or name"
)
def status(project: Optional[str]) -> None:
    """Show the status of a Serena project."""
    if not project:
        project = os.getcwd()
    
    project_path = Path(project).resolve()
    config_file = project_path / ".serena" / "config.json"
    
    if not config_file.exists():
        click.echo(f"No Serena project found in {project_path}")
        click.echo("Run 'serena init' to initialize a project.")
        return
    
    with open(config_file) as f:
        config = json.load(f)
    
    click.echo(f"Project: {config.get('project_name', 'Unknown')}")
    click.echo(f"Path: {config.get('project_path', project_path)}")
    click.echo(f"Context: {config.get('context', 'Unknown')}")
    click.echo(f"Modes: {', '.join(config.get('modes', []))}")
    click.echo(f"Created: {config.get('created_at', 'Unknown')}")


if __name__ == "__main__":
    cli()