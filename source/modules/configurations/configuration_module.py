# source/modules/configurations/configuration_module.py

import json
import os

from source.constants.constants import *
from source.enumerations.enums import *

class Configuration: 
    def __init__(self):
     pass
    
    @classmethod
    def read_app_configuration(self):
        with open(CONFIGURATION_PATH + '/' + APP_CONFIGURATION_FILE, 'r') as f:
            app_config = json.load(f)
        return app_config
    

    @classmethod
    def read_table_configuration(self):
        with open(CONFIGURATION_PATH + '/' + TABLE_CONFIGURATION_FILE, 'r') as f:
            table_config = json.load(f)
        return table_config   