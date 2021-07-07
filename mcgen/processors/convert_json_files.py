import json
import logging
from pathlib import Path

from mcgen.context import Context

LOG = logging.getLogger(__name__)


def process(ctx: Context, **options):
    """Convert json files into another form."""

    LOG.info("Converting json files...")

    # convert every file we encounter into multiple forms
    for dirpath, dirnames, filenames in ctx.walk(ctx.input_dir):
        sub_indir = Path(dirpath)
        # determine the corresponding path to the output directory
        sub_reldir = sub_indir.relative_to(ctx.input_dir)
        LOG.debug(f"Converting json files at: {sub_reldir}")
        # process each file
        for filename in filenames:
            if filename.endswith(".json"):
                file_inpath = sub_indir / filename
                with open(file_inpath) as fp:
                    file_data = json.load(fp)
                node_path = (sub_reldir / filename).with_suffix("")
                ctx.write_json_node(file_data, node_path)
                ctx.write_min_json_node(file_data, node_path)
