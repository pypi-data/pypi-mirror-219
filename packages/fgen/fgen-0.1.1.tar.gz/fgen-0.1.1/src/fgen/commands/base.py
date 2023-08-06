"""
Base utilities for the CLI
"""
import logging

import click

logger = logging.getLogger(__name__)
LOGFORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging() -> None:
    """
    Early setup for logging.
    """
    logging.basicConfig(
        level=logging.INFO,
        format=LOGFORMAT,
    )


@click.group()
def cli() -> None:
    """
    Entrypoint for the CLI
    """
    setup_logging()
