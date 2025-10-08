class DataScienceException(Exception):
    pass

class DatabaseConnectionException(DataScienceException):
    pass

class SQLGenerationException(DataScienceException):
    pass

class ModelExecutionException(DataScienceException):
    pass

class ConfigurationException(DataScienceException):
    pass