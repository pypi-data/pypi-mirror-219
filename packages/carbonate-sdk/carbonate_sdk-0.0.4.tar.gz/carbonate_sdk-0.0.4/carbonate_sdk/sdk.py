import os
import json
from distutils.util import strtobool
from time import sleep
from typing import List, Callable, Optional, IO
from .browser import Browser
from .api import Api
from .exceptions import FailedExtractionException, InvalidXpathException, BrowserException, TestException
from .logger import Logger
from .slugify import slugify
from .test_logger import TestLogger
import logging as python_logging

class SDK:
    def __init__(
            self,
            browser: Browser,
            cache_dir: str = None,
            api_user_id: str = None,
            api_key: str = None,
            logging = None,
            client: Optional[Api] = None,
    ):
        self.browser = browser
        self.client = client or Api(api_user_id, api_key)
        self.test_prefix = None
        self.test_name = None
        self.cache_dir = cache_dir or os.environ.get('CARBONATE_CACHE_DIR')
        self.network_whitelist = []
        self.instruction_cache = {}

        # Log to exception - default
        if logging is None:
            self.logger = TestLogger()
        # Path to file or IO object
        elif isinstance(logging, str) or isinstance(logging, IO):
            self.logger = TestLogger(logging, False)
        # Custom logger
        else:
            self.logger = logging

    def get_test_name(self):
        if self.test_prefix:
            return self.test_prefix + ': ' + self.test_name

        return self.test_name

    def wait_for_load(self, skip_func: Callable):
        i = 0

        while self.browser.evaluate_script('return window.carbonate_dom_updating') or self.browser.evaluate_script('return window.carbonate_active_xhr'):
            if skip_func():
                self.logger.info("Found cached element, skipping DOM wait")
                break

            if self.browser.evaluate_script('return window.carbonate_dom_updating'):
                self.logger.info("Waiting for DOM update to finish")
            else:
                self.logger.info("Waiting for active Network to finish")

            if i > 20:
                raise BrowserException("Waited too long for DOM/XHR update to finish")

            sleep(0.5)
            i += 1

    def get_cache_path(self, instruction):
        return self.cache_dir + '/' + slugify(self.test_name) + '/' + slugify(instruction) + '.json'

    def cached_actions(self, instruction):
        if self.cache_dir is not None and os.path.isfile(self.get_cache_path(instruction)):
            # Open the file as parse the json
            with open(self.get_cache_path(instruction), 'r') as f:
                actions = json.load(f)
                self.logger.debug("Using locally cached actions", {'actions': actions})
                return actions

        return []

    def extract_actions(self, instruction):
        actions = self.client.extract_actions(self.get_test_name(), instruction, self.browser.get_html())

        if len(actions) > 0:
            self.logger.info("Successfully extracted actions", {'actions': actions})
            self.cache_instruction(actions, instruction)

            return actions

        raise FailedExtractionException('Could not extract actions')

    def cache_instruction(self, result, instruction):
        if self.cache_dir is not None:
            self.instruction_cache[instruction] = result

    def write_cache(self) -> None:
        if self.cache_dir is None:
            raise Exception("Cannot call write_cache without setting cache_dir")

        if self.test_name is None:
            raise Exception("Test name not set, please call start_Test first")

        if len(self.instruction_cache) == 0:
            return

        # Create the cache directory if it doesn't exist
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        # Create the test name directory if it doesn't exist
        if not os.path.exists(self.cache_dir + '/' + slugify(self.test_name)):
            os.makedirs(self.cache_dir + '/' + slugify(self.test_name))

        for instruction, result in self.instruction_cache.items():
            # Write the actions to a file
            with open(self.get_cache_path(instruction), 'w') as f:
                json.dump(result, f)

        self.instruction_cache = []

    def cached_assertions(self, instruction):
        if self.cache_dir is not None and os.path.isfile(self.get_cache_path(instruction)):
            # Open the file as parse the json
            with open(self.get_cache_path(instruction), 'r') as f:
                actions = json.load(f)
                self.logger.debug("Using locally cached assertions", {'actions': actions})
                return actions

        return []

    def extract_assertions(self, instruction):
        assertions = self.client.extract_assertions(self.get_test_name(), instruction, self.browser.get_html())

        if len(assertions) > 0:
            self.logger.info("Successfully extracted assertions", {'assertions': assertions})
            self.cache_instruction(assertions, instruction)

            return assertions

        raise FailedExtractionException('Could not extract assertions')

    def action(self, instruction):
        self.logger.info("Querying action", {'test_name': self.get_test_name(), 'instruction': instruction})
        actions = self.cached_actions(instruction)

        is_action_ready = lambda action: len(self.browser.find_by_xpath(action['xpath'])) > 0
        self.wait_for_load(lambda: len(actions) > 0 and all(map(is_action_ready, actions)))

        if len(actions) == 0:
            self.logger.notice("No actions found, extracting from page")
            actions = self.extract_actions(instruction)

        self.perform_actions(actions)

    def perform_actions(self, actions):
        previous_actions = []
        for action in actions:
            self.logger.notice("Performing action", {'action': action})
            elements = self.browser.find_by_xpath(action['xpath'])

            if len(elements) == 0:
                raise InvalidXpathException("Could not find element for xpath: " + action['xpath'])

            if len(elements) > 1:
                self.logger.warning(
                    "More than one element found for xpath",
                    {'num': len(elements), 'xpath': action['xpath']}
                )
                return previous_actions

            self.browser.perform_action(action, elements)
            previous_actions.append(action)

        return previous_actions

    def assertion(self, instruction):
        self.logger.info("Querying assertion", {'test_name': self.get_test_name(), 'instruction': instruction})

        assertions = self.cached_assertions(instruction)

        self.wait_for_load(lambda: len(assertions) > 0 and all(map(self.is_assertion_ready, assertions)))

        if len(assertions) == 0:
            self.logger.notice("No assertions found, extracting from page")
            assertions = self.extract_assertions(instruction)

        return self.perform_assertions(assertions)

    def perform_assertions(self, assertions: List) -> bool:
        for assertion in assertions:
            result = self.perform_assertion(assertion)

            if not result:
                return False

        return True

    def is_assertion_ready(self, assertion):
        try:
            self.perform_assertion(assertion)
            return True
        except BrowserException as e:
            return False

    def perform_assertion(self, assertion):
        self.logger.notice("Performing assertion", {'assertion': assertion['assertion']})

        return self.browser.evaluate_script('window.carbonate_reset_assertion_result(); (function() { ' + assertion['assertion'] + ' })(); return window.carbonate_assertion_result;')

    def cached_lookup(self, instruction):
        if self.cache_dir is not None and os.path.isfile(self.get_cache_path(instruction)):
            # Open the file as parse the json
            with open(self.get_cache_path(instruction), 'r') as f:
                lookup = json.load(f)
                self.logger.debug("Using locally cached lookup", {'lookup': lookup})
                return lookup

        return None

    def extract_lookup(self, instruction):
        lookup = self.client.extract_lookup(self.get_test_name(), instruction, self.browser.get_html())

        if lookup is not None:
            self.logger.info("Successfully extracted lookup", {'lookup': lookup})
            self.cache_instruction(lookup, instruction)

            return lookup

        raise FailedExtractionException('Could not extract lookup')

    def lookup(self, instruction):
        self.logger.info("Querying lookup", {'test_name': self.get_test_name(), 'instruction': instruction})
        element = self.cached_lookup(instruction)

        self.wait_for_load(lambda: element is not None and len(self.browser.find_by_xpath(element['xpath'])) > 0)

        if element is None:
            self.logger.notice("No elements found, extracting from page")
            element = self.extract_lookup(instruction)

        elements = self.browser.find_by_xpath(element['xpath'])

        if len(elements) == 0:
            raise InvalidXpathException("Could not find element for xpath: " + element['xpath'])

        return elements[0]

    def start_test(self, test_prefix, test_name):
        if len(self.instruction_cache.keys()) > 0:
            raise Exception("Instruction cache not empty, did you forget to call end_test()?")

        if hasattr(self.logger, 'clear_logs'):
            self.logger.clear_logs()

        self.test_prefix = test_prefix
        self.test_name = test_name

    def end_test(self):
        if self.cache_dir is not None:
            self.write_cache()

    def load(self, url):
        self.logger.info("Loading page", {'url': url, 'whitelist': self.network_whitelist})
        self.browser.load(url, self.network_whitelist)

    def close(self):
        self.logger.info("Closing browser")
        self.browser.close()

    def whitelist_network(self, url):
        self.network_whitelist.append(url)

    def handle_failed_test(self, e):
        self.instruction_cache = []

        if hasattr(self.logger, 'get_logs'):
            raise TestException(self.logger.get_logs()) from e

        raise e

    def get_logger(self) -> Logger:
        return self.logger

    def get_browser(self) -> Browser:
        return self.browser