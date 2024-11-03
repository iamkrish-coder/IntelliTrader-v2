from backend.utils.logging_utils import *
from backend.controllers.cloud_controller import CloudController


class FactoryReset:

    def __init__(self, cloud_module, database_module):
        self.cloud_module = cloud_module
        self.database_module = database_module

    ###########################################
    # Initialize Database Module
    ###########################################

    def initialize(self):
        log_info("********* Resetting the application to its factory defaults. Hang tight, we're on it! ********* ")
        self.restore_factory_defaults()

    def restore_factory_defaults(self):

        # Delete Tables | Delete Caches | Delete Configs | Delete Subscriptions | Delete Topics | Delete Queues
        log_info("Removing subscriptions...")
        if not self.cloud_module.delete_subscriptions():
            return False

        log_info("Removing topics...")
        if not self.cloud_module.delete_topics():
            return False

        log_info("Removing queues...")
        if not self.cloud_module.delete_queues():
            return False

        log_info("Removing tables...")
        if not self.database_module.delete_tables():
            return False

        return True
