"""
This type stub file was generated by pyright.
"""

import click

@click.group(help="""Various commands for the marimo config.""")
def config() -> None:
    ...

@click.command(help="""Show the marimo config""")
def show() -> None:
    """
    Print out marimo config information.
    Example usage:

        marimo config show
    """
    ...

@click.command(help="""Describe the marimo config""")
def describe() -> None:
    """Print documentation for all config options."""
    ...
