from PyQt5.QtWidgets import QApplication
from gui.menu import Menu  # Import hlavní třídy okna z modulu menu
import sys
from setproctitle import setproctitle  

title = "TimeTracker"
setproctitle(title)

def main():
    # Vytvoření instance aplikace PyQt
    app = QApplication(sys.argv)

    # Vytvoření hlavního okna aplikace
    window = Menu()
    
    # Zobrazení okna
    window.show()

    # Spuštění hlavní smyčky aplikace
    sys.exit(app.exec_())

if __name__ == '__main__':
    # Hlavní vstupní bod aplikace
    main()
