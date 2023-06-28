from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QBoxLayout, QListWidgetItem, QListWidget
from main_w import Ui_MainWindow


class UIController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.vlyo_urls.addStretch()
        self.vlyo_urls.setDirection(QBoxLayout.BottomToTop)
        