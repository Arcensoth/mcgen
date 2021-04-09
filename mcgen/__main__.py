import argparse
import logging
from pathlib import Path

from mcgen.logging import setup_logging
from mcgen.run import run

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
    default="mcgen/jars",
    help="Where to download and store server jars. Default: mcgen/jars",
)
ARG_PARSER.add_argument(
    "--rawdir",
    default="mcgen/raw",
    help="Where to store the raw server-generated files. Default: mcgen/raw",
)
ARG_PARSER.add_argument(
    "--outdir",
    default="mcgen/out",
    help="Where to write the final processed output. Default: mcgen/out",
)
ARG_PARSER.add_argument(
    "--version",
    default="snapshot",
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
    + " Defaults to a pre-defined set of basic processors.",
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
