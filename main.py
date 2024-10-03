from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from gui.menu import Menu  # Import hlavní třídy okna z modulu menu
import sys

def main():
    # Vytvoření instance aplikace PyQt
    app = QApplication(sys.argv)

    # Vytvoření hlavního okna aplikace
    window = Menu()

    # Spuštění hlavní smyčky aplikace
    sys.exit(app.exec_())

if __name__ == '__main__':
    # Hlavní vstupní bod aplikace
    main()
