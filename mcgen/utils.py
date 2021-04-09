import logging
from pathlib import Path
from typing import List

from mcgen.context import Context

LOG = logging.getLogger(__name__)


def summarize_registry(
    ctx: Context,
    registry_location: str,
    namespace: str = "minecraft",
) -> List[str]:
    LOG.debug(f"Summarizing registry at: {registry_location}")
    registry_indir = ctx.input_dir / registry_location
    unsorted_ids = []
    for dirpath, dirnames, filenames in ctx.walk(registry_indir):
        dirpath_path = Path(dirpath)
        for filename in filenames:
            filepath = dirpath_path / filename
            resource_name = filepath.relative_to(registry_indir).with_suffix("")
            resource_id = f"{namespace}:{resource_name}"
            unsorted_ids.append(resource_id)
    sorted_ids = sorted(unsorted_ids)
    summary = {"values": sorted_ids}
    ctx.write_values(sorted_ids, registry_location)
    ctx.write_data(summary, registry_location)
    return sorted_ids
