# file with custom exceptions


class BotException(Exception):
    """Base Exception class for all user defined Exceptions for this bot."""

    def __init__(self, message: str):
        self.message: str = message

    def __str__(self) -> str:
        return "{}: {}".format(type(self), self.message)


class FirstAttachmentNotCSVError(BotException):
    """Error for first attachment of message is not a csv file with utf-8 formatting."""

    def __init__(self):
        super().__init__(message="First attachment of message used for command wasn't a csv with utf-8 charset.")


class IncorrectCSVFormatError(BotException):
    """Exception for csv size is not expected."""

    def __init__(self, message: str):
        super().__init__(message=message)
