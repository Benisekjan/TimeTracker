from PyQt5.QtWidgets import QApplication, QMessageBox
from gui.menu import Menu  # Import hlavní třídy okna z modulu menu
import sys
import os
import plistlib
from pathlib import Path
from setproctitle import setproctitle  

title = "TimeTracker"
setproctitle(title)

# Cesta k souboru, který bude uchovávat informace o nastavení
settings_file = Path.home() / '.timetracker_settings'

# Funkce pro vytvoření souboru .plist pro automatické spuštění
def create_launch_agent():
    plist_path = Path.home() / 'Library/LaunchAgents/com.timetracker.startup.plist'
    
    # Cesta k aplikaci
    app_path = os.path.join(os.path.dirname(__file__), 'TimeTracker.app/Contents/MacOS/TimeTracker')

    if not plist_path.exists():
        plist = {
            'Label': 'com.timetracker.startup',
            'ProgramArguments': [
                app_path,
            ],
            'RunAtLoad': True,
        }
        with plist_path.open('wb') as plist_file:
            plistlib.dump(plist, plist_file)
        print("TimeTracker bude spuštěn při startu systému.")
    else:
        print("TimeTracker již byl nastaven na spuštění při startu.")

# Funkce pro zobrazení dotazu na automatické spuštění
def ask_user(app):
    # Pokud soubor nastavení neexistuje (první spuštění), zeptáme uživatele
    if not settings_file.exists():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Chcete, aby se aplikace TimeTracker spouštěla při startu systému?")
        msg.setWindowTitle("Automatické spuštění")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # Zobrazení dialogu a získání odpovědi
        answer = msg.exec_()

        if answer == QMessageBox.Yes:
            create_launch_agent()

        # Uložení informací, že uživatel odpověděl na tuto otázku
        with open(settings_file, 'w') as f:
            f.write('setup_completed')  # Indikace, že uživatel souhlasil s nastavením

def main():
    # Vytvoření instance aplikace PyQt
    app = QApplication(sys.argv)

    # Zobrazí dotaz na automatické spuštění, pokud to je první spuštění
    ask_user(app)

    # Vytvoření hlavního okna aplikace
    window = Menu()
    
    # Zobrazení okna
    window.show()

    # Spuštění hlavní smyčky aplikace
    sys.exit(app.exec_())

if __name__ == '__main__':
    # Hlavní vstupní bod aplikace
    main()
