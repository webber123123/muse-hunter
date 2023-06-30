from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from selenium import webdriver

import requests, threading, pathlib, pyperclip
from time import sleep

from bs4 import BeautifulSoup

from ui_controller import UIController
from tools import Tools
import common as cmn





class MuseHunter(UIController):
    sgnl_change_wd_sts = QtCore.pyqtSignal(str)
    
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
        self.ln_add_url.returnPressed.connect(self.add_url_rtn_press)
        # timer
        self.auto_url_listener.timeout.connect(self.auto_add_url)
    
    def bind_signal(self):
        self.sgnl_change_wd_sts.connect(self.change_webdriver_status)
    
    def thd_initial_process(self):
        thd_init_prc = threading.Thread(target=self.initial_process)
        thd_init_prc.start()
        thd_init_prc.join
    
    def initial_process(self):
        self.check_webdriver_available()
    
    def add_url(self, new_url=''):
        if new_url == '': new_url = self.ln_add_url.text()
        if new_url != '':
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
    
    def start_ckeck_url(self, id):
        ck_url = threading.Thread(target=self.check_url, args=(id, ))
        ck_url.start()
        ck_url.join
    
    def check_url(self, id):
        try:
            if self.url_queue[id]['status'] == 'down':
                self.change_url_status('ing', id)
                sleep(1)
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
    
    def get_sheet(self):
        pass
    
    def combine_svg_to_pdf(self):
        pass
    
    def update_log(self):
        pass
    
    def add_to_complete_area(self):
        pass
    
    def exit_comfirm(self):
        pass
    
    def check_webdriver_available(self):
        # webdriver
        self.sgnl_change_wd_sts.emit('checking')
        rst = self.tools.check_webdriver()
        if rst == 'has':
            self.tools.tools_status['webdriver'] = True
            self.sgnl_change_wd_sts.emit('up')
        elif rst == 'need dl':
            self.tools.tools_status['webdriver'] = False
            self.btn_download_t0.setEnabled(True)
            self.sgnl_change_wd_sts.emit('need dl')
        elif rst == 'need updt':
            self.tools.tools_status['webdriver'] = False
            self.btn_download_t0.setEnabled(True)
        self.sgnl_change_wd_sts.emit(rst)
    
    def update_tool_0(self):
        self.sgnl_change_wd_sts.emit('downloading')
        self.tools.thd_updtWbd()
        self.check_webdriver_available()
    
    def add_url_rtn_press(self):
        self.add_url()
    
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
            self.lbt_status_t0.setText('Downloading ...')
            self.set_wg_style(self.lbt_status_t0, 'color: rgb(255, 255, 0);')
    
    def auto_add_url(self):
        clipboard_content = pyperclip.paste()
        if 'https://musescore.com/' in clipboard_content:
            self.add_url(clipboard_content)
            pyperclip.copy('')
        self.auto_url_listener.start(self.timer_freq['auto_url'])
        
