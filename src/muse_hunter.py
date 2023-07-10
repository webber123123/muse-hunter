from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QPushButton

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image
from PyPDF2 import PdfFileMerger
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

import requests, threading, pyperclip, subprocess, time
from bs4 import BeautifulSoup

from ui_controller import UIController
from tools import Tools
import common as cmn
from common import User



class MuseHunter(UIController):
    sgnl_change_wd_status = QtCore.pyqtSignal(str)
    sgnl_ck_webdriver = QtCore.pyqtSignal()
    sgnl_updt_log = QtCore.pyqtSignal(str, str)
    sgnl_change_url_sts = QtCore.pyqtSignal(str, int, str)
    sgnl_change_btn_sts = QtCore.pyqtSignal(QPushButton, bool)
    
    def __init__(self):
        super().__init__()
        self.new_folder()
        # init val
        self.tools = Tools()
        self.user = User()
        self.MAX_QUEUE = 49
        self.auto_url_old = ''
        self.url_queue = {}     # id : { 'url':'......', 'status':'down/ing/up/fail/dl_fail', 'name':'......', 'page':'...' }
        self.done_urls_c = 1
        self.timer_freq = {'auto_url':1000}
        self.curr_sheet_id = 0
        self.downloader_running = False
        # init action
        self.set_rdBtn_status()
        self.bind_event()
        self.bind_signal()
        self.thd_initial_process()
        self.auto_url_listener.start(self.timer_freq['auto_url'])
    
    def bind_event(self):
        self.btn_add_url.clicked.connect(self.add_url)
        self.btn_download_t0.clicked.connect(self.update_tool_0)
        self.ln_add_url.returnPressed.connect(self.add_url)
        self.btn_start_download.clicked.connect(self.push_start_button)
        self.rdBtn_ad_t0.clicked.connect(self.btn_auto_dl_t0)
        self.rdBtn_auto_add_url.clicked.connect(self.btn_auto_add_url)
        # timer
        self.auto_url_listener.timeout.connect(self.auto_add_url)
    
    def bind_signal(self):
        self.sgnl_change_wd_status.connect(self.change_webdriver_status)
        self.sgnl_ck_webdriver.connect(self.check_webdriver_available)
        self.sgnl_updt_log.connect(self.update_log)
        self.sgnl_change_url_sts.connect(self.change_url_status)
        self.sgnl_change_btn_sts.connect(self.button_enable_switch)
    
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
        if not self.downloader_running:
            exec('self.vlyo_urls.removeWidget(self.frm_url_%s)'%(id))
            exec('self.frm_url_%s.deleteLater()'%(id))
            self.scrwc_urls.repaint()
            del self.url_queue[id]
            self.check_download_available()
            self.sgnl_updt_log.emit('URL deleted\n', 'suc')
    
    def auto_add_url(self):
        if self.user.setting_pref['auto_add_url']:
            clipboard_content = pyperclip.paste()
            if clipboard_content != self.auto_url_old and 'https://musescore.com/' in clipboard_content:
                self.auto_url_old = clipboard_content
                self.add_url(clipboard_content)
        if cmn.app_alive: self.auto_url_listener.start(self.timer_freq['auto_url'])
    
    def thd_ckeck_url(self, id):
        ck_url = threading.Thread(target=self.ckeck_url, args=(id, ))
        ck_url.start()
        ck_url.join
    
    def ckeck_url(self, id):
        try:
            if self.url_queue[id]['status'] == 'down':
                self.sgnl_change_url_sts.emit('ing', id, '')
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
                    self.sgnl_change_url_sts.emit('up', id, title)
                    self.sgnl_updt_log.emit('URL added\n', 'suc')
                    if cmn.TESTING['print']: print(self.url_queue[id])
                except Exception as e:
                    self.sgnl_change_url_sts.emit('fail', id, 'Error : Sheet not found !')
                    self.sgnl_updt_log.emit('failed to add URL\n', 'ct')
                    if cmn.TESTING['exception']: print(e)
        except: pass
        time.sleep(0.1)
        self.check_download_available()
    
    def add_complete_url(self, name):
        if len(name) > 20: name = name[:20]
        self.txtB_complete.append(str(self.done_urls_c)+'. '+name+'\n---------------------')
        self.done_urls_c += 1
    
    def change_url_status(self, status, id, title=''):
        try:
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
            elif status == 'dl_ing':
                style_s = '''background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(0, 255, 255, 180), stop: 1.0 rgba(0, 80, 80, 130));
border-radius: 4px;'''
            elif status == 'dl_fail':
                style_s = '''background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(100, 100, 100, 180), stop: 1.0 rgba(80, 80, 80, 130));
border-radius: 4px;'''
            t_code = f'''self.frm_url_{id}.setStyleSheet(style_s)
if title != '': self.lbt_url_{id}.setText(title)'''
            exec(t_code)
        except: pass
    
    def check_download_available(self):
        # check status
        t_dict = self.url_queue.copy()
        if t_dict == {}:
            self.sgnl_change_btn_sts.emit(self.btn_start_download, False)
            return False
        for sheet in t_dict:
            if t_dict[sheet]['status'] != 'up' and t_dict[sheet]['status'] != 'dl_fail':
                self.sgnl_change_btn_sts.emit(self.btn_start_download, False)
                return False
        self.sgnl_change_btn_sts.emit(self.btn_start_download, True)
        return True
        
    # tool tab
    
    def check_webdriver_available(self):
        # webdriver
        self.btn_download_t0.setEnabled(False)
        self.tools.tools_status['webdriver'] = False
        self.change_webdriver_status('checking')
        rst = self.tools.check_webdriver()
        if rst == 'up': self.tools.tools_status['webdriver'] = True
        elif rst == 'need dl' or rst == 'need updt':
            self.btn_download_t0.setEnabled(True)
        self.change_webdriver_status(rst)
        if self.user.setting_pref['wd_auto_dl'] and rst == 'need dl' or rst == 'need updt':
            self.update_tool_0()
    
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
    
    def set_rdBtn_status(self):
        self.rdBtn_ad_t0.setChecked(self.user.setting_pref['wd_auto_dl'])
        self.rdBtn_auto_add_url.setChecked(self.user.setting_pref['auto_add_url'])
    
    def btn_auto_dl_t0(self):
        button = self.sender()
        if button.isChecked(): self.user.change_pref('wd_auto_dl', True)
        else: self.user.change_pref('wd_auto_dl', False)
    
    def btn_auto_add_url(self):
        button = self.sender()
        if button.isChecked(): self.user.change_pref('auto_add_url', True)
        else: self.user.change_pref('auto_add_url', False)
    
    # downloader
    
    def thd_run_downloader(self):
        thd_rundl = threading.Thread(target=self.run_downloader)
        thd_rundl.start()
        thd_rundl.join
    
    def push_start_button(self):
        if self.downloader_running:
            self.stop_downloader()
            self.btn_start_download.setText('start')
            self.set_start_btn_style('rgb(0, 255, 0)', 'rgb(0, 220, 0)')
        else:
            self.thd_run_downloader()
            self.btn_start_download.setText('stop')
            self.set_start_btn_style('rgb(255, 0, 0)', 'rgb(220, 0, 0)')
    
    def run_downloader(self):
        if not self.check_download_available(): return
        self.sgnl_change_btn_sts.emit(self.btn_start_download, True)
        self.downloader_running = True
        self.sgnl_updt_log.emit('start download\n', 'sys')
        t_queue = self.url_queue.copy()
        for sheet in t_queue:
            self.curr_sheet_id = sheet
            self.sgnl_change_url_sts.emit('dl_ing', sheet, '')
            if self.downloader_running == False: break
            if 'musescore' in t_queue[sheet]['url']:
                try:
                    rtn = self.get_sheet_musescore(t_queue[sheet])
                    if rtn[0]:
                        if self.combine_pages_to_pdf(t_queue[sheet], rtn[1]):
                            self.ending_combine(t_queue[sheet])
                            self.del_url(sheet)
                            self.add_complete_url(t_queue[sheet]['name'])
                            self.sgnl_updt_log.emit('sheet get !\n', 'suc')
                            continue
                except: pass
            if self.downloader_running == False: break
            self.sgnl_change_url_sts.emit('dl_fail', sheet, '')
        try: self.sgnl_change_url_sts.emit('up', self.curr_sheet_id, '')
        except: pass
        self.check_download_available()
        self.remove_workspace()
        self.sgnl_updt_log.emit('downloader stopped\n', 'sys')
        self.sgnl_change_btn_sts.emit(self.btn_start_download, True)
    
    def stop_downloader(self):
        self.sgnl_change_btn_sts.emit(self.btn_start_download, False)
        self.sgnl_updt_log.emit('stopping downloader\n', 'ing')
        self.downloader_running = False
        self.sgnl_change_url_sts.emit('up', self.curr_sheet_id, '')
        try: hunter.quit()
        except: pass
    
    def get_sheet_musescore(self, sheet_i):
        global hunter
        
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
                    if '.svg' in sc_src: file_type = '.svg'
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
        self.sgnl_updt_log.emit('clearing unnecessary files and rename sheet\n', 'ing')
        self.remove_workspace()
        try:
            cmnd = 'ren "complete\\score.pdf" "'+str(sheet_i['name']).replace('|', '／').replace('/', '／').replace('?', '_').replace('\"', '\'').replace('*', '~').replace(':', '-').replace('<', '_').replace('>', '_')+'.pdf"'
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
    
    def fail_url_handle(self, sheet_id):
        self.sgnl_change_url_sts.emit('dl_fail', sheet_id, '')
        self.sgnl_updt_log.emit('the url has been passed', 'sys')
    
    # other
    
    def new_folder(self):
        cmnd = 'mkdir complete'
        new_f1 = subprocess.Popen(cmnd, shell=True)
        new_f1.communicate()
        cmnd = 'mkdir user'
        new_f2 = subprocess.Popen(cmnd, shell=True)
        new_f2.communicate()
    
    def new_workspace(self):
        cmnd = 'mkdir workspace'
        new_ws = subprocess.Popen(cmnd, shell=True)
        new_ws.communicate()
    
    def remove_workspace(self):
        try:
            cmnd = 'rd /s /q workspace'
            del_ws = subprocess.Popen(cmnd, shell=True)
            del_ws.communicate()
        except: pass
    
    def closeEvent(self, event):
        if QMessageBox.question(None, 'exit comfirm', 'exit ?', QMessageBox.Yes | QMessageBox.No) == QMessageBox.No: 
            event.ignore()
            return
        cmn.app_alive = False
        event.accept()