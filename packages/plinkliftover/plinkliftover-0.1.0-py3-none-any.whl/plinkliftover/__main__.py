# type: ignore[attr-defined]

import random
from enum import Enum
from typing import Optional

import typer
from rich.console import Console

from plinkliftover import __version__
from plinkliftover.example import hello
from distutils.spawn import find_executable


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


app = typer.Typer(
    name="plinkliftover",
    help="Awesome `plinkliftover` is a Python cli/package created with https://github.com/TezRomacH/python-package-template",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(
            f"[yellow]plinkliftover[/] version: [bold blue]{__version__}[/]"
        )
        raise typer.Exit()


@app.command(name="")
def main(
    name: str = typer.Option(..., help="Name of person to greet."),
    color: Optional[Color] = typer.Option(
        None,
        "-c", "--color", "--colour",
        case_sensitive=False,
        help="Color for name. If not specified then choice will be random.",
    ),
    version: bool = typer.Option(
        None,
        "-v", "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the plinkliftover package.",
    ),
):
    """Prints a greeting for a giving name."""
    if color is None:
        # If no color specified use random value from `Color` class
        color = random.choice(list(Color.__members__.values()))

    greeting: str = hello(name)
    console.print(f"[bold {color}]{greeting}[/]")


def main(
    mapFile: str = typer.Argument(..., help="The plink MAP file to `liftOver`."),
    pedFile: str = typer.Option("", help='Optionally remove "unlifted SNPs" from the plink PED file after running `liftOver`.'),
    datFile: str = typer.Option("", help="Optionally remove 'unlifted SNPs' from a data file containing a list of SNPs (e.g. for  --exclude or --include in `plink`)"),
    prefix: str = typer.Option("", help="The prefix to give to the output files."),
    chainFile: str = typer.Argument(..., help="The location of the chain files to provide to `liftOver`."),
    liftOverExecutable: Optional[str] = typer.Option(None, help="The location of the `liftOver` executable."),
) -> None:
    """Converts genotype data stored in plink's PED+MAP format from one genome
    build to another, using liftOver.
    """
    # Show usage message if user hasn't provided any arguments, rather
    # than giving a non-descript error message with the usage()

    oldBed = f"{mapFile}.bed"
    makesure(map2bed(mapFile, oldBed), "map->bed succ")

    # If a location is not specified for the liftOver executable.
    # assume it is in the User's $PATH.
    if liftOverExecutable is None:
        liftOverPath = find_executable("liftOver")
    else:
        liftOverPath = liftOverExecutable

    newBed = Path(f"{mapFile}.bed")
    unlifted = Path(f"{prefix}.unlifted")
    makesure(liftBed(oldBed, newBed, unlifted, chainFile, liftOverPath), "liftBed succ")

    newMap = Path(f"{prefix}.map")
    makesure(bed2map(newBed, newMap), "bed->map succ")

    if datFile:
        newDat = Path(f"{prefix}.dat")
        makesure(liftDat(datFile, newDat), "liftDat succ")

    if pedFile:
        newPed = Path(f"{prefix}.ped")
        makesure(liftPed(pedFile, newPed, mapFile), "liftPed succ")

    print("cleaning up BED files...")
    newBed.unlink()
    oldBed.unlink()
