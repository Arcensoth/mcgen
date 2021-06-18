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
    jarpath: str,
    rawpath: str,
    outpath: str,
    version: str,
    manifest_location: str,
    processors: List[Any],
):
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

    jar_path = Path(jarpath.format(version=resolved_version)).absolute()
    LOG.info(f"Using path for server jar: {jar_path}")

    if jar_path.exists():
        LOG.info(f"Found local server jar at: {jar_path}")

    else:
        LOG.info("Unable to find local server jar; requires download")

        # create parent directories
        jar_path.parent.mkdir(parents=True, exist_ok=True)

        # download the version data
        version_url = version_entry["url"]
        LOG.info(f"Downloading version data from: {version_url}")
        version_data_raw = urllib.request.urlopen(version_url).read()
        version_data = json.loads(version_data_raw)

        # download the server jar
        server_jar_url = version_data["downloads"]["server"]["url"]
        LOG.info(f"Downloading server jar from: {server_jar_url}")
        server_jar_raw = urllib.request.urlopen(server_jar_url).read()
        LOG.info(f"Saving server jar to: {jar_path}")
        with open(jar_path, "wb") as jar_fp:
            jar_fp.write(server_jar_raw)

    # resolve the path to the raw data
    raw_path = Path(rawpath.format(version=resolved_version)).absolute()
    LOG.info(f"Using directory for raw data: {raw_path}")
    if raw_path.exists():
        raise Exception(f"Directory for raw data already exists at: {raw_path}")
    raw_path.mkdir(parents=True, exist_ok=True)

    # collect the raw server-generated data
    LOG.info(f"Storing raw data under: {raw_path}")
    java_cmd = f"java -cp {jar_path} net.minecraft.data.Main --server --reports"
    LOG.info(f"Invoking server's data generator with: {java_cmd}")
    LOG.info("-" * 80)
    java_proc = subprocess.Popen(java_cmd.split(), cwd=raw_path)
    java_result = java_proc.wait()
    LOG.info("-" * 80)
    LOG.info(f"Server's data generator completed with result: {java_result}")

    # create a folder for the processed output
    out_path = Path(outpath.format(version=resolved_version)).absolute()
    LOG.info(f"Using directory for output: {out_path}")
    if out_path.exists():
        raise Exception(f"Directory for output already exists at: {out_path}")
    out_path.mkdir(parents=True, exist_ok=True)

    # create context and run processors
    LOG.info("Processing data...")
    ctx = Context(
        input_dir=raw_path / "generated",
        output_dir=out_path,
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
