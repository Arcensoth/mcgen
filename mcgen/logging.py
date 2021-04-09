import logging.config

LOG_FORMAT_DETAILED = "%(log_color)s%(asctime)s %(levelname)-8s [%(name)s] %(message)s"

LOG_COLORS = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red,bg_white",
}


def setup_logging(
    level: str = logging.WARNING,
):
    log_handler = logging.StreamHandler()

    try:
        import colorlog

        log_handler.setFormatter(
            colorlog.ColoredFormatter(fmt=LOG_FORMAT_DETAILED, log_colors=LOG_COLORS)
        )

    except:
        pass

    logging.basicConfig(level=level, handlers=[log_handler])
