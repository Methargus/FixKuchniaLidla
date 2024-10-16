from infrastructure.azure_configuration_manager import AzureConfigurationManager

class AzureSqlCommunication():
    def __init__(self):
        self.cursor = AzureConfigurationManager().get_cursor()
    def list_tables(self):
        self.cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';")
        tables = self.cursor.fetchall()
        [print(table[0]) for table in tables]