from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import re


URL = 'https://cgifederal.secure.force.com'


class WebDriver():
    """Context manager to webdriver"""
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()



class wait_for_text_to_match(object):
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


def get_captcha_base64_image(url):
    """Get captcha image in base64 format."""
    with WebDriver(webdriver.Chrome()) as driver:

        driver.get(url)

        wait = WebDriverWait(driver, 5)

        image_element = wait.until(
            wait_for_text_to_match(
                (By.ID, 'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:theId'),
                r'data:image;base64,.'
                )
            )
        
        _, base64_img = image_element.string.split(',')


    return base64_img


def pass_authorization_on_site():
    pass


if __name__ == '__main__':
    captcha = get_captcha_base64_image(URL)
    print(captcha)
