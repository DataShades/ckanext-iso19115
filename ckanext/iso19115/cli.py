import json
import logging
import sys
from typing import Optional

import ckan.plugins.toolkit as tk
import click
import xmlschema

from ckanext.iso19115 import utils

log = logging.getLogger(__name__)


def get_commands():
    return [iso19115]


@click.group(short_help="ISO19115 tools")
def iso19115():
    pass


@iso19115.group(invoke_without_command=True)
def build():
    """..."""
    pass


@build.command("xml")
@click.argument("source", type=click.File("r"), default=sys.stdin)
def build_xml(source):
    content = bytes(source.read(), "utf8")
    b = utils.get_builder("mdb:MD_Metadata")
    xml = xmlschema.etree_tostring(b.build(json.loads(content)), namespaces=utils.ns)

    click.echo(xml)


@build.command("describe")
@click.option("-r", "--root", default="mdb:MD_Metadata")
@click.option("-s", "--skip-optional", is_flag=True)
@click.option("-d", "--max-depth", type=int, default=0)
@click.option("-q", "--qualified", is_flag=True)
@click.option("-v", "--annotated", is_flag=True)
@click.option(
    "-f",
    "--format",
    type=click.Choice(["overview", "dataclass"]),
    default="overview",
)
def build_describe(
    root: str,
    skip_optional: bool,
    format: str,
    qualified: bool,
    max_depth: int,
    annotated: bool,
):
    b = utils.get_builder(root)
    b.print_tree(format, skip_optional, qualified, max_depth, annotated)


@build.command("example")
@click.option("-r", "--root", default="mdb:MD_Metadata")
@click.option("-f", "--format", type=click.Choice(["json", "xml"]), default="json")
@click.option(
    "--seed",
)
@click.option("-s", "--skip-optional", is_flag=True)
@click.option("-d", "--max-depth", type=int, default=0)
def build_example(
    root: str,
    format: str,
    seed: Optional[str],
    skip_optional: bool,
    max_depth: int,
):
    b = utils.get_builder(root)
    example = b.example(format, seed, skip_optional, max_depth)
    click.echo(example)


@iso19115.group()
def cache():
    """Cache management."""
    pass


@cache.command("clear")
def cache_clear():
    """Remove compiled schema cache files."""
    cache_dir = utils.get_cache_dir(create=False)
    persistent_dir = tk.config.get(utils.CONFIG_CACHE_DIR)

    if not persistent_dir:
        click.echo(
            f"Persistent cache directory is not configured "
            f"({utils.CONFIG_CACHE_DIR}). Using temporary path: {cache_dir}"
        )

    if not cache_dir.exists():
        click.echo(f"Cache directory {cache_dir} does not exist.")
        return

    if not cache_dir.is_dir():
        raise click.ClickException(f"Cache path {cache_dir} is not a directory.")

    removed = 0
    errors = []
    for cache_file in cache_dir.glob("*.pickle"):
        try:
            cache_file.unlink()
            removed += 1
        except OSError as exc:
            errors.append((cache_file, exc))

    for path, exc in errors:
        tk.error_shout(f"Failed to remove {path}: {exc}")

    if errors:
        raise click.ClickException("Unable to clear cache completely.")

    if removed:
        click.secho(f"Removed {removed} cache file(s) from {cache_dir}", fg="green")
    else:
        click.echo(f"No cache files found in {cache_dir}")


@iso19115.group()
def validate():
    """Validate data agains ISO 19115 schema."""
    pass


@validate.command("file")
@click.argument("source", type=click.File("r"), default=sys.stdin)
@click.option("--codelist", is_flag=True)
@click.option("--schematron", is_flag=True)
def validate_file(source, codelist: bool, schematron: bool):
    """Validate file/STDIN agains ISO 19115"""

    content = bytes(source.read(), "utf8")
    try:
        utils.validate_schema(content, validate_codelists=codelist)
        if schematron:
            utils.validate_schematron(content)
    except tk.ValidationError as e:
        for f, error in e.error_summary.items():
            tk.error_shout(f"{f}: {error}")
    else:
        click.secho("Provided document is valid", fg="green")
