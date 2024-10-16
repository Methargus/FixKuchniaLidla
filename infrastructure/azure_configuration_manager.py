import pyodbc, struct
from pyodbc import Cursor
from azure.identity import DefaultAzureCredential
from configuration import ConfigurationProvider

class AzureConfigurationManager():
    def __init__(self):
        configuration = ConfigurationProvider.get_config()
        self.connection_string = configuration.get_azure_db_connection_string()
        
    def get_token(self):
        # Get the token using DefaultAzureCredential
        
        # credential = DefaultAzureCredential()
        credential = DefaultAzureCredential(exclude_interactive_browser_credential=False, interactive_browser_tenant_id="f1c78b4e-52ac-4353-87ee-5fcfdef2b4b1")
        token = credential.get_token("https://database.windows.net/.default")

        token_bytes = token.token.encode("UTF-16-LE")

        # Extract the token value
        token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        return token_struct #todo: check if above boilerplate is needed

    def get_cursor(self) -> Cursor:
        return pyodbc.connect(self.connection_string, attrs_before={1256: self.get_token()}).cursor()