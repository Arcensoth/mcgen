import json
import logging
import subprocess
import urllib.request
from importlib import import_module
from pathlib import Path
from typing import Any, List

from mcgen.context import Context

LOG = logging.getLogger(__name__)


def run(
    jarsdir: Path,
    rawdir: Path,
    outdir: Path,
    version: str,
    manifest_location: str,
    processors: List[Any],
):
    LOG.info(f"Using jarsdir: {jarsdir}")
    jarsdir.mkdir(parents=True, exist_ok=True)

    LOG.info(f"Using rawdir: {rawdir}")
    rawdir.mkdir(parents=True, exist_ok=True)

    LOG.info(f"Using outdir: {outdir}")
    outdir.mkdir(parents=True, exist_ok=True)

    LOG.info(f"Using version: {version}")
    LOG.info(f"Using manifest location: {manifest_location}")

    # load the version manifest (remote or local)
    if manifest_location.startswith(("http://", "https://")):
        LOG.info(f"Fetching remote version manifest from: {manifest_location}")
        manifest_raw = urllib.request.urlopen(manifest_location).read()
        manifest = json.loads(manifest_raw)
    else:
        LOG.info(f"Loading local version manifest from: {manifest_location}")
        with open(manifest_location) as manifest_fp:
            manifest = json.load(manifest_fp)

    # resolve the version (release, snapshot, etc)
    if version == "release":
        resolved_version = manifest["latest"]["release"]
        LOG.info(f"Resolved latest release version: {resolved_version}")
    elif version == "snapshot":
        resolved_version = manifest["latest"]["snapshot"]
        LOG.info(f"Resolved latest snapshot version: {resolved_version}")
    else:
        resolved_version = version

    # get the corresponding version entry
    version_entry = next(v for v in manifest["versions"] if v["id"] == resolved_version)
    assert version_entry is not None

    # download the server jar if we don't already have it
    server_jar_path = jarsdir / f"minecraft_server.{resolved_version}.jar"
    if not server_jar_path.exists():
        LOG.info("Unable to find local server jar; requires download")

        # download the version data
        version_url = version_entry["url"]
        LOG.info(f"Downloading version data from: {version_url}")
        version_data_raw = urllib.request.urlopen(version_url).read()
        version_data = json.loads(version_data_raw)

        # download the server jar
        server_jar_url = version_data["downloads"]["server"]["url"]
        LOG.info(f"Downloading server jar from: {server_jar_url}")
        server_jar_raw = urllib.request.urlopen(server_jar_url).read()
        LOG.info(f"Saving server jar to: {server_jar_path}")
        with open(server_jar_path, "wb") as jar_fp:
            jar_fp.write(server_jar_raw)

    else:
        LOG.info(f"Found local server jar at: {server_jar_path}")

    # keep the server-generated data for this version in its own folder
    version_rawdir = rawdir / resolved_version
    LOG.info(f"Storing version's raw data under: {version_rawdir}")
    if not version_rawdir.exists():
        version_rawdir.mkdir()
        # invoke the server's data generator via subprocess
        java_cmd = (
            f"java -cp {server_jar_path} net.minecraft.data.Main --server --reports"
        )
        LOG.info(f"Invoking server's data generator with: {java_cmd}")
        LOG.info("-" * 80)
        java_proc = subprocess.Popen(java_cmd.split(), cwd=version_rawdir)
        java_result = java_proc.wait()
        LOG.info("-" * 80)
        LOG.info(f"Server's data generator completed with result: {java_result}")
    else:
        LOG.warning(
            f"Generated data for version {resolved_version} already exists at: {version_rawdir}"
        )

    # also keep the processed data for this version in its own folder
    version_outdir = outdir / resolved_version
    LOG.info(f"Storing version's processed data under: {version_outdir}")
    if not version_outdir.exists():
        version_outdir.mkdir()
    else:
        LOG.warning(
            f"Processed data for version {resolved_version} already exists at: {version_outdir}"
        )

    # create context and run processors
    LOG.info("Processing data...")
    ctx = Context(
        input_dir=version_rawdir / "generated",
        output_dir=version_outdir,
        version=resolved_version,
    )
    for processor in processors:
        try:
            if isinstance(processor, str):
                processor_name = processor
                processor_options = {}
                processor_disabled = processor_name.startswith("!")
            elif isinstance(processor, dict):
                processor_name = processor["name"]
                processor_options = processor.get("options", {})
                processor_disabled = processor.get("disabled", False)
            else:
                raise ValueError(f"Invaid processor: {processor}")
            if processor_disabled:
                continue
            processor_module = import_module(processor_name)
            processor_function = getattr(processor_module, "process")
            LOG.info(f"Running processor: {processor_name}")
            processor_function(ctx, **processor_options)
        except:
            LOG.exception(f"Skipping processor because it caused an error: {processor}")

    LOG.info("Done!")
