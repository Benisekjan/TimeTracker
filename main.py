import sys
from PyQt5.QtWidgets import QApplication
from PyObjCTools import AppHelper
from gui.menu import Menu

def main():
    app = QApplication(sys.argv)
    window = Menu()
    AppHelper.runEventLoop()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
