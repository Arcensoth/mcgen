import logging

from mcgen.context import Context

LOG = logging.getLogger(__name__)


def process(
    ctx: Context,
    version_file_location="VERSION.txt",
    **options,
):
    """Write the game version to a file."""
    LOG.info(f"Writing version to: {version_file_location}")
    version_file_path = ctx.output_dir / version_file_location
    with open(version_file_path, "w") as fp:
        fp.write(ctx.version)
