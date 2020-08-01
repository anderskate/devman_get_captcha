from selenium import webdriver


URL = 'https://cgifederal.secure.force.com'


class WebDriver():
    """Context manager to webdriver"""
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def get_captcha_base64_image(url):
    """Get captcha image in base64 format."""
    with WebDriver(webdriver.Chrome()) as driver:

        driver.get(url)

        image_element = driver.find_element_by_id(
            'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:theId'
        )

        _, base64_img = image_element.get_attribute('src').split(',')

    return base64_img


def pass_authorization_on_site():
    pass


if __name__ == '__main__':
    captcha = get_captcha_base64_image(URL)
    print(captcha)
