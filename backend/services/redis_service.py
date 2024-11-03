import subprocess
import socket
from backend.utils.logging_utils import *


class RedisServiceController:
    def __init__(self):
        pass

    def start_redis_server(self):
        if not self.is_redis_running():
            try:
                subprocess.run(['wsl', 'sudo', 'service', 'redis-server', 'start'], check=True)
                log_info("Redis server started successfully.")
            except subprocess.CalledProcessError as error:
                log_error(f"Error starting Redis server: {error}")
        else:
            log_info("Redis server is already running.")

    @staticmethod
    def stop_redis_server():
        try:
            # Execute the command to stop the Redis server in WSL
            subprocess.run(['wsl', 'sudo', 'service', 'redis-server', 'stop'], check=True)
            log_info("Redis server stopped successfully.")
        except subprocess.CalledProcessError as error:
            log_error(f"Error stopping Redis server: {error}")

    @staticmethod
    def is_redis_running():
        # Attempt to connect to the Redis server's default port
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Set a timeout for the connection attempt
                s.connect(('localhost', 6379))
                return True
        except (ConnectionRefusedError, socket.timeout):
            return False
