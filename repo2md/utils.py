import logging
import os

LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(
    fmt=logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s - Line: %(lineno)d - %(message)s",
        datefmt="%b-%d-%Y %H:%M:%S",
    )
)
if os.environ.get("DEBUG", "").lower() in ("1", "true"):
    LOGGER.setLevel(level=logging.DEBUG)
else:
    LOGGER.setLevel(level=logging.INFO)
LOGGER.addHandler(hdlr=handler)
