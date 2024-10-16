from infrastructure.azure_sql_communication import AzureSqlCommunication


if __name__ == "__main__":
    a = AzureSqlCommunication()
    a.list_tables()