import argparse
import logging

from mcgen.logging import setup_logging
from mcgen.run import run

DEFAULT_JARPATH = "temp/jars/minecraft_server.{version}.jar"
DEFAULT_RAWPATH = "temp/raw/{version}"
DEFAULT_OUTPATH = "temp/out/{version}"
DEFAULT_VERSION = "snapshot"
DEFAULT_MANIFEST = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
DEFAULT_JAVA_CMD = (
    "java -DbundlerMainClass=net.minecraft.data.Main -jar {jar_path} --server --reports"
)
DEFAULT_PROCESSORS = (
    "mcgen.processors.write_version_file",
    "mcgen.processors.convert_json_files",
    "mcgen.processors.simplify_blocks",
    "mcgen.processors.split_registries",
    "mcgen.processors.summarize_data",
    "mcgen.processors.summarize_worldgen",
    "mcgen.processors.create_all_tags_data_pack",
)

ARG_PARSER = argparse.ArgumentParser(
    prog="mcgen",
    description="Download the Minecraft server jar for the specified version,"
    + " invoke the data generator, and process the output.",
)
ARG_PARSER.add_argument(
    "--jarpath",
    default=DEFAULT_JARPATH,
    help=f"Where to download and store the server jar. Default: {DEFAULT_JARPATH}",
)
ARG_PARSER.add_argument(
    "--rawpath",
    default=DEFAULT_RAWPATH,
    help=f"Where to store the raw server-generated files. Default: {DEFAULT_RAWPATH}",
)
ARG_PARSER.add_argument(
    "--outpath",
    default=DEFAULT_OUTPATH,
    help=f"Where to write the final processed output. Default: {DEFAULT_OUTPATH}",
)
ARG_PARSER.add_argument(
    "--version",
    default=DEFAULT_VERSION,
    help="The server version to download and process. Defaults to latest snapshot.",
)
ARG_PARSER.add_argument(
    "--cmd",
    default=DEFAULT_JAVA_CMD,
    help="The java command to invoke the data generator. This string will be formatted"
    + f" with the `jar_path` argument available. Default: {DEFAULT_JAVA_CMD}.",
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
    jarpath=str(ARGS.jarpath),
    rawpath=str(ARGS.rawpath),
    outpath=str(ARGS.outpath),
    version=str(ARGS.version),
    java_cmd=str(ARGS.cmd),
    manifest_location=str(ARGS.manifest),
    processors=list(ARGS.processors),
)
