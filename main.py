from PyQt5.QtWidgets import QApplication
from gui.menu import Menu
import sys

def main():
    app = QApplication(sys.argv)
    window = Menu()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
