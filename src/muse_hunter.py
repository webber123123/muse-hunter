from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image
from PyPDF2 import PdfFileMerger
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

import requests, threading, pyperclip, subprocess
import time

from bs4 import BeautifulSoup

from ui_controller import UIController
from tools import Tools
import common as cmn





class MuseHunter(UIController):
    sgnl_change_wd_status = QtCore.pyqtSignal(str)
    sgnl_ck_webdriver = QtCore.pyqtSignal()
    sgnl_updt_log = QtCore.pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        # init val
        self.tools = Tools()
        self.MAX_QUEUE = 49
        self.url_queue = {}     # id : { 'url':'......', 'status':'down/ing/up/fail', 'name':'......', 'page':'...' }
        self.done_urls_c = 1
        self.timer_freq = {'auto_url':1000}
        # init action
        self.new_folder()
        self.bind_event()
        self.bind_signal()
        self.thd_initial_process()
        self.auto_url_listener.start(self.timer_freq['auto_url'])
    
    def bind_event(self):
        self.btn_add_url.clicked.connect(self.add_url)
        self.btn_download_t0.clicked.connect(self.update_tool_0)
        self.ln_add_url.returnPressed.connect(self.add_url)
        self.btn_start_download.clicked.connect(self.thd_run_downloader)
        # timer
        self.auto_url_listener.timeout.connect(self.auto_add_url)
    
    def bind_signal(self):
        self.sgnl_change_wd_status.connect(self.change_webdriver_status)
        self.sgnl_ck_webdriver.connect(self.check_webdriver_available)
        self.sgnl_updt_log.connect(self.update_log)
    
    def thd_initial_process(self):
        thd_init_prc = threading.Thread(target=self.initial_process)
        thd_init_prc.start()
        thd_init_prc.join
    
    def initial_process(self):
        self.check_webdriver_available()
    
    # download tab
    
    def add_url(self, new_url=''):
        if new_url == False: new_url = self.ln_add_url.text()
        if new_url != '':
            self.update_log('adding', 'ing')
            self.btn_start_download.setEnabled(False)
            for i in range(self.MAX_QUEUE):
                if i not in self.url_queue:
                    self.url_queue[i] = {'url':new_url, 'status':'down', 'name':'None', 'page':'None'}
                    new_wg = self.add_frame_to_queue(i, new_url)
                    new_wg[2].clicked.connect(lambda: self.del_url(i))
                    self.ln_add_url.clear()
                    self.thd_ckeck_url(i)
                    break
            if cmn.TESTING['print']:
                print(new_url)
                print(self.url_queue)
    
    def del_url(self, id):
        exec('self.vlyo_urls.removeWidget(self.frm_url_%s)'%(id))
        exec('self.frm_url_%s.deleteLater()'%(id))
        self.scrwc_urls.repaint()
        print('sadasdad : ')
        print(self.url_queue)
        del self.url_queue[id]
        self.check_download_available()
        self.sgnl_updt_log.emit('URL deleted\n', 'suc')
    
    def auto_add_url(self):
        clipboard_content = pyperclip.paste()
        if 'https://musescore.com/' in clipboard_content and False:
            self.add_url(clipboard_content)
            pyperclip.copy('')
        self.auto_url_listener.start(self.timer_freq['auto_url'])
    
    def thd_ckeck_url(self, id):
        ck_url = threading.Thread(target=self.ckeck_url, args=(id, ))
        ck_url.start()
        ck_url.join
    
    def ckeck_url(self, id):
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
                    if not page_count.isnumeric(): raise Exception
                    self.url_queue[id]['name'], self.url_queue[id]['pages'] = title, int(page_count)
                    self.change_url_status('up', id, title)
                    self.sgnl_updt_log.emit('URL added\n', 'suc')
                    if cmn.TESTING['print']: print(self.url_queue[id])
                except Exception as e:
                    self.change_url_status('fail', id, 'Error : Sheet not found !')
                    self.sgnl_updt_log.emit('failed to add URL\n', 'ct')
                    if cmn.TESTING['exception']: print(e)
                    
        except: pass
        self.check_download_available()
    
    def add_complete_url(self, name):
        if len(name) > 20: name = name[:20]
        self.txtB_complete.append(str(self.done_urls_c)+'. '+name+'\n---------------------')
        self.done_urls_c += 1
    
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
    
    def thd_run_downloader(self):
        thd_rundl = threading.Thread(target=self.run_downloader)
        thd_rundl.start()
        thd_rundl.join
    
    def run_downloader(self):
        if not self.check_download_available(): return
        self.sgnl_updt_log.emit('start download\n', 'ing')
        t_queue = self.url_queue.copy()
        for sheet in t_queue:
            if 'musescore' in t_queue[sheet]['url']:
                rtn = self.get_sheet_musescore(t_queue[sheet])
                if rtn[0]:
                    if self.combine_pages_to_pdf(t_queue[sheet], rtn[1]):
                        self.ending_combine(t_queue[sheet])
                        self.del_url(sheet)
                        self.add_complete_url(t_queue[sheet]['name'])
                        self.sgnl_updt_log.emit('sheet get !\n', 'suc')
    
    def get_sheet_musescore(self, sheet_i):
        self.sgnl_updt_log.emit('launching webdriver\n', 'ing')
        try: hunter = webdriver.Chrome(executable_path=self.tools.driver_path, chrome_options=cmn.chrome_options)
        except: return [self.exception_handler('no_tool_0_up')]
        
        self.sgnl_updt_log.emit('connecting to website\n', 'ing')
        try: hunter.get(sheet_i['url'])
        except: return [self.exception_handler('no_conn')]
        
        scrl_length = 400
        js="var q=document.getElementById('jmuse-scroller-component').scrollTop=" + str(scrl_length)
        hunter.execute_script(js)
        
        file_type = ''
        self.new_workspace()
        self.sgnl_updt_log.emit('downloading sheet pages\n', 'ing')
        for page in range(1, sheet_i['pages']+1):
            sh_xpath = '//*[@id="jmuse-scroller-component"]/div['+str(page)+']/img'
            while 1:
                try:
                    WebDriverWait(hunter, 4).until(EC.presence_of_element_located((By.XPATH, sh_xpath)))
                    break
                except:
                    scrl_length += 200
                    js="var q=document.getElementById('jmuse-scroller-component').scrollTop=" + str(scrl_length)
                    hunter.execute_script(js)
                    if scrl_length > 1200*page: return [self.exception_handler('page_missing')]
            try:
                sc_src = hunter.find_element('xpath', sh_xpath).get_attribute('src')
                if page == 1:
                    if 'score_1.svg' in sc_src: file_type = '.svg'
                    else: file_type = '.png'
                if cmn.TESTING['print']: print(sc_src)
                res = requests.get(sc_src)
                with open('workspace\\'+str(page)+file_type ,'wb') as f:
                    f.write(res.content)
            except: return [self.exception_handler('dl_fail')]
            scrl_length += 1000
            js="var q=document.getElementById('jmuse-scroller-component').scrollTop=" + str(scrl_length)
            hunter.execute_script(js)
            time.sleep(1)
        hunter.quit()
        return [True, file_type]
    
    def combine_pages_to_pdf(self, sheet_i, file_type):
        self.sgnl_updt_log.emit('combining pages to pdf\n', 'ing')
        merger = PdfFileMerger()
        try:
            if file_type == '.svg':
                for img_n in range(1, sheet_i['pages']+1):
                    images = svg2rlg('workspace\\'+str(img_n)+'.svg')
                    renderPDF.drawToFile(images, 'workspace\\'+str(img_n)+'.pdf')
                time.sleep(1)
                for pdf_n in range(1, sheet_i['pages']+1):
                    merger.append('workspace\\'+str(pdf_n)+'.pdf')
                    time.sleep(0.5)
                merger.write('complete\\score.pdf')
                merger.close()
            elif file_type == '.png':
                for n in range(1, sheet_i['pages']+1):
                    im = Image.open('workspace\\%d.png'%(n))
                    im = im.convert('RGB')
                    im.save('workspace\\%d.jpg'%(n), quality=95)
                images = [
                    Image.open('workspace\\%d.jpg'%(n))
                    for n in range(1, sheet_i['pages']+1)
                ]
                images[0].save('complete\\score.pdf', 'PDF' ,resolution=100.0, save_all=True, append_images=images[1:])
        except Exception as e:
            if cmn.TESTING['exception']: print(e)
            return self.exception_handler('combine_error')
        return True
    
    def ending_combine(self, sheet_i):
        self.sgnl_updt_log.emit('clearing unnecessary files\n', 'ing')
        self.remove_workspace()
        try:
            cmnd = 'ren "complete\\score.pdf" "complete\\'+str(sheet_i['name']).replace('|', '／').replace('/', '／').replace('?', '_').replace('\"', '\'').replace('*', '~').replace(':', '-').replace('<', '_').replace('>', '_')+'.pdf"'
            rnpdf = subprocess.Popen(cmnd, shell=True)
            rnpdf.communicate()
        except:
            try:
                rnpdf = subprocess.Popen('ren "complete\\score.pdf" "complete\\InvalidName_%d.pdf"'%(self.done_urls_c), shell=True)
                rnpdf.communicate()
            except: pass
        time.sleep(0.75)
        return True
    
    def exception_handler(self, event, args=[]):
        if event == 'no_tool_0_up':
            self.sgnl_updt_log.emit('tool missing, please check your tools status at SETTING tab', 'ct')
        elif event == 'no_conn':
            self.sgnl_updt_log.emit('no connection, please check your network connection', 'ct')
        elif event == 'page_missing':
            self.sgnl_updt_log.emit('sheet page missing, please try again later', 'ct')
        elif event == 'dl_fail':
            self.sgnl_updt_log.emit('failed to download sheet page, please try again later', 'ct')
        elif event == 'combine_error':
            self.sgnl_updt_log.emit('failed to combine sheet pages, please try again later', 'ct')
        return False
    
    def update_log(self, text, type):
        htmls = ''
        current_time = time.strftime("--%H:%M--  ", time.localtime())
        if type == 'suc': htmls = '''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#55ff00;"> ''' + current_time + text + '''</span></p>'''
        elif type == 'ing': htmls = '''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#ffff00;"> ''' + current_time + text + '''</span></p>'''
        elif type == 'ct': htmls = '''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#ff7800;"> ''' + current_time + text + '''</span></p>'''
        elif type == 'sys': htmls = '''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#ffffff;"> ''' + current_time + text + '''</span></p>'''
        elif cmn.TESTING['exception']: return print('type error')
        self.txtB_log.append(htmls)
        self.txtB_log.moveCursor(QtGui.QTextCursor.End)
    
    def add_to_complete_area(self):
        
        pass
    
    # other
    
    def new_folder(self):
        cmnd = 'mkdir complete'
        new_f2 = subprocess.Popen(cmnd, shell=True)
        new_f2.communicate()
    
    def new_workspace(self):
        cmnd = 'mkdir workspace'
        new_ws = subprocess.Popen(cmnd, shell=True)
        new_ws.communicate()
    
    def remove_workspace(self):
        cmnd = 'rm /q workspace'
        del_ws = subprocess.Popen(cmnd, shell=True)
        del_ws.communicate()
        
    
    def exit_comfirm(self):
        pass
    