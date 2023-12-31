# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_w.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(561, 561)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(561, 561))
        MainWindow.setMaximumSize(QtCore.QSize(561, 561))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frm_main = QtWidgets.QFrame(self.centralwidget)
        self.frm_main.setGeometry(QtCore.QRect(0, 0, 561, 561))
        self.frm_main.setStyleSheet("background-color: rgb(20, 20, 20);")
        self.frm_main.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_main.setObjectName("frm_main")
        self.tabwg_main = QtWidgets.QTabWidget(self.frm_main)
        self.tabwg_main.setGeometry(QtCore.QRect(0, 0, 561, 561))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.tabwg_main.setFont(font)
        self.tabwg_main.setStyleSheet("background-color: rgb(65, 65, 65);")
        self.tabwg_main.setObjectName("tabwg_main")
        self.tab_download = QtWidgets.QWidget()
        self.tab_download.setObjectName("tab_download")
        self.frm_download = QtWidgets.QFrame(self.tab_download)
        self.frm_download.setGeometry(QtCore.QRect(0, 0, 561, 531))
        self.frm_download.setStyleSheet("background-color: rgb(65, 65, 65);")
        self.frm_download.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_download.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_download.setObjectName("frm_download")
        self.scrA_urls = QtWidgets.QScrollArea(self.frm_download)
        self.scrA_urls.setGeometry(QtCore.QRect(30, 20, 501, 191))
        self.scrA_urls.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scrA_urls.setAcceptDrops(True)
        self.scrA_urls.setStyleSheet("width: 3px;\n"
"background-color: rgb(40, 40, 40);")
        self.scrA_urls.setWidgetResizable(True)
        self.scrA_urls.setObjectName("scrA_urls")
        self.scrwc_urls = QtWidgets.QWidget()
        self.scrwc_urls.setGeometry(QtCore.QRect(0, 0, 499, 189))
        self.scrwc_urls.setAcceptDrops(True)
        self.scrwc_urls.setObjectName("scrwc_urls")
        self.vlyo_urls = QtWidgets.QVBoxLayout(self.scrwc_urls)
        self.vlyo_urls.setSpacing(9)
        self.vlyo_urls.setObjectName("vlyo_urls")
        self.scrA_urls.setWidget(self.scrwc_urls)
        self.scrA_log = QtWidgets.QScrollArea(self.frm_download)
        self.scrA_log.setGeometry(QtCore.QRect(230, 348, 301, 161))
        self.scrA_log.setWidgetResizable(True)
        self.scrA_log.setObjectName("scrA_log")
        self.scrwc_log = QtWidgets.QWidget()
        self.scrwc_log.setGeometry(QtCore.QRect(0, 0, 299, 159))
        self.scrwc_log.setObjectName("scrwc_log")
        self.txtB_log = QtWidgets.QTextBrowser(self.scrwc_log)
        self.txtB_log.setGeometry(QtCore.QRect(0, 0, 301, 161))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.txtB_log.setFont(font)
        self.txtB_log.setFocusPolicy(QtCore.Qt.NoFocus)
        self.txtB_log.setStyleSheet("background-color: rgb(40, 40, 40);\n"
"color: rgb(220, 220, 220);\n"
"width: 2px;")
        self.txtB_log.setObjectName("txtB_log")
        self.scrA_log.setWidget(self.scrwc_log)
        self.ln_add_url = QtWidgets.QLineEdit(self.frm_download)
        self.ln_add_url.setGeometry(QtCore.QRect(30, 230, 421, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ln_add_url.setFont(font)
        self.ln_add_url.setStyleSheet("color: rgb(255, 255, 255);")
        self.ln_add_url.setText("")
        self.ln_add_url.setObjectName("ln_add_url")
        self.btn_add_url = QtWidgets.QPushButton(self.frm_download)
        self.btn_add_url.setGeometry(QtCore.QRect(470, 230, 61, 33))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.btn_add_url.setFont(font)
        self.btn_add_url.setStyleSheet("color: rgb(245, 245, 245);\n"
"background-color: rgb(88, 88, 88);")
        self.btn_add_url.setObjectName("btn_add_url")
        self.scrA_complete = QtWidgets.QScrollArea(self.frm_download)
        self.scrA_complete.setGeometry(QtCore.QRect(30, 348, 171, 161))
        self.scrA_complete.setWidgetResizable(True)
        self.scrA_complete.setObjectName("scrA_complete")
        self.scrwc_complete = QtWidgets.QWidget()
        self.scrwc_complete.setGeometry(QtCore.QRect(0, 0, 169, 159))
        self.scrwc_complete.setObjectName("scrwc_complete")
        self.txtB_complete = QtWidgets.QTextBrowser(self.scrwc_complete)
        self.txtB_complete.setGeometry(QtCore.QRect(0, 0, 171, 161))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.txtB_complete.setFont(font)
        self.txtB_complete.setFocusPolicy(QtCore.Qt.NoFocus)
        self.txtB_complete.setStyleSheet("background-color: rgb(40, 40, 40);\n"
"color: rgb(220, 220, 220);\n"
"width: 2px;")
        self.txtB_complete.setObjectName("txtB_complete")
        self.scrA_complete.setWidget(self.scrwc_complete)
        self.lbt_complete = QtWidgets.QLabel(self.frm_download)
        self.lbt_complete.setGeometry(QtCore.QRect(31, 310, 141, 30))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.lbt_complete.setFont(font)
        self.lbt_complete.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.lbt_complete.setObjectName("lbt_complete")
        self.btn_start_download = QtWidgets.QPushButton(self.frm_download)
        self.btn_start_download.setEnabled(False)
        self.btn_start_download.setGeometry(QtCore.QRect(210, 286, 141, 33))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.btn_start_download.setFont(font)
        self.btn_start_download.setStyleSheet("QPushButton {\n"
"    color: rgb(0, 255, 0);\n"
"    background-color: rgb(88, 88, 88);\n"
"}\n"
"QPushButton:hover {\n"
"    color: rgb(0, 220, 0);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(160, 160, 160);\n"
"}")
        self.btn_start_download.setObjectName("btn_start_download")
        self.tabwg_main.addTab(self.tab_download, "")
        self.tab_setting = QtWidgets.QWidget()
        self.tab_setting.setObjectName("tab_setting")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_setting)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 551, 531))
        self.scrollArea.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 532, 618))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frm_setting = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.frm_setting.setMinimumSize(QtCore.QSize(0, 600))
        self.frm_setting.setMaximumSize(QtCore.QSize(16777215, 600))
        self.frm_setting.setStyleSheet("background-color: rgb(65, 65, 65);")
        self.frm_setting.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_setting.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_setting.setObjectName("frm_setting")
        self.frm_tool_0 = QtWidgets.QFrame(self.frm_setting)
        self.frm_tool_0.setGeometry(QtCore.QRect(-10, 95, 381, 81))
        self.frm_tool_0.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.frm_tool_0.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_tool_0.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_tool_0.setObjectName("frm_tool_0")
        self.lbt_tool_n_t0 = QtWidgets.QLabel(self.frm_tool_0)
        self.lbt_tool_n_t0.setGeometry(QtCore.QRect(30, 10, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.lbt_tool_n_t0.setFont(font)
        self.lbt_tool_n_t0.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbt_tool_n_t0.setObjectName("lbt_tool_n_t0")
        self.lbt_status_t0 = QtWidgets.QLabel(self.frm_tool_0)
        self.lbt_status_t0.setGeometry(QtCore.QRect(110, 54, 261, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.lbt_status_t0.setFont(font)
        self.lbt_status_t0.setStyleSheet("QLabel{\n"
"    color: rgb(255, 85, 0);\n"
"}")
        self.lbt_status_t0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbt_status_t0.setObjectName("lbt_status_t0")
        self.gBox_rdBtn_ad_t0 = QtWidgets.QGroupBox(self.frm_tool_0)
        self.gBox_rdBtn_ad_t0.setGeometry(QtCore.QRect(240, 10, 138, 36))
        self.gBox_rdBtn_ad_t0.setStyleSheet("border-style: none;")
        self.gBox_rdBtn_ad_t0.setTitle("")
        self.gBox_rdBtn_ad_t0.setObjectName("gBox_rdBtn_ad_t0")
        self.rdBtn_ad_t0 = QtWidgets.QRadioButton(self.gBox_rdBtn_ad_t0)
        self.rdBtn_ad_t0.setGeometry(QtCore.QRect(20, 6, 118, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.rdBtn_ad_t0.setFont(font)
        self.rdBtn_ad_t0.setStyleSheet("color: rgb(255, 255, 255);")
        self.rdBtn_ad_t0.setObjectName("rdBtn_ad_t0")
        self.btn_download_t0 = QtWidgets.QPushButton(self.frm_setting)
        self.btn_download_t0.setEnabled(False)
        self.btn_download_t0.setGeometry(QtCore.QRect(390, 110, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.btn_download_t0.setFont(font)
        self.btn_download_t0.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 0);\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-color: rgba(80, 80, 80, 180);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-color: rgba(255, 255, 0, 190);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(120, 120, 120);\n"
"}")
        self.btn_download_t0.setObjectName("btn_download_t0")
        self.line_tool = QtWidgets.QFrame(self.frm_setting)
        self.line_tool.setGeometry(QtCore.QRect(10, 200, 531, 16))
        self.line_tool.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_tool.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_tool.setObjectName("line_tool")
        self.lbt_tool = QtWidgets.QLabel(self.frm_setting)
        self.lbt_tool.setGeometry(QtCore.QRect(110, 10, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(23)
        self.lbt_tool.setFont(font)
        self.lbt_tool.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbt_tool.setAlignment(QtCore.Qt.AlignCenter)
        self.lbt_tool.setObjectName("lbt_tool")
        self.lbt_opt = QtWidgets.QLabel(self.frm_setting)
        self.lbt_opt.setGeometry(QtCore.QRect(110, 230, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(23)
        self.lbt_opt.setFont(font)
        self.lbt_opt.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbt_opt.setAlignment(QtCore.Qt.AlignCenter)
        self.lbt_opt.setObjectName("lbt_opt")
        self.frm_opt_0 = QtWidgets.QFrame(self.frm_setting)
        self.frm_opt_0.setGeometry(QtCore.QRect(-10, 315, 381, 151))
        self.frm_opt_0.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.frm_opt_0.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_opt_0.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_opt_0.setObjectName("frm_opt_0")
        self.lbt_opt_n_o0 = QtWidgets.QLabel(self.frm_opt_0)
        self.lbt_opt_n_o0.setGeometry(QtCore.QRect(30, 10, 341, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.lbt_opt_n_o0.setFont(font)
        self.lbt_opt_n_o0.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbt_opt_n_o0.setObjectName("lbt_opt_n_o0")
        self.txtB_opt_i_o0 = QtWidgets.QTextBrowser(self.frm_opt_0)
        self.txtB_opt_i_o0.setGeometry(QtCore.QRect(20, 60, 341, 81))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.txtB_opt_i_o0.setFont(font)
        self.txtB_opt_i_o0.setFocusPolicy(QtCore.Qt.NoFocus)
        self.txtB_opt_i_o0.setStyleSheet("color: rgb(240, 240, 240);")
        self.txtB_opt_i_o0.setObjectName("txtB_opt_i_o0")
        self.gBox_rdBtn_aa_url = QtWidgets.QGroupBox(self.frm_setting)
        self.gBox_rdBtn_aa_url.setGeometry(QtCore.QRect(400, 370, 81, 61))
        self.gBox_rdBtn_aa_url.setStyleSheet("border-style: none;")
        self.gBox_rdBtn_aa_url.setTitle("")
        self.gBox_rdBtn_aa_url.setObjectName("gBox_rdBtn_aa_url")
        self.rdBtn_auto_add_url = QtWidgets.QRadioButton(self.gBox_rdBtn_aa_url)
        self.rdBtn_auto_add_url.setGeometry(QtCore.QRect(20, 20, 61, 21))
        self.rdBtn_auto_add_url.setStyleSheet("color: rgb(255, 255, 255);")
        self.rdBtn_auto_add_url.setObjectName("rdBtn_auto_add_url")
        self.verticalLayout.addWidget(self.frm_setting)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.tabwg_main.addTab(self.tab_setting, "")
        self.tab_tutorial = QtWidgets.QWidget()
        self.tab_tutorial.setObjectName("tab_tutorial")
        self.frm_tutorial = QtWidgets.QFrame(self.tab_tutorial)
        self.frm_tutorial.setGeometry(QtCore.QRect(0, 0, 561, 531))
        self.frm_tutorial.setStyleSheet("background-color: rgb(65, 65, 65);")
        self.frm_tutorial.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_tutorial.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_tutorial.setObjectName("frm_tutorial")
        self.scrA_tutorial_t = QtWidgets.QScrollArea(self.frm_tutorial)
        self.scrA_tutorial_t.setGeometry(QtCore.QRect(30, 230, 501, 271))
        self.scrA_tutorial_t.setWidgetResizable(True)
        self.scrA_tutorial_t.setObjectName("scrA_tutorial_t")
        self.scrwc_tutoral_t = QtWidgets.QWidget()
        self.scrwc_tutoral_t.setGeometry(QtCore.QRect(0, 0, 499, 269))
        self.scrwc_tutoral_t.setObjectName("scrwc_tutoral_t")
        self.txtB_tutorial_t = QtWidgets.QTextBrowser(self.scrwc_tutoral_t)
        self.txtB_tutorial_t.setGeometry(QtCore.QRect(0, 0, 501, 271))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.txtB_tutorial_t.setFont(font)
        self.txtB_tutorial_t.setFocusPolicy(QtCore.Qt.NoFocus)
        self.txtB_tutorial_t.setStyleSheet("color: rgb(255, 255, 255);\n"
"border-style: none;\n"
"width: 4px;")
        self.txtB_tutorial_t.setObjectName("txtB_tutorial_t")
        self.scrA_tutorial_t.setWidget(self.scrwc_tutoral_t)
        self.txtB_app_info = QtWidgets.QTextBrowser(self.frm_tutorial)
        self.txtB_app_info.setGeometry(QtCore.QRect(30, 20, 501, 201))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.txtB_app_info.setFont(font)
        self.txtB_app_info.setFocusPolicy(QtCore.Qt.NoFocus)
        self.txtB_app_info.setStyleSheet("color: rgb(255, 255, 255);\n"
"border-style: none;")
        self.txtB_app_info.setObjectName("txtB_app_info")
        self.tabwg_main.addTab(self.tab_tutorial, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabwg_main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.txtB_log.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.ln_add_url.setPlaceholderText(_translate("MainWindow", "Enter URL here"))
        self.btn_add_url.setText(_translate("MainWindow", "ADD"))
        self.txtB_complete.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.lbt_complete.setText(_translate("MainWindow", "Complete :"))
        self.btn_start_download.setText(_translate("MainWindow", "START"))
        self.tabwg_main.setTabText(self.tabwg_main.indexOf(self.tab_download), _translate("MainWindow", "Download"))
        self.lbt_tool_n_t0.setText(_translate("MainWindow", "Web driver (chrome)"))
        self.lbt_status_t0.setText(_translate("MainWindow", "......"))
        self.rdBtn_ad_t0.setText(_translate("MainWindow", "Auto Download"))
        self.btn_download_t0.setText(_translate("MainWindow", "Download"))
        self.lbt_tool.setText(_translate("MainWindow", "Tools"))
        self.lbt_opt.setText(_translate("MainWindow", "Options"))
        self.lbt_opt_n_o0.setText(_translate("MainWindow", "Auto add URL to Queue"))
        self.txtB_opt_i_o0.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The app will continuously listen, and when the user copies a specific URL, the app will add the URL to the queue.</p></body></html>"))
        self.rdBtn_auto_add_url.setText(_translate("MainWindow", "On"))
        self.tabwg_main.setTabText(self.tabwg_main.indexOf(self.tab_setting), _translate("MainWindow", "Setting"))
        self.txtB_tutorial_t.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Tutorial</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">First, you need to download tools from Setting tab.</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Second, obtain the URL of the webpage where the sheet music you want to download is located.</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Third, back to this app, enter the URL into the input box in the middle of the Download tab and click ADD.</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can add many URL into the Queue, click the X button on the right side of the URL to remove it.</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Finally, wait until all url box turns green and click START to run the program.</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.txtB_app_info.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Muse Hunter</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">A tool for download score from website ... without login</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">version : 1.0.0</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Supported website :</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Musescore</span></p></body></html>"))
        self.tabwg_main.setTabText(self.tabwg_main.indexOf(self.tab_tutorial), _translate("MainWindow", "Tutorial"))
