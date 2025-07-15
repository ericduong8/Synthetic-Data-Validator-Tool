#!/usr/bin/env python3
"""Allow data_validator to be executable as a module with python -m data_validator."""

from .cli import cli

if __name__ == "__main__":
    cli()
