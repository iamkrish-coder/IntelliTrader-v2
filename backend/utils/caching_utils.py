import shutil
import datetime
from diskcache import Cache
from backend.constants.const import CACHE_PATH
from backend.utils.logging_utils import *


def generate_cache_key():
    """
    Generates a unique cache key based on the input.

    # You'll need to fill in the logic to generate the key here
    # (e.g., return f"{exchange}:{symbol}:{timeframe}")
    """
    pass


def get_cache_path(cache_directory, cache_sub_directory=None):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    # Construct the cache path with subfolder
    if cache_sub_directory:
        cache_path = os.path.join(CACHE_PATH, formatted_date, cache_directory, cache_sub_directory)
    else:
        cache_path = os.path.join(CACHE_PATH, formatted_date, cache_directory)
    return cache_path


def create_cache_path(cache_path):
    # Create the cache directory if it doesn't exist
    if not os.path.exists(cache_path):
        try:
            os.makedirs(cache_path, exist_ok=True)
        except OSError as error:
            log_error(f"Error creating cache directory: {error}")


def clear_cache(cache_name, cache_directory=None):
    if cache_directory:
        cache_path = get_cache_path(cache_directory)
        disk_cache = Cache(cache_path)

        if cache_name != "disk":
            raise ValueError(f"Invalid cache name: {cache_name}")

        disk_cache.clear()
        try:
            if os.path.isdir(cache_path):
                shutil.rmtree(cache_path)
        except OSError as error:
            log_error(f"Error removing directory {cache_path}: {error}")
    else:
        remove_cache_directories()


def remove_cache(cache_name, cache_directory=None):
    if cache_directory:
        cache_path = get_cache_path(cache_directory)

        try:
            if os.path.isdir(cache_path):
                shutil.rmtree(cache_path)
        except OSError as error:
            log_error(f"Error removing directory {cache_path}: {error}")
    else:
        remove_cache_directories()


def remove_cache_directories():
    # Remove old cache directories
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")

    old_cache_dirs = [os.path.join(CACHE_PATH, directory)
                      for directory in os.listdir(CACHE_PATH)
                      if directory != formatted_date]
    for directory in old_cache_dirs:
        try:
            if os.path.isdir(directory):
                shutil.rmtree(directory)
        except OSError as error:
            log_error(f"Error removing directory {directory}: {error}")


def get_cached_item(cache_name, cache_directory, key):
    """
    This function retrieves an item from the specified cache.

    Args:
        cache_directory:
        cache_name (str): The name of the cache to use (e.g., "topics").
        key (str): The unique key for the cached item.

    Returns:
        object: The cached item or None if not found.
    """
    cache_sub_directory = key
    cache_path = get_cache_path(cache_directory, cache_sub_directory)
    disk_cache = Cache(cache_path)

    if cache_name != "disk":
        raise ValueError(f"Invalid cache name: {cache_name}")

    return disk_cache.get(key)


def set_cached_item(cache_name, cache_directory, key, value):
    """
    This function sets an item in the specified cache with expiration.

    Args:
        cache_directory:
        cache_name (str): The name of the cache to use (e.g., "topics").
        key (str): The unique key for the cached item.
        value (object): The item to be cached.
    """
    cache_sub_directory = key
    cache_path = get_cache_path(cache_directory, cache_sub_directory)
    create_cache_path(cache_path)
    disk_cache = Cache(cache_path)

    if cache_name != "disk":
        raise ValueError(f"Invalid cache name: {cache_name}")

    disk_cache.set(key, value)
