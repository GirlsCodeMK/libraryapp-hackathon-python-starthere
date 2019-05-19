from .api_views import *
from .web_views import *

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# create the logging file handler
fh = logging.FileHandler("library.views.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)


# Use by calling 
# logger.warning('some message that is all one string')