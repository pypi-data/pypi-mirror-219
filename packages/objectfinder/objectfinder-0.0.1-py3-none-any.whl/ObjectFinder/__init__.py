# __init__.py

import logging
import ObjectFinder
import setup

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.info('Initializing Object Finder')


# This will log 'Initializing Object Finder'