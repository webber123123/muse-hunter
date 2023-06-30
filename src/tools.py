from os.path import join
import os, threading, subprocess, webdriver_manager

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import common as cmn



class Tools:
    def __init__(self):
        self.tools_status = {'webdriver':False}
        #self.driver_path = self.get_driver_path()
        self.driver_path = ''
        
    def check_webdriver(self):
        try:
            self.driver_path = self.get_driver_path()
            if self.driver_path == '': return 'need dl'
            test_driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=cmn.chrome_options)
            test_driver.quit()
            return 'up'
        except Exception as e:
            if cmn.TESTING['exception']: print('in check_webdriver : '+str(e))
            return 'need updt'
    
    def thd_updtWbd(self, func, param, func_ed):
        td_updtWbd = threading.Thread(target=self.update_webdriver, args=(func, param, func_ed, ))
        td_updtWbd.start()
        td_updtWbd.join
    
    def update_webdriver(self, change_status, val, check_function):
        change_status(val)
        try: self.driver_path = ChromeDriverManager(path = r".\\tools").install()
        except: pass
        check_function()
    
    def get_driver_path(self):
        fTree = os.walk( '.\\tools\\.wdm\\drivers\\chromedriver\\win32', topdown=True )
        fpnList = []
        for dirs, subdirs, files in fTree:
            for f in files: 
                if 'chromedriver.exe' in f:
                    full_path = join(dirs, f)
                    fpnList.append(full_path)
                    return fpnList[0]
        return ''
    
    
    
    