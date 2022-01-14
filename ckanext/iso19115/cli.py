import sys
import click
import ckan.plugins.toolkit as tk
from ckanext.iso19115 import utils


def get_commands():
    return [iso19115]


@click.group(short_help="ISO19115 tools")
def iso19115():
    pass


@iso19115.group()
def validate():
    pass


@validate.command("file")
@click.argument("source", type=click.File("rb"), default=sys.stdin)
@click.option("--codelist", is_flag=True)
@click.option("--schematron", is_flag=True)
def validate_file(source, codelist: bool, schematron: bool):
    """Validate file/STDIN agains ISO 19115"""

    content = source.read()
    try:
        utils.validate_schema(content, validate_codelists=codelist)
        if schematron:
            utils.validate_schematron(content)
    except tk.ValidationError as e:
        for f, error in e.error_summary.items():
            tk.error_shout(f"{f}: {error}")
    else:
        click.secho("Provided document is valid", fg="green")
