class MandatoryArgsNotFilled(Exception):
    """Exception raised for errors in the request args. This method expects to be fulfilled all the mandatory params."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ContentTypeNotSupported(Exception):
    """Exception raised for errors in the body request type. The request's body should be formatted as a JSON."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
