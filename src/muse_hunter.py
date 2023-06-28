from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

import requests
from time import sleep
import threading

from bs4 import BeautifulSoup

from ui_controller import UIController


TESTING = {'print':True, 'quick_start':True}


class MuseHunter(UIController):
    def __init__(self):
        super().__init__()
        self.bind_event()
        self.MAX_QUEUE = 99
        self.url_queue = {}     # id : { 'url':'......', 'status':'down/ing/up/fail', 'name':'......', 'page':'...' }
        self.done_urls = []
    
    def bind_event(self):
        self.btn_add_url.clicked.connect(self.add_url)
    
    def add_url(self):
        new_url = self.ln_add_url.text()
        for i in range(self.MAX_QUEUE):
            if i not in self.url_queue:
                self.url_queue[i] = {'url':new_url, 'status':'down', 'name':'None', 'page':'None'}
                t_widget = []
                _translate = QtCore.QCoreApplication.translate
                t_code = f'''self.frm_url_{i} = QtWidgets.QFrame(self.scrwc_urls)
self.lbt_url_{i} = QtWidgets.QLabel(self.frm_url_{i})
self.btn_rm_u{i} = QtWidgets.QPushButton(self.frm_url_{i})
t_widget.append(self.frm_url_{i})
t_widget.append(self.lbt_url_{i})
t_widget.append(self.btn_rm_u{i})'''
                exec(t_code)
                t_widget[0].setMinimumSize(QtCore.QSize(0, 30))
                t_widget[0].setMaximumSize(QtCore.QSize(16777215, 30))
                t_widget[0].setStyleSheet("background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(100, 100, 100, 180), stop: 1.0 rgba(80, 80, 80, 130));"
                "border-radius: 4px;")
                t_widget[0].setFrameShape(QtWidgets.QFrame.StyledPanel)
                t_widget[0].setFrameShadow(QtWidgets.QFrame.Raised)
                t_widget[1].setGeometry(QtCore.QRect(10, 0, 441, 31))
                font = QtGui.QFont()
                font.setFamily("Microsoft YaHei UI")
                font.setPointSize(12)
                t_widget[1].setFont(font)
                t_widget[1].setStyleSheet("color: rgb(255, 255, 255);"
                "background-color: rgba(255, 255, 255, 0);")
                t_widget[2].setGeometry(QtCore.QRect(450, 0, 31, 27))
                font = QtGui.QFont()
                font.setFamily("Microsoft YaHei")
                font.setPointSize(14)
                t_widget[2].setFont(font)
                t_widget[2].setStyleSheet("background-color: rgba(255, 255, 255, 0);"
                "border-radius: 12px;"
                "color: rgba(255, 255, 255, 180);")
                t_widget[1].setText(_translate("MainWindow", new_url))
                t_widget[2].setText(_translate("MainWindow", "x"))
                self.vlyo_urls.addWidget(t_widget[0])
                t_widget[2].clicked.connect(lambda: self.del_url(i))
                self.start_ckeck_url(i)
                break
        if TESTING['print']:
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
                    _sub_str = 'pages_count&quot;:'
                    _str_html = str(soup)
                    _index = _str_html.find(_sub_str)
                    page_count = str(soup)[_index+len(_sub_str):_index+len(_sub_str)+3].split(',')[0]
                    if page_count == '\n<h': raise Exception
                    self.url_queue[id]['name'], self.url_queue[id]['pages'] = title, page_count
                    self.change_url_status('up', id, title)
                    if TESTING['print']: print(self.url_queue[id])
                except: self.change_url_status('fail', id, 'Error : Sheet not found !')
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
    
    def check_tools_available(self):
        pass
    
    def update_tools(self):
        pass
    
    def download_webdriver(self):
        pass


    
