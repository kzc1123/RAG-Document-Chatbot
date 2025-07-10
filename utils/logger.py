import logging
import os

level = os.environ.get("LOGLEVEL", "INFO").upper()
logger = logging.Logger(name="rag_app", level=level)