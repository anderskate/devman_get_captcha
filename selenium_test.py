import re
import asyncio
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from contextlib import contextmanager


URL = 'https://cgifederal.secure.force.com'

CAPTCHA_ELEMENT_ID = 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:theId'
EMAIL_FIELD_ELEMENT_ID = 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:username'
PASSWORD_FIELD_ELEMENT_ID = 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:password'
PRIVACY_STATEMENT_CHECKBOX_ELEMENT_NAME = 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:j_id167'
CAPTCHA_FIELD_ELEMENT_ID = 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:recaptcha_response_field'
LOGIN_BUTTON_FIELD_ID = 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:loginButton'


REGEX_SEARCH_CAPTCHA = r'data:image;base64,.'
WAITING_TIME = 5


@contextmanager
def start_driver():
    """Run driver as context manager"""
    driver = webdriver.Firefox()
    try:
        yield driver
    finally:
        driver.quit()


class SearchCaptchaDataInElement():
    """Search for captcha data in an element attribute.

    Searches using a regular expression.
    """
    def __init__(self, locator, pattern):
        self.locator = locator
        self.pattern = re.compile(pattern)

    def __call__(self, driver):
        try:
            element = ec._find_element(driver, self.locator)
            element_src = element.get_attribute('src')
            return self.pattern.search(element_src)
        except StaleElementReferenceException:
            return False


async def get_captcha_base64_image(url):
    """Get captcha image in base64 format."""
    with start_driver() as driver:
        driver.get(url)

        wait = WebDriverWait(driver, WAITING_TIME)

        image_element = wait.until(
            SearchCaptchaDataInElement(
                (By.ID, CAPTCHA_ELEMENT_ID),
                REGEX_SEARCH_CAPTCHA
                )
            )

        _ , base64_img = image_element.string.split(',')


        await asyncio.sleep(0)

    return base64_img


async def pass_authorization_on_site(driver, email, password, captcha_symbols):
    """Make authorization on the site.

    Enter the necessary credentials, such as login, password 
    and captcha for authorization on the site.
    """
    email_field = driver.find_element_by_id(EMAIL_FIELD_ELEMENT_ID)
    email_field.send_keys(email)

    password_field = driver.find_element_by_id(PASSWORD_FIELD_ELEMENT_ID)
    password_field.send_keys(password)

    privacy_statement_checkbox = driver.find_element_by_name(
        PRIVACY_STATEMENT_CHECKBOX_ELEMENT_NAME
        )
    privacy_statement_checkbox.click()

    captcha_field = driver.find_element_by_id(CAPTCHA_FIELD_ELEMENT_ID)
    captcha_field.send_keys(captcha_symbols)

    login_button = driver.find_element_by_id(LOGIN_BUTTON_FIELD_ID)
    login_button.click()

    await asyncio.sleep(0)
    


if __name__ == '__main__':
    asyncio.run(get_captcha_base64_image(URL))
