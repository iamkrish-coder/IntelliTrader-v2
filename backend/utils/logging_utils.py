# backend/shared/logging_utils.py
import inspect
import logging
import colorlog
import os
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.enumerations.resource_string_enums import INFO, ERROR, WARN
from backend.language.resources_EN_IN import ResourceStrings


def configure_logging():
    """Configures logging with a console handler (optional)."""

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Colored console handler with additional configuration (optional)
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = colorlog.ColoredFormatter('%(log_color)s%(asctime)s  %(levelname)-8s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler with customizable log level and formatter
    file_handler = logging.FileHandler(os.path.join(OUTPUT_PATH, 'intelliTrader.log'))
    file_handler.setLevel(logging.ERROR)  # Adjust logging level as needed
    plain_formatter = logging.Formatter('%(asctime)s  %(levelname)-8s : %(message)s')
    file_handler.setFormatter(plain_formatter)
    root_logger.addHandler(file_handler)

def log_message(level, message, filename, *args, **kwargs):
    """
    Logs a message with the specified level.

    Args:
    message: An enumeration value representing the message key.
    level: The logging level (e.g., logging.INFO, logging.ERROR).
    *args: Positional arguments for message formatting.
    **kwargs: Keyword arguments for message formatting.
    """
    formatted_message = ResourceStrings.get(message)
    if not formatted_message:
        formatted_message = message
    if kwargs:
        formatted_message = formatted_message.format(**kwargs)
    elif args:
        if "%" in formatted_message:
            formatted_message = formatted_message % args
        else:
            formatted_message = formatted_message.format(*args)
    else:
        formatted_message = get_message(message)

    logger = logging.getLogger("uvicorn")
    if level == 40:
        logger.log(level, f"{filename}: {formatted_message}")
    else:
        logger.log(level, formatted_message)

def get_message(resource_string):
    """Retrieves message from ResourceStrings or returns the input string if not found.

    Args:
        resource_string (str | backend.enumerations.messages.Info_Messages |
                          backend.enumerations.messages.Error_Messages |
                          backend.enumerations.messages.Warning_Messages):
            The enum member representing the message you want to retrieve or a custom string message.

    Returns:
        str: The message string (either from ResourceStrings or the input string).
    """

    if isinstance(resource_string, (INFO, ERROR, WARN)):
        message = ResourceStrings.get(resource_string)
        return message or resource_string.value
    else:
        # logging.warning(f"get_message received a non-enum string: {resource_string}")
        return resource_string

def log_info(message, *args, **kwargs):
    """Logs a message with INFO level."""
    frame = inspect.stack()[1]
    filename = frame.filename
    log_message(logging.INFO, message, filename, *args, **kwargs)


def log_error(message, *args, **kwargs):
    """Logs a message with ERROR level."""
    frame = inspect.stack()[1]
    filename = frame.filename
    log_message(logging.ERROR, message, filename, *args, **kwargs)


def log_warn(message, *args, **kwargs):
    """Logs a message with WARNING level."""
    frame = inspect.stack()[1]
    filename = frame.filename
    log_message(logging.WARNING, message, filename, *args, **kwargs)