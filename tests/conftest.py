"""
Shared pytest fixtures for end-to-end testing.

- fastapi_server: starts the real application (python main.py) in a
  subprocess, waits for it to answer HTTP, and shuts it down after tests.
- playwright/browser/page: manage a headless Chromium browser so tests can
  drive the site the way a user would.
"""

import subprocess
import sys
import time

import pytest
import requests
from playwright.sync_api import sync_playwright

SERVER_URL = "http://127.0.0.1:8000/"


@pytest.fixture(scope="session")
def fastapi_server():
    """Run the FastAPI app in a subprocess for the duration of the session."""
    process = subprocess.Popen([sys.executable, "main.py"])

    # Poll until the server answers or the timeout expires.
    timeout = 30
    start = time.time()
    while time.time() - start < timeout:
        try:
            if requests.get(SERVER_URL).status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)
    else:
        process.terminate()
        raise RuntimeError("FastAPI server failed to start within timeout.")

    yield

    process.terminate()
    process.wait()


@pytest.fixture(scope="session")
def playwright_instance():
    """Manage Playwright's lifecycle for the test session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    """Launch one headless Chromium browser shared by all E2E tests."""
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """Give each test a fresh browser page."""
    page = browser.new_page()
    yield page
    page.close()
