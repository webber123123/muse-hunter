from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QBoxLayout, QListWidgetItem, QListWidget
from main_w import Ui_MainWindow

import common as cmn


class UIController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.vlyo_urls.addStretch()
        self.vlyo_urls.setDirection(QBoxLayout.BottomToTop)
    
    def add_frame_to_queue(self, i, new_url):
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
        return t_widget
    
    def set_wg_style(self, widget, tg_val):
        try:
            style_sheet = widget.styleSheet()
            sStr = style_sheet[ str(style_sheet).find('{')+1 : str(style_sheet).find('}') ]
            vals = sStr.split(';')
            rtnStr = style_sheet[ 0 : str(style_sheet).find('{') ] + '{'
            for i in range(len(vals)-1):
                if (' '+tg_val.split(':')[0]) in vals[i]:
                    vals[i] = vals[i][0:vals[i].find(tg_val.split(':')[0])] + tg_val
                rtnStr += (vals[i])
                if not ';' in vals[i]: rtnStr += ';'
            rtnStr += style_sheet[ str(style_sheet).find('}') : ]
            widget.setStyleSheet(rtnStr)
        except Exception as e: 
            if cmn.TESTING['exception']: print(e)
    
    
    
    