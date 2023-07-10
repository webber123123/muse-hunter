from selenium import webdriver
import pathlib

VERSION = '1.0.0'
TESTING = {'print':False, 'exception':False}

app_alive = True


path_cr = str(pathlib.Path().absolute()) + '\\'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': path_cr }
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_experimental_option('prefs', prefs)

class User:
    def __init__(self):
        self.setting_pref = {'wd_auto_dl':False, 'auto_add_url':False}
        self.read_file()
    
    def write_to_file(self):
        with open('user\\user.txt', 'w') as f:
            f.write(str(self.setting_pref))
    
    def read_file(self):
        try:
            with open('user\\user.txt', 'r') as f:
                content = f.read()
            self.setting_pref = eval(content)
            if TESTING['print']: print(self.setting_pref)
        except Exception as e:
            if TESTING['exception']: print(e)
            self.write_to_file()
    
    def change_pref(self, key, val):
        self.setting_pref[key] = val
        self.write_to_file()