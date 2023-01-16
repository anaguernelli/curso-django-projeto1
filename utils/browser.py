from selenium import webdriver
# pega desde a raiz de nosso projeto até aqui, no browser.py
from pathlib import Path
from selenium.webdriver.chrome.service import Service
from time import sleep
import os


ROOT_PATH = Path(__file__).parent.parent

# c:\Users\an\Desktop\curso-django-projeto1\utils\browser.py
# .parent
# \Users\an\Desktop\curso-django-projeto1\utils
# .parent
# \Users\an\Desktop\curso-django-projeto1

CHROMEDRIVER_NAME = 'chromedriver'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME
# \Users\an\Desktop\curso-django-projeto1\bin\chromedriver


# função que cria o browser para mim
def make_chrome_browser(*options):
    # criar webdriver
    # opções do chrome
    chrome_options = webdriver.ChromeOptions()

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')

    if options is not None:
        for option in options:
            # estamos passando nas options qualquer argumento
            # como por exemplo o --headless
            chrome_options.add_argument(option)

    # service para passar o path do nosso chromedriver
    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    # criar o browser
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


# este if não é executado quando importa dessa maneira
# --headless não abre o navegador, mas continua atua "por baixo dos panos"
if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('http://www.udemy.com/')
    sleep(5)
    browser.quit()
