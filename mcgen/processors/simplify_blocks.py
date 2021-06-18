import json
import logging

from mcgen.context import Context

LOG = logging.getLogger(__name__)


def process(ctx: Context, **options):
    """Create a simplified version of `blocks.json`."""

    blocks_location = "reports/blocks.json"
    LOG.info(f"Simplifying blocks at: {blocks_location}")

    # load blocks.json
    blocks_inpath = ctx.input_dir / blocks_location
    with open(blocks_inpath) as fp:
        blocks_data = json.load(fp)

    # summarize block and block state data
    data = {}
    for block_name, block_data in blocks_data.items():
        data[block_name] = {
            "properties": block_data.get("properties", {}),
            "default": next(
                filter(lambda s: s.get("default", False), block_data["states"])
            ).get("properties", {}),
        }

    # write the simplified blocks file
    simplified_blocks_root = "reports/blocks/simplified"
    ctx.write_data(data, simplified_blocks_root)
