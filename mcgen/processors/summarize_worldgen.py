import logging
from pathlib import Path

from mcgen.context import Context
from mcgen.utils import summarize_registry

LOG = logging.getLogger(__name__)


def process(ctx: Context, **options):
    """Create a summary of worldgen reports."""

    worldgen_path = Path("reports/worldgen/minecraft")
    LOG.info(f"Summarizing worldgen at: {worldgen_path}")

    # TODO Scan for registries automatically. #enhance

    worldgen_summary = {}

    # dimension
    worldgen_summary["dimension"] = summarize_registry(ctx, worldgen_path / "dimension")

    # dimension_type
    worldgen_summary["dimension_type"] = summarize_registry(
        ctx, worldgen_path / "dimension_type"
    )

    # worldgen/biome
    worldgen_summary["worldgen/biome"] = summarize_registry(
        ctx, worldgen_path / "worldgen/biome"
    )

    # worldgen/configured_carver
    worldgen_summary["worldgen/configured_carver"] = summarize_registry(
        ctx, worldgen_path / "worldgen/configured_carver"
    )

    # worldgen/configured_feature
    worldgen_summary["worldgen/configured_feature"] = summarize_registry(
        ctx, worldgen_path / "worldgen/configured_feature"
    )

    # worldgen/configured_structure_feature
    worldgen_summary["worldgen/configured_structure_feature"] = summarize_registry(
        ctx, worldgen_path / "worldgen/configured_structure_feature"
    )

    # worldgen/noise
    worldgen_summary["worldgen/noise"] = summarize_registry(
        ctx, worldgen_path / "worldgen/noise"
    )

    # worldgen/noise_settings
    worldgen_summary["worldgen/noise_settings"] = summarize_registry(
        ctx, worldgen_path / "worldgen/noise_settings"
    )

    # worldgen/placed_feature
    worldgen_summary["worldgen/placed_feature"] = summarize_registry(
        ctx, worldgen_path / "worldgen/placed_feature"
    )

    # worldgen/processor_list
    worldgen_summary["worldgen/processor_list"] = summarize_registry(
        ctx, worldgen_path / "worldgen/processor_list"
    )

    # worldgen/template_pool
    worldgen_summary["worldgen/template_pool"] = summarize_registry(
        ctx, worldgen_path / "worldgen/template_pool"
    )

    ctx.write_json_node(worldgen_summary, worldgen_path)
    ctx.write_min_json_node(worldgen_summary, worldgen_path)
