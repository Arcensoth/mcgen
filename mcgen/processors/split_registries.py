import json
import logging

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
    registries_location = "reports/registries"
    for reg_name, registry in registries_data.items():
        reg_entries = registry["entries"]
        LOG.debug(f"Found {len(reg_entries)} entries for registry: {reg_name}")
        reg_shortname = reg_name.split(":")[1]
        reg_location = f"{registries_location}/{reg_shortname}"
        values = sorted(list(reg_entries.keys()))
        data = {"values": values}
        ctx.write_values(values, reg_location)
        ctx.write_data(data, reg_location)
