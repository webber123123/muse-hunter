from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication
import sys
from muse_hunter import MuseHunter


if __name__ == '__main__':
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    QtGui.QGuiApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    muse = MuseHunter()
    muse.show()
    sys.exit(app.exec_())