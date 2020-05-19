from shutil import which

SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
SELENIUM_DRIVER_ARGUMENTS = ['-headless']

BOT_NAME = 'rozetka_notebooks'

SPIDER_MODULES = ['rozetka_notebooks.spiders']
NEWSPIDER_MODULE = 'rozetka_notebooks.spiders'

ROBOTSTXT_OBEY = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800
}
