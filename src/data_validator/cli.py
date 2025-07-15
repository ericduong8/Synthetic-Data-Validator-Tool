import click
import json
from .validators import validate_file

@click.group()
def cli():
    """Data Validator CLI for genomics and health data quality control."""

@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--json-output", "-j", type=click.Path(), help="Write detailed report to JSON file")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed validation results")
@click.option("--schema", "-s", type=click.Path(exists=True), help="JSON schema file for validation")
def validate(files, json_output, verbose, schema):
    """
    Validate one or more CSV/JSON data FILES for missing values, data type errors, 
    out-of-range values, and format consistency issues.
    
    Designed for genomics and health data quality control in data pipelines.
    """
    if not files:
        click.echo("No files provided for validation.")
        return
    
    validation_schema = None
    if schema:
        try:
            with open(schema, 'r') as f:
                validation_schema = json.load(f)
        except Exception as e:
            click.echo(f"Error loading schema file: {e}", err=True)
            return
    
    full_report = {}
    total_files = len(files)
    passed_files = 0
    
    click.echo(f"Validating {total_files} file(s)...")
    click.echo("=" * 50)
    
    for path in files:
        report = validate_file(path, validation_schema)
        full_report[path] = report
        
        status_color = "green" if report.get("status") == "PASS" else "red"
        click.echo(f"\nFile: {path}")
        click.echo(f"Status: ", nl=False)
        click.secho(f"{report.get('status', 'UNKNOWN')}", fg=status_color)
        click.echo(f"Summary: {report.get('summary', 'No summary available')}")
        
        if report.get("status") == "PASS":
            passed_files += 1
        
        if verbose and report.get("status") != "ERROR":
            if "missing" in report and report["missing"]:
                click.echo("  Missing values:")
                for col, count in report["missing"]:
                    click.echo(f"    - {col}: {count} missing values")
            
            if "outliers" in report and report["outliers"]:
                click.echo("  Outliers/Range violations:")
                for col, count in report["outliers"]:
                    click.echo(f"    - {col}: {count} outlier(s)")
            
            if "type_errors" in report and report["type_errors"]:
                click.echo("  Data type errors:")
                for col, error in report["type_errors"]:
                    click.echo(f"    - {col}: {error}")
            
            if "format_errors" in report and report["format_errors"]:
                click.echo("  Format errors:")
                for error in report["format_errors"]:
                    click.echo(f"    - {error}")
        
        if report.get("status") == "ERROR":
            click.echo(f"  Error: {report.get('error', 'Unknown error')}")
    
    click.echo("\n" + "=" * 50)
    click.echo(f"Validation Summary: {passed_files}/{total_files} files passed")
    
    if passed_files == total_files:
        click.secho("✓ All files passed validation!", fg="green")
    else:
        failed_files = total_files - passed_files
        click.secho(f"✗ {failed_files} file(s) failed validation", fg="red")
    
    if json_output:
        try:
            with open(json_output, "w") as fp:
                json.dump(full_report, fp, indent=2)
            click.echo(f"\nDetailed report written to: {json_output}")
        except Exception as e:
            click.echo(f"Error writing JSON report: {e}", err=True)
