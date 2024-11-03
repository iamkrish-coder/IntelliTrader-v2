# Standard library imports
import asyncio
import webbrowser

# Third-party library imports

# Custom application modules
from backend.configurations.configuration import Configuration
from backend.modules.BaseModules import BaseModules
from backend.modules.helper.helper_module import Helper
from backend.modules.restore.factory_reset import FactoryReset
from backend.modules.connection.connection_module import Connection
from backend.controllers.database_controller import DatabaseController
from backend.controllers.cloud_controller import CloudController
from backend.controllers.BaseController import BaseController
from backend.controllers.strategy_controller import StrategyController
from backend.controllers.signal_controller import SignalController
from backend.controllers.trade_controller import TradeController

# utils Import
from backend.utils.logging_utils import *

class Algo:
    def __init__(self):
        self.strategy_controller_instance = None
        self.signal_controller_instance = None
        self.trade_controller_instance = None
        self.scheduler_instance = None
        self.cancelled = False
        self.initialize_logging()
        self.app_configuration = Configuration().read_app_configuration()
        self.table_configuration = Configuration().read_table_configuration()
        self.database = DatabaseController(self.table_configuration)
        self.connection = Connection().connect_to_broker()
        self.modules = BaseModules(self.connection).get_all_modules()
        self.components = self.initialize_components()
        self.cloud = CloudController(self.components)

    def get_configuration(self):
        return self.app_configuration

    def initialize_logging(self):
        """Prepares logging for the application."""
        Helper().create_output_directory()
        configure_logging()

    def initialize_components(self):
        """Establishes connection, initializes modules and configuration."""
        try:
            if self.app_configuration is not None and self.table_configuration is not None:
                return BaseController(self.connection, self.modules, self.app_configuration, self.database)
            else:
                log_error("Incomplete configuration: App or Table configuration is missing. Please verify the setup...")
        except Exception as error:
            log_error(f"Failed to initialize components: {error}")

        return None


    ###########################################
    ###########################################
    #            MODULE PRE-REQUISITES        #
    ###########################################
    ###########################################

    def initialize_module_prerequisites(self):
        # Restore Factory Settings if Reset App is requested
        reset_application = self.app_configuration.get("reset_app")
        if reset_application is True:
            factory_reset_object = FactoryReset(self.cloud, self.database)
            factory_reset_object.initialize()

        # Establishes Database Connection
        if not self.database.initialize():
            return False

        # Establishes Module Prerequisites
        if not self.cloud.initialize():
            return False

        return True

    #################################################
    #################################################
    #                RUN ALWAYS ON                  #
    #################################################
    #################################################

    async def autorun(self):

        if self.components is not None:
            try:
                """Initialize database connection and module prerequisites"""
                if not self.initialize_module_prerequisites():
                    log_error(f"Application failed to initialize required modules. Please check the setup.")
                    return False
                else:
                    """Initialize controllers only if all module initialization succeeded"""
                    self.strategy_controller_instance = StrategyController(self.components)
                    self.signal_controller_instance = SignalController(self.components)
                    self.trade_controller_instance = TradeController(self.components)

                    # Concurrent Run
                    tasks = [
                        self.strategy_controller(),
                        self.signal_controller(),
                        self.trade_controller()
                    ]
                    await asyncio.gather(*tasks)
            except Exception as error:
                log_error(f"Error running autorun: {error}")
                return False
        else:
            log_error(f"Application failed to initialize controller. Please check the setup.")
            return False


    ###########################################
    ###########################################
    #            STRATEGY CONTROLLER          #
    ###########################################
    ###########################################

    async def strategy_controller(self):
        """Starts the scanning process for watchlist stocks."""
        await self.strategy_controller_instance.initialize()  # FOR TESTING

        # Instantiate the Scheduler Instance
        # scheduler_instance = Scheduler(self.configuration, strategy_controller_instance, None, ASYNCIO)

        # # Start Scheduler
        # scheduler_instance.start_scheduler()
        # await asyncio.sleep(6000)

    ###########################################
    ###########################################
    #            SIGNAL CONTROLLER            #
    ###########################################
    ###########################################

    async def signal_controller(self):
        """Processes any generated alerts from the scanner."""
        await self.signal_controller_instance.initialize()

        # Instantiate the Scheduler Instance
        # scheduler_instance = Scheduler(self.configuration, signal_controller_instance, None, ASYNCIO)

        # # Start Scheduler
        # scheduler_instance.start_scheduler()
        # await asyncio.sleep(6000)

    ###########################################
    ###########################################
    #             TRADE CONTROLLER            #
    ###########################################
    ###########################################

    async def trade_controller(self):
        """Processes trade signals and executes trade"""
        await self.trade_controller_instance.initialize()

        # Instantiate the Scheduler Instance
        # scheduler_instance = Scheduler(self.configuration, trade_controller_instance, None, ASYNCIO)

        # # Start Scheduler
        # scheduler_instance.start_scheduler()
        # await asyncio.sleep(6000)

if __name__ == "__main__":
    try:
        application = Algo()
        asyncio.run(application.autorun())
    except Exception as error:
        print(f"error: {str(error)}")














    """ DEPRECATED METHODS """

    # Approach 1: Threading

    """
    
    # Start strategy in a separate thread
    strategy_thread = threading.Thread(target=trader.initialize_strategy_controller)
    strategy_thread.start()

    # Start signal in a separate thread
    strategy_thread = threading.Thread(target=trader.initialize_signal_processor_controller)
    strategy_thread.start()
    
    # Start monitoring in a separate thread
    strategy_thread = threading.Thread(target=trader.initialize_trade_execution_controller)
    strategy_thread.start()
    
    """

    # Approach 2: Multiprocessing

    """
    
    process1 = Process(target=trader.initialize_strategy_controller)
    process1.start()

    process2 = Process(target=trader.initialize_signal_controller)
    process2.start()

    process3 = Process(target=trader.initialize_trade_execution_controller)
    process3.start()

    """
