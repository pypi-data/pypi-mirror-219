import contextlib
import re
import typing
import click
from halo import Halo  # type: ignore[import]

import pathlib
import yaml
from pydantic import BaseModel

import jinja2

from click_schema_config.read_config import read_configs

import black, black.const


# TODO: Allow nested spinner?
@contextlib.contextmanager
def spinner(*args: typing.Any, **kwargs: typing.Any):
    with Halo(*args, **kwargs) as halo:
        try:
            yield halo
            halo.succeed()
        except Exception as e:
            halo.fail()
            raise e


jinja = jinja2.Environment(
    loader=jinja2.FileSystemLoader(pathlib.Path(__file__).with_name("templates")),
    trim_blocks=True,
    lstrip_blocks=True,
)


class Schema(BaseModel):
    """
    Schema for the codegen.yaml file
    """

    """
    Folder to generate the dataclasses in
    """
    generated_dir: str = "./generated/codegen_ini/"

    """
    Dictionary of dataclasses to generate

    Key is the name of the dataclass, value is the list of files to read in order to generate the dataclass
    """
    schemas: dict[str, list[str] | str]


@click.command()
@click.option("--config", type=click.File("r"), default="codegen.yaml")
@click.pass_context
def codegen(ctx: click.Context, config: click.File) -> None:
    """
    Generate dataclasses from ini config files

    This is a command-line utility to complement click-schema-config.
    It generates the pydantic schema that represents the dict passed to click functions decorated
    with schema_from_inis with the same files.
    """
    config_parsed = Schema.model_validate(yaml.safe_load(config))  # type: ignore[arg-type]
    output_dir = pathlib.Path(config_parsed.generated_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with spinner(text="Generating schemas", spinner="dots"):
        dataclass_template = jinja.get_template(
            "dataclass.py.jinja",
        )

        for name, inis in config_parsed.schemas.items():
            with spinner(text=f"Generating {name}.py", spinner="dots"):
                dataclass_to_generate = read_configs(inis)
                with open(output_dir / f"{name}.py", "w") as f:
                    f.write(
                        dataclass_template.render(
                            name=name,
                            variables=[
                                v
                                for section in dataclass_to_generate.values()
                                for v in section.values()
                            ],
                        )
                    )

    with spinner(text=f"Generating __init__.py", spinner="dots"):
        init_template = jinja.get_template("__init__.py.jinja")
        with open(output_dir / "__init__.py", "w") as f:
            f.write(init_template.render(dataclasses=config_parsed.schemas.keys()))

    with spinner(text=f"Running black", spinner="dots"):
        # Sadly, click does not seem to automatically convert the arguments to their types
        try:
            ctx.invoke(
                black.main,
                target_version=[],
                src=("./generated",),
                include=re.compile(black.const.DEFAULT_INCLUDES),
                quiet=True,
            )
        except click.exceptions.Exit:
            pass


if __name__ == "__main__":
    codegen()
