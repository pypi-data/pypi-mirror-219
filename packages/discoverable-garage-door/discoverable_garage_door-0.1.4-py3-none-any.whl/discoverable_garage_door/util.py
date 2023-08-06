import os
import logging
import logging.config

logger = None
if os.path.isfile("logging.conf"):
    logging_file = "logging.conf"
else:
    path = os.path.dirname(__file__)
    logging_file = f"{path}/logging.conf"
module_name = __name__.split(".")[0]
logging.config.fileConfig(logging_file)
logger = logging.getLogger(module_name)
