import argparse
import logging
from pathlib import Path

from mcgen.logging import setup_logging
from mcgen.run import run

DEFAULT_JARSDIR = "temp/mcgen/jars"
DEFAULT_RAWDIR = "temp/mcgen/raw"
DEFAULT_OUTDIR = "temp/mcgen/out"
DEFAULT_VERSION = "snapshot"
DEFAULT_MANIFEST = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
DEFAULT_PROCESSORS = (
    "mcgen.processors.convert_json_files",
    "mcgen.processors.split_registries",
    "mcgen.processors.summarize_data",
    "mcgen.processors.summarize_biomes",
    "mcgen.processors.write_version_file",
)

ARG_PARSER = argparse.ArgumentParser(
    prog="mcgen",
    description="Download the Minecraft server jar for the specified version,"
    + " invoke the data generator, and process the output.",
)
ARG_PARSER.add_argument(
    "--jarsdir",
    default=DEFAULT_JARSDIR,
    help=f"Where to download and store server jars. Default: {DEFAULT_JARSDIR}",
)
ARG_PARSER.add_argument(
    "--rawdir",
    default=DEFAULT_RAWDIR,
    help=f"Where to store the raw server-generated files. Default: {DEFAULT_RAWDIR}",
)
ARG_PARSER.add_argument(
    "--outdir",
    default=DEFAULT_OUTDIR,
    help=f"Where to write the final processed output. Default: {DEFAULT_OUTDIR}",
)
ARG_PARSER.add_argument(
    "--version",
    default=DEFAULT_VERSION,
    help="The server version to download and process. Defaults to latest snapshot.",
)
ARG_PARSER.add_argument(
    "--manifest",
    default=DEFAULT_MANIFEST,
    help="Where to fetch the version manifest from. Defaults to Mojang's online copy.",
)
ARG_PARSER.add_argument(
    "--processors",
    default=DEFAULT_PROCESSORS,
    nargs="*",
    help="Which processors to use in processing the raw server-generated files."
    + " Defaults to a set of built-in processors.",
)
ARG_PARSER.add_argument(
    "--log",
    default=logging.WARNING,
    help="The level of verbosity at which to print log messages.",
)
ARGS = ARG_PARSER.parse_args()

setup_logging(ARGS.log)


run(
    jarsdir=Path(ARGS.jarsdir).absolute(),
    rawdir=Path(ARGS.rawdir).absolute(),
    outdir=Path(ARGS.outdir).absolute(),
    version=str(ARGS.version),
    manifest_location=str(ARGS.manifest),
    processors=list(ARGS.processors),
)
