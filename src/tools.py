from os.path import join
import os, threading, subprocess, webdriver_manager

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



class Tools:
    def __init__(self):
        self.driver_path = ''
        
    def thd_updtWbd(self):
        td_updtWbd = threading.Thread(target=self.update_webdriver)
        td_updtWbd.start()
        td_updtWbd.join
    
    def check_webdriver(self):
        try:
            driver = webdriver.Chrome()
            driver.quit()
        except: pass
        pass
    
    def update_webdriver(self):
        try: self.driver_path = ChromeDriverManager(path = r".\\tools").install()
        except: print('has')
    
    def get_driver_path(self):
        return ChromeDriverManager(path = r".\\tools").install()

    
    