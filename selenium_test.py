from selenium import webdriver


URL = 'https://cgifederal.secure.force.com'


def get_captcha_base64_image(url):
    """Get captcha image in base64 format."""
    driver = webdriver.Firefox()
    driver.get(url)

    image_element = driver.find_element_by_id(
        'loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:theId'
    )

    _, base64_img = image_element.get_attribute('src').split(',')

    driver.close()

    return base64_img


def pass_authorization_on_site():
    pass


if __name__ == '__main__':
    captcha = get_captcha_base64_image(URL)
    print(captcha)
