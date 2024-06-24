import sys
from PyQt5.QtWidgets import QApplication
from gui.menu import Menu

def main():
    app = QApplication(sys.argv)
    window = Menu()
    window.main()  # Call main method to start the application logic
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
