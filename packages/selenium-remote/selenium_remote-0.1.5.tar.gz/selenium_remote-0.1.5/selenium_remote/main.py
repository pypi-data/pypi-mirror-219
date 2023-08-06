"""This is a test."""

import logging

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from urllib3.exceptions import MaxRetryError
from webdriver_manager.chrome import ChromeDriverManager
import json
import requests

logger = logging.getLogger(__name__)


def create_remote_driver(
    selenium_grid_url="http://localhost:4445/wd/hub", fake_user_agent=True, remote=True
):
    """
    Connect to a selennium grid server and create a driver
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument("--disable-gpu")
    if fake_user_agent:
        user_agent = UserAgent()
        user_agent_random = user_agent.random
        # logger.info(f"Generating Fake User Agent. {user_agent_random}")
        chrome_options.add_argument(f"user-agent={user_agent_random}")
    if remote:
        # logger.debug(
        #     "selenium_grid_url: ",", sys.version{selenium_grid_url}")
        try:
            driver = webdriver.Remote(selenium_grid_url, options=chrome_options)
            # logger.debug(f"Got Driver: {driver}")
        except MaxRetryError as error:
            raise ConnectionError("There was an error with the connection.") from error
        return driver
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def clear_sessions(session_id=None, selenium_grid_url="http://selenium:4444"):
    """
    Here we query and delete orphan sessions
    docs: https://www.selenium.dev/documentation/grid/advanced_features/endpoints/
    :return: None
    """
    if not session_id:
        # delete all sessions
        r = requests.get("{}/status".format(selenium_grid_url))
        data = json.loads(r.text)
        for node in data["value"]["nodes"]:
            for slot in node["slots"]:
                if slot["session"]:
                    id = slot["session"]["sessionId"]
                    r = requests.delete("{}/session/{}".format(selenium_grid_url, id))
    else:
        # delete session from params
        r = requests.delete("{}/session/{}".format(selenium_grid_url, session_id))


def main():
    """
    This is a test
    """
    return "This is a test"


if __name__ == "__main__":
    main()
