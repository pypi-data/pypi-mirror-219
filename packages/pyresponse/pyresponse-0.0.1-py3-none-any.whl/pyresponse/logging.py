"""
Logging module for PyResponse package.
"""

import logging
import rollbar
import sentry_sdk
from config import SENTRY_DSN, ROLLBAR_ACCESS_TOKEN, ROLLBAR_ENVIRONMENT


def configure_logging():
    """
    Configure logging for PyResponse package.

    This function initializes the Rollbar and Sentry logging handlers
    and sets up the logger for the package.
    """
    rollbar.init(ROLLBAR_ACCESS_TOKEN, environment=ROLLBAR_ENVIRONMENT)
    rollbar_handler = rollbar.LogHandler()
    rollbar_handler.setLevel(logging.ERROR)

    sentry_sdk.init(dsn=SENTRY_DSN)
    sentry_handler = sentry_sdk.integrations.logging.EventHandler()
    sentry_handler.setLevel(logging.ERROR)

    logger = logging.getLogger(__name__)
    logger.addHandler(rollbar_handler)
    logger.addHandler(sentry_handler)
