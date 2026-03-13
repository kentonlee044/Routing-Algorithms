class InvalidConfigFileError(Exception):
    """Raised when the configuration file is invalid."""
    def __init__(self, message="Invalid configuration file. Please check the file format and contents."):
        self.message = message
        super().__init__(self.message)