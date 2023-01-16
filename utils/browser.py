from selenium import webdriver
# pega desde a raiz de nosso projeto até aqui, no browser.py
from pathlib import Path
from selenium.webdriver.chrome.service import Service
from time import sleep

ROOT_PATH = Path(__file__).parent.parent

# c:\Users\an\Desktop\curso-django-projeto1\utils\browser.py
# .parent
# \Users\an\Desktop\curso-django-projeto1\utils
# .parent
# \Users\an\Desktop\curso-django-projeto1

CHROMEDRIVER_NAME = 'chromedriver'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME
# \Users\an\Desktop\curso-django-projeto1\bin\chromedriver


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    # service para passar onde está nosso chromedriver

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    # criar o browser
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


# este if não é executado quando importa dessa maneira

if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('http://www.udemy.com/')
    sleep(5)
    browser.quit()
