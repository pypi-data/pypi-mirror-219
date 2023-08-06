import os
import json
from selenium.common import ElementNotInteractableException
from selenium.common.exceptions import JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

try:
    import importlib.resources as pkg_resources
    if not hasattr(pkg_resources, 'files'):
        raise ImportError
except ImportError:
    import importlib_resources as pkg_resources

from .browser import Browser
from .action import Action
from .exceptions import BrowserException

class WebDriver(Browser):
    def __init__(self, driver):
        self.browser = driver
        inject_js_resource = pkg_resources.files('carbonate_sdk.resources') / "carbonate.js"
        with inject_js_resource.open("r") as file:
            self.inject_js = file.read()

    def get_html(self):
        return self.browser.execute_script("return document.documentElement.innerHTML")

    def load(self, url, whitelist=None):
        if self.evaluate_script('return typeof window.carbonate_dom_updating === "undefined"'):
            self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': self.inject_js})

        self.browser.get(url)
        self.evaluate_script('window.carbonate_set_xhr_whitelist(' + json.dumps(whitelist) + ')')

    def close(self):
        self.browser.quit()

    def find_by_xpath(self, xpath):
        return self.browser.find_elements(By.XPATH, xpath)

    def find_by_id(self, id):
        return self.browser.find_elements(By.ID, id)

    def evaluate_script(self, script):
        try:
            return self.browser.execute_script(script)
        except JavascriptException as e:
            raise BrowserException("Could not evaluate script: " + script) from e

    def perform_action(self, action, elements):
        if action["action"] == Action.CLICK.value:
            try:
                elements[0].click()
            except ElementNotInteractableException:
                ActionChains(self.browser).move_to_element(elements[0]).click().perform()

        elif action["action"] == Action.TYPE.value:
            nonTypeable = ['date', 'datetime-local', 'month', 'time', 'week', 'color', 'range']
            if elements[0].tag_name == "input" and elements[0].get_attribute("type") in nonTypeable:
                # Not ideal but filling via the UI is not currently possible
                self.browser.execute_script(
                    "arguments[0].value = arguments[1];" +
                    # Trigger onchange manually
                    "arguments[0].dispatchEvent(new Event('change'), {bubbles: true});",
                    elements[0], action["text"]
                )

                return

            if elements[0].tag_name == "label":
                elements = self.find_by_id(elements[0].get_attribute("for"))

            elements[0].send_keys(action["text"])
            self.evaluate_script('!!document.activeElement ? document.activeElement.blur() : 0')
        elif action["action"] == Action.KEY.value:
            elements[0].send_keys(action["key"])
