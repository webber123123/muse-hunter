from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests, threading, pathlib, pyperclip
import time

from bs4 import BeautifulSoup

from ui_controller import UIController
from tools import Tools
import common as cmn





class MuseHunter(UIController):
    sgnl_change_wd_status = QtCore.pyqtSignal(str)
    sgnl_ck_webdriver = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        # init val
        self.tools = Tools()
        self.MAX_QUEUE = 99
        self.url_queue = {}     # id : { 'url':'......', 'status':'down/ing/up/fail', 'name':'......', 'page':'...' }
        self.done_urls = []
        self.timer_freq = {'auto_url':1000}
        # init action
        self.bind_event()
        self.bind_signal()
        self.thd_initial_process()
        self.auto_url_listener.start(self.timer_freq['auto_url'])
    
    def bind_event(self):
        self.btn_add_url.clicked.connect(self.add_url)
        self.btn_download_t0.clicked.connect(self.update_tool_0)
        self.ln_add_url.returnPressed.connect(self.add_url)
        # timer
        self.auto_url_listener.timeout.connect(self.auto_add_url)
    
    def bind_signal(self):
        self.sgnl_change_wd_status.connect(self.change_webdriver_status)
        self.sgnl_ck_webdriver.connect(self.check_webdriver_available)
    
    def thd_initial_process(self):
        thd_init_prc = threading.Thread(target=self.initial_process)
        thd_init_prc.start()
        thd_init_prc.join
    
    def initial_process(self):
        self.check_webdriver_available()
    
    # download tab
    
    def add_url(self, new_url=''):
        if new_url == False: new_url = self.ln_add_url.text()
        print(new_url)
        if new_url != '':
            self.update_log('adding', 'ing')
            self.btn_start_download.setEnabled(False)
            for i in range(self.MAX_QUEUE):
                if i not in self.url_queue:
                    self.url_queue[i] = {'url':new_url, 'status':'down', 'name':'None', 'page':'None'}
                    new_wg = self.add_frame_to_queue(i, new_url)
                    new_wg[2].clicked.connect(lambda: self.del_url(i))
                    self.ln_add_url.clear()
                    self.start_ckeck_url(i)
                    break
            if cmn.TESTING['print']:
                print(new_url)
                print(self.url_queue)
    
    def del_url(self, id):
        exec('self.vlyo_urls.removeWidget(self.frm_url_%s)'%(id))
        exec('self.frm_url_%s.deleteLater()'%(id))
        self.scrwc_urls.repaint()
        del self.url_queue[id]
        self.check_download_available()
    
    def auto_add_url(self):
        clipboard_content = pyperclip.paste()
        if 'https://musescore.com/' in clipboard_content and False:
            self.add_url(clipboard_content)
            pyperclip.copy('')
        self.auto_url_listener.start(self.timer_freq['auto_url'])
    
    def start_ckeck_url(self, id):
        ck_url = threading.Thread(target=self.check_url, args=(id, ))
        ck_url.start()
        ck_url.join
    
    def check_url(self, id):
        try:
            if self.url_queue[id]['status'] == 'down':
                self.change_url_status('ing', id)
                time.sleep(1)
                try:
                    res = requests.get(self.url_queue[id]['url'])
                    soup = BeautifulSoup(res.content, 'html.parser')
                    title = soup.find("meta", property="og:title")["content"]
                    _sub_str_2 = 'pages_count&quot;:'
                    _sub_str = 'pages_count":'
                    _str_html = str(soup)
                    
                    _index = _str_html.find(_sub_str)
                    page_count = str(soup)[_index+len(_sub_str):_index+len(_sub_str)+3].split(',')[0]
                    
                    if not page_count.isnumeric() or title == '':
                        _index = _str_html.find(_sub_str_2)
                        page_count = str(soup)[_index+len(_sub_str_2):_index+len(_sub_str_2)+3].split(',')[0]
                    
                    if cmn.TESTING['print']: print(_index, str(soup)[_index+len(_sub_str_2):_index+len(_sub_str_2)+3])
                    
                    #https://musescore.com/user/12461571/scores/3291706
                    
                    if not page_count.isnumeric(): raise Exception
                    self.url_queue[id]['name'], self.url_queue[id]['pages'] = title, page_count
                    self.change_url_status('up', id, title)
                    if cmn.TESTING['print']: print(self.url_queue[id])
                except Exception as e:
                    if cmn.TESTING['exception']: print(e)
                    self.change_url_status('fail', id, 'Error : Sheet not found !')
        except: pass
        self.check_download_available()
    
    def change_url_status(self, status, id, title='none'):
        self.url_queue[id]['status'] = status
        if status == 'ing':
            style_s = '''background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(255, 255, 0, 180), stop: 1.0 rgba(220, 220, 0, 130));
border-radius: 4px;'''
        elif status == 'up':
            style_s = '''background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(85, 255, 0, 180), stop: 1.0 rgba(70, 220, 0, 130));
border-radius: 4px;'''
        elif status == 'fail':
            style_s = '''background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(255, 85, 0, 180), stop: 1.0 rgba(220, 80, 0, 130));
border-radius: 4px;'''
        t_code = f'''self.frm_url_{id}.setStyleSheet(style_s)
if title != 'none': self.lbt_url_{id}.setText(title)'''
        exec(t_code)
    
    def check_download_available(self):
        # check status
        t_dict = self.url_queue.copy()
        if t_dict == {}:
            self.btn_start_download.setEnabled(False)
            return False
        for sheet in t_dict:
            if t_dict[sheet]['status'] != 'up':
                self.btn_start_download.setEnabled(False)
                return False
        self.btn_start_download.setEnabled(True)
        return True
    
    # tool tab
    
    def check_webdriver_available(self):
        # webdriver
        self.btn_download_t0.setEnabled(False)
        self.tools.tools_status['webdriver'] = False
        self.change_webdriver_status('checking')
        rst = self.tools.check_webdriver()
        if rst == 'up': self.tools.tools_status['webdriver'] = True
        elif rst == 'need dl' or rst == 'need updt': self.btn_download_t0.setEnabled(True)
        self.change_webdriver_status(rst)
    
    def update_tool_0(self):
        self.tools.thd_updtWbd(self.sgnl_change_wd_status.emit, 'downloading', self.sgnl_ck_webdriver.emit)
    
    def change_webdriver_status(self, sts):
        if sts == 'up': # up / need download / need update / downloading / checking
            self.lbt_status_t0.setText('Available')
            self.set_wg_style(self.lbt_status_t0, 'color: rgb(85, 255, 0);')
        elif sts == 'checking':
            self.lbt_status_t0.setText('Checking updates ...')
            self.set_wg_style(self.lbt_status_t0, 'color: rgb(0, 255, 255);')
        elif sts == 'need dl':
            self.lbt_status_t0.setText('Need to download')
            self.set_wg_style(self.lbt_status_t0, 'color: rgb(255, 10, 0);')
        elif sts == 'need updt':
            self.lbt_status_t0.setText('Need to update')
            self.set_wg_style(self.lbt_status_t0, 'color: rgb(255, 170, 0);')
        elif sts == 'downloading':
            self.btn_download_t0.setEnabled(False)
            self.lbt_status_t0.setText('Downloading ...')
            self.set_wg_style(self.lbt_status_t0, 'color: rgb(255, 255, 0);')
        
    # downloader
    
    def run_downloader(self):
        if not self.check_download_available(): return 
        for sheet in self.url_queue:
            if 'musescore' in self.url_queue[sheet]['url']:
                self.get_sheet_musescore(sheet)
    
    def get_sheet_musescore(self, sheet_i):
        
        try: hunter = webdriver.Chrome(executable_path=self.tools.driver_path, chrome_options=cmn.chrome_options)
        except: return self.exception_handler('no up')
        
        try: hunter.get(sheet_i['url'])
        except: return self.exception_handler('no conn')
        
        
        
    
    def combine_svg_to_pdf(self):
        
        pass
    
    def exception_handler(self, event, args=[]):
        if event == 'no up':
            
            pass
        elif event == 'no conn':
            
            pass
        
        
        
        return False
    def update_log(self, text, type):
        htmls = ''
        current_time = time.strftime("--%H:%M--  ", time.localtime())
        if type == 'suc': htmls = '''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#55ff00;"> ''' + current_time + text + '''</span></p>'''
        elif type == 'ing': htmls = '''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#ffff00;"> ''' + current_time + text + '''</span></p>'''
        elif type == 'ct': htmls = '''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#ff7800;"> ''' + current_time + text + '''</span></p>'''
        elif type == 'sys': htmls = '''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#ffffff;"> ''' + current_time + text + '''</span></p>'''
        else: return
        self.txtB_log.append(htmls)
        self.txtB_log.moveCursor(QtGui.QTextCursor.End)
    
    def add_to_complete_area(self):
        
        pass
    
    # other
    
    def exit_comfirm(self):
        pass
    