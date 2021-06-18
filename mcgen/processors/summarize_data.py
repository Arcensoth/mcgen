import logging

from mcgen.context import Context
from mcgen.utils import summarize_registry

LOG = logging.getLogger(__name__)


def process(ctx: Context, **options):
    """Create a summary of each vanilla registry."""

    data_location = "data/minecraft"
    LOG.info(f"Summarizing data at: {data_location}")

    # TODO Scan for registries automatically. #enhance

    data_summary = {}

    # advancements
    data_summary["advancements"] = summarize_registry(
        ctx, f"{data_location}/advancements"
    )

    # loot tables
    data_summary["loot_tables"] = summarize_registry(
        ctx, f"{data_location}/loot_tables"
    )

    # recipes
    data_summary["recipes"] = summarize_registry(ctx, f"{data_location}/recipes")

    # tags
    data_summary["tags"] = {}
    data_summary["tags"]["blocks"] = summarize_registry(
        ctx, f"{data_location}/tags/blocks"
    )
    data_summary["tags"]["entity_types"] = summarize_registry(
        ctx, f"{data_location}/tags/entity_types"
    )
    data_summary["tags"]["fluids"] = summarize_registry(
        ctx, f"{data_location}/tags/fluids"
    )
    data_summary["tags"]["game_events"] = summarize_registry(
        ctx, f"{data_location}/tags/game_events"
    )
    data_summary["tags"]["items"] = summarize_registry(
        ctx, f"{data_location}/tags/items"
    )

    ctx.write_data(data_summary, data_location)
