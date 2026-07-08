"""
End-to-end tests using Playwright.

Each test drives a real headless Chromium browser against the live app
(started by the fastapi_server fixture), simulating exactly what a user
does: load the page, type numbers, click a button, read the result.
"""

import pytest
from playwright.sync_api import expect

BASE_URL = "http://localhost:8000"


@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    """The homepage displays the Hello World heading."""
    page.goto(BASE_URL)
    assert page.inner_text("h1") == "Hello World"


@pytest.mark.e2e
def test_calculator_add(page, fastapi_server):
    """Adding 10 and 5 displays 'Calculation Result: 15'."""
    page.goto(BASE_URL)
    page.fill("#a", "10")
    page.fill("#b", "5")
    page.click('button:text("Add")')
    expect(page.locator("#result")).to_have_text("Calculation Result: 15")


@pytest.mark.e2e
def test_calculator_subtract(page, fastapi_server):
    """Subtracting 5 from 10 displays 'Calculation Result: 5'."""
    page.goto(BASE_URL)
    page.fill("#a", "10")
    page.fill("#b", "5")
    page.click('button:text("Subtract")')
    expect(page.locator("#result")).to_have_text("Calculation Result: 5")


@pytest.mark.e2e
def test_calculator_multiply(page, fastapi_server):
    """Multiplying 10 by 5 displays 'Calculation Result: 50'."""
    page.goto(BASE_URL)
    page.fill("#a", "10")
    page.fill("#b", "5")
    page.click('button:text("Multiply")')
    expect(page.locator("#result")).to_have_text("Calculation Result: 50")


@pytest.mark.e2e
def test_calculator_divide(page, fastapi_server):
    """Dividing 10 by 5 displays 'Calculation Result: 2'."""
    page.goto(BASE_URL)
    page.fill("#a", "10")
    page.fill("#b", "5")
    page.click('button:text("Divide")')
    expect(page.locator("#result")).to_have_text("Calculation Result: 2")


@pytest.mark.e2e
def test_calculator_divide_by_zero(page, fastapi_server):
    """Dividing by zero displays the server's error message."""
    page.goto(BASE_URL)
    page.fill("#a", "10")
    page.fill("#b", "0")
    page.click('button:text("Divide")')
    expect(page.locator("#result")).to_have_text("Error: Cannot divide by zero!")
