from abc import abstractmethod, ABCMeta

class Logger(metaclass=ABCMeta):
    @abstractmethod
    def emergency(self, message, context=None):
        pass

    @abstractmethod
    def alert(self, message, context=None):
        pass

    @abstractmethod
    def critical(self, message, context=None):
        pass

    @abstractmethod
    def error(self, message, context=None):
        pass

    @abstractmethod
    def warning(self, message, context=None):
        pass

    @abstractmethod
    def notice(self, message, context=None):
        pass

    @abstractmethod
    def info(self, message, context=None):
        pass

    @abstractmethod
    def debug(self, message, context=None):
        pass
