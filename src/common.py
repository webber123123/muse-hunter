from selenium import webdriver
import pathlib

VERSION = '1.0.0'
TESTING = {'print':True, 'exception':False}


path_cr = str(pathlib.Path().absolute()) + '\\'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': path_cr }
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_experimental_option('prefs', prefs)