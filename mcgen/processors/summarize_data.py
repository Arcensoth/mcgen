import logging
from pathlib import Path

from mcgen.context import Context
from mcgen.utils import summarize_registry

LOG = logging.getLogger(__name__)


def process(ctx: Context, **options):
    """Create a summary of each vanilla registry."""

    data_path = Path("data/minecraft")
    LOG.info(f"Summarizing data at: {data_path}")

    # TODO Scan for registries automatically. #enhance

    data_summary = {}

    # advancements
    data_summary["advancements"] = summarize_registry(ctx, data_path / "advancements")

    # loot tables
    data_summary["loot_tables"] = summarize_registry(ctx, data_path / "loot_tables")

    # recipes
    data_summary["recipes"] = summarize_registry(ctx, data_path / "recipes")

    # tags
    data_summary["tags"] = {}
    data_summary["tags"]["blocks"] = summarize_registry(ctx, data_path / "tags/blocks")
    data_summary["tags"]["entity_types"] = summarize_registry(
        ctx, data_path / "tags/entity_types"
    )
    data_summary["tags"]["fluids"] = summarize_registry(ctx, data_path / "tags/fluids")
    data_summary["tags"]["game_events"] = summarize_registry(
        ctx, data_path / "tags/game_events"
    )
    data_summary["tags"]["items"] = summarize_registry(ctx, data_path / "tags/items")

    ctx.write_json_node(data_summary, data_path)
    ctx.write_min_json_node(data_summary, data_path)
