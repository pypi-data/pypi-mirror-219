import json
from abc import ABCMeta, abstractmethod

class Browser(metaclass=ABCMeta):
    @abstractmethod
    def get_html(self):
        pass

    @abstractmethod
    def load(self, url, whitelist=None):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def find_by_xpath(self, xpath):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def evaluate_script(self, script):
        pass

    @abstractmethod
    def perform_action(self, action, elements):
        pass