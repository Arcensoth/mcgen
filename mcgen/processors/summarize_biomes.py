import logging
from pathlib import Path

from mcgen.context import Context
from mcgen.utils import summarize_registry

LOG = logging.getLogger(__name__)


def process(ctx: Context, **options):
    """Create a summary of biome reports."""
    biomes_path = Path("reports/biomes")
    LOG.info(f"Summarizing biomes at: {biomes_path}")
    summarize_registry(ctx, biomes_path)
