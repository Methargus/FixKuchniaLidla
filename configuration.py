import json
import os

class ConfigurationProvider:
    _config = None

    @staticmethod
    def get_config():
        if(ConfigurationProvider._config == None):
            ConfigurationProvider._config = Configuration()

        return ConfigurationProvider._config
    
class Configuration:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "configuration.json")
    
        with open(config_path, "r") as file:
            self.config = json.load(file)

    def get_azure_db_connection_string(self):
        return self.config["ConnectionString"]
    