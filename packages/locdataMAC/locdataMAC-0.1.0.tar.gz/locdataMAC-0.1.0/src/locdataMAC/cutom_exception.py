class InvalidOSException(Exception):
    def __init__(self, message: str = "Either Linux or Windows system found!"):
        self.message = message
        super().__init__(self.message)

class InvalidpathException(Exception):
    def __init__(self, message: str = "filepath is invalid"):
        self.message = message
        super().__init__(self.message)