import logging

from mcgen.context import Context
from mcgen.utils import summarize_registry

LOG = logging.getLogger(__name__)


def process(ctx: Context, **options):
    """Create a summary of biome reports."""
    registry_location = "reports/biomes"
    LOG.info(f"Summarizing biomes at: {registry_location}")
    summarize_registry(ctx, registry_location)
