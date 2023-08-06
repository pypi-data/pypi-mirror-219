class InvalidURLException(Exception):
    def __init__(self, message: str = "URL is not Valid"):
        self.message = message
        super().__init__(message)
