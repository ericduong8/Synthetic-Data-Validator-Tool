import click
from .validators import validate_file

@click.group()
def cli():
    """Data Validator CLI."""

@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--json-output", "-j", type=click.Path(), help="Write report to JSON")
def validate(files, json_output):
    """
    Validate one or more CSV/JSON data FILES for missing values, format errors, and range violations.
    """
    full_report = {}
    for path in files:
        report = validate_file(path)
        full_report[path] = report
        click.echo(f"{path}: {report['summary']}")
    if json_output:
        import json
        with open(json_output, "w") as fp:
            json.dump(full_report, fp, indent=2)
        click.echo(f"Full report written to {json_output}")
