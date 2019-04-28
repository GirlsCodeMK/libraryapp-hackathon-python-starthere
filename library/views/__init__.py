from .api_views import *
from .web_views import *

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Use by calling 
# logger.warning('some message that is all one string')