import json
import logging
from pathlib import Path

from mcgen.context import Context

LOG = logging.getLogger(__name__)


def process(ctx: Context, **options):
    """Split `registries.json` into separate files."""

    # load registries.json
    registries_inpath = ctx.input_dir / "reports/registries.json"
    LOG.info(f"Splitting registries at: {registries_inpath}")
    with open(registries_inpath) as fp:
        registries_data = json.load(fp)

    # split each registry into its own set of files
    registries_path = Path("reports/registries")
    for reg_name, registry in registries_data.items():
        reg_entries = registry["entries"]
        LOG.debug(f"Found {len(reg_entries)} entries for registry: {reg_name}")
        reg_shortname = reg_name.split(":")[1]
        reg_node_path = registries_path / reg_shortname
        values = sorted(list(reg_entries.keys()))
        data = {"values": values}
        ctx.write_values_txt_node(values, reg_node_path)
        ctx.write_json_node(data, reg_node_path)
        ctx.write_min_json_node(data, reg_node_path)
