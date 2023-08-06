class CarbonateException(Exception):
    pass

class ApiException(CarbonateException):
    pass

class BrowserException(CarbonateException):
    pass

class FailedExtractionException(CarbonateException):
    pass

class InvalidXpathException(CarbonateException):
    pass

class TestException(CarbonateException):
    pass
