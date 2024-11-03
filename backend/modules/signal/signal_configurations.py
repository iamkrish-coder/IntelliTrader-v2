# handlers/signal

from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *


class SignalConfigurations:
    def __init__(self, configuration):
        self.configuration = configuration

    def initialize(self):
        return self.manage_configurations()

    def manage_configurations(self):
        try:
            # Initialize Settings
            config = self.configuration
            settings = {}

            # Store non-dict top-level items in main_params
            settings['runtime_params'] = {key: value for key, value in config.items() if not isinstance(value, dict)}

            if config['global_trade']:
                settings['global_params'] = config['global_trade_params']

            # Retrieve strategy params dynamically (assuming strategy_id exists)
            strategy_id = self.configuration.get("strategy")
            strategy_param_key = f"strategy_{strategy_id}_params"
            settings['strategy_params'] = config.get(strategy_param_key)

            return settings

        except Exception as error:
            log_info(f"An error occurred retrieving Application Settings: {error}")
            return None
