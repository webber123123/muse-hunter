from os.path import join
import os, threading, subprocess, webdriver_manager

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import common as cmn



class Tools:
    def __init__(self):
        self.tools_status = {'webdriver':False}
        self.driver_path = self.get_driver_path()
        
    def thd_updtWbd(self):
        td_updtWbd = threading.Thread(target=self.update_webdriver)
        td_updtWbd.start()
        td_updtWbd.join
    
    def check_webdriver(self):
        try:
            test_driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=cmn.chrome_options)
            test_driver.quit()
            print('exist')
            return True
        except Exception as e:
            print(e)
            return False
    
    def update_webdriver(self):
        try: self.driver_path = ChromeDriverManager(path = r".\\tools").install()
        except: print('has')
    
    def get_driver_path(self):
        return ChromeDriverManager(path = r".\\tools").install()

    
    