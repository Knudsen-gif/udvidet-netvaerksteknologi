import pytest
import re
from playwright.sync_api import Page, expect

@pytest.fixture(autouse=True)
def set_viewport(page: Page):
    """Sikrer standard desktop-opløsning."""
    page.set_viewport_size({"width": 1280, "height": 720})

def accept_cookies(page: Page):
    """Håndterer cookie-banner hvis det dukker op."""
    try:
        cookie_btn = page.get_by_role("button", name=re.compile(r"accept|godkend", re.IGNORECASE)).first
        if cookie_btn.is_visible(timeout=3000):
            cookie_btn.click()
    except Exception:
        pass

def test_1_forside_og_logo(page: Page):
    page.goto("https://www.zealand.dk/")
    accept_cookies(page)
    
    logo = page.locator('img[alt*="Zealand"], a.logo').first
    expect(logo).to_be_visible()

def test_2_soegefunktion(page: Page):
    # Read-only søgetest via direkte URL
    page.goto("https://www.zealand.dk/?s=Datamatiker")
    accept_cookies(page)
    
    expect(page.locator("body")).to_contain_text("Datamatiker")

def test_3_navigation_til_uddannelser(page: Page):
    # Direkte navigation til uddannelsesoversigten for at sikre en stabil test
    page.goto("https://www.zealand.dk/fuldtidsuddannelser/")
    accept_cookies(page)
    
    expect(page).to_have_url(re.compile(r".*fuldtidsuddannelser.*|.*uddannelser.*"))

def test_4_overskrift_vises(page: Page):
    page.goto("https://www.zealand.dk/fuldtidsuddannelser/")
    accept_cookies(page)
    
    heading = page.locator("h1").first
    expect(heading).to_be_visible()