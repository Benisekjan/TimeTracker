from PyQt5.QtWidgets import QMainWindow, QAction, QVBoxLayout, QTableWidget, QTableWidgetItem, QMenu, QSystemTrayIcon, QApplication, QWidget, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QDateTime
import psutil  # Knihovna pro práci s procesy a systémovými informacemi
import time  # Knihovna pro práci s časem
from utils.activity_tracker import ActivityTracker  # Import třídy pro sledování aktivit
from utils.screenshot import ScreenshotManager  # Import třídy pro správu screenshotů
from gui.settings import SettingsDialog  # Dialog pro uživatelské nastavení
import os  # Práce se soubory a složkami
import csv  # Práce s CSV soubory
import sys  # Knihovna pro práci se systémem

class Menu(QMainWindow):  # Třída hlavního okna aplikace
    def __init__(self):
        super().__init__()
        self.initUI()  # Inicializace uživatelského rozhraní

        # Inicializace ScreenshotManager a výchozích složek
        self.screenshot_manager = ScreenshotManager()  # Správce screenshotů
        self.screenshot_directory = self.screenshot_manager.screenshot_directory  # Výchozí složka screenshotů
        self.csv_directory = "/tmp/csv_logs"  # Výchozí složka pro CSV logy
        os.makedirs(self.csv_directory, exist_ok=True)  # Vytvoření složky pro CSV, pokud neexistuje

        # Inicializace CSV souboru
        self.csv_file = os.path.join(self.csv_directory, "activity_log.csv")  # Cesta k CSV souboru

        # Inicializace sledování aktivit
        self.activity_tracker = ActivityTracker()  # Objekt pro sledování změn oken
        self.activity_tracker.windowChanged.connect(self.on_window_changed)  # Připojení signálu ke změně aktivního okna

        self.window_data = {}  # Slovník pro ukládání dat o oknech
        self.active_window = None  # Aktuálně aktivní okno
        self.active_start_time = None  # Čas, kdy bylo okno aktivováno

        # Nastavení časovačů
        self.update_timer = QTimer(self)  # Časovač pro aktualizaci informací o procesech
        self.update_timer.timeout.connect(self.update_process_info)  # Připojení časovače k metodě aktualizace
        self.update_timer.start(1000)  # Spuštění časovače každou sekundu

        self.screenshot_timer = QTimer(self)  # Časovač pro pořizování screenshotů
        self.screenshot_timer.timeout.connect(self.take_screenshot)  # Připojení k metodě pořizování screenshotů
        self.screenshot_timer.start(300000)  # Spuštění každých 5 minut (300 000 ms)

        self.csv_timer = QTimer(self)  # Časovač pro zápis do CSV
        self.csv_timer.timeout.connect(self.write_to_csv)  # Připojení k metodě zápisu do CSV
        self.csv_timer.start(300000)  # Spuštění každých 5 minut (300 000 ms)

    def initUI(self):  # Inicializace uživatelského rozhraní
        
        # Nastavení cesty k ikoně
        if hasattr(sys, "_MEIPASS"):  # Kontrola, zda běžíme v zabalené aplikaci
            icon_path = os.path.join(sys._MEIPASS, 'icons', 'icon.icns')
        else:  # Pokud aplikace běží ze zdrojového kódu
            icon_path = 'icons/icon.icns'
        
        # Ikona pro tray a menu
        self.tray_icon = QSystemTrayIcon(self)  # Ikona aplikace v systémové liště
        self.tray_icon.setIcon(QIcon(icon_path)) # Nastavení ikony pro aplikaci

        tray_menu = QMenu()  # Vytvoření menu pro tray ikonu
        showAct = QAction("Zobrazit", self)  # Akce pro zobrazení hlavního okna
        showAct.triggered.connect(self.show_window)  # Připojení akce k metodě zobrazení okna
        tray_menu.addAction(showAct)  # Přidání akce do menu

        exitAct = QAction("Ukončit", self)  # Akce pro ukončení aplikace
        exitAct.triggered.connect(self.exit_app)  # Připojení akce k metodě ukončení aplikace
        tray_menu.addAction(exitAct)  # Přidání akce do menu
        
        settingsAct = QAction("Nastavení", self)  # Akce pro otevření dialogu nastavení
        settingsAct.triggered.connect(self.open_settings)  # Připojení akce k metodě otevření dialogu
        tray_menu.addAction(settingsAct)  # Přidání akce do menu

        self.tray_icon.setContextMenu(tray_menu)  # Nastavení menu pro tray ikonu
        self.tray_icon.show()  # Zobrazení tray ikony

        # Widget pro zobrazení tabulky s procesy
        central_widget = QWidget(self)  # Vytvoření centrálního widgetu pro hlavní okno
        self.setCentralWidget(central_widget)  # Nastavení centrálního widgetu
        layout = QVBoxLayout(central_widget)  # Layout pro central_widget
        
        # Tabulka s informacemi o procesech
        self.table_widget = QTableWidget()  # Tabulka pro zobrazení dat
        self.table_widget.setColumnCount(7)  # Nastavení počtu sloupců
        self.table_widget.setHorizontalHeaderLabels([
            "Název okna", "Poslední aktivace", "Doba aktivace", 
            "CPU", "RAM", "PID", "Uživatel"
        ])  # Hlavička tabulky
        layout.addWidget(self.table_widget)  # Přidání tabulky do layoutu

        self.setWindowTitle("Sledování aktivit oken")  # Nastavení názvu hlavního okna
        self.resize(800, 600)  # Nastavení velikosti okna

    def open_settings(self):  # Metoda pro otevření dialogu nastavení
        dialog = SettingsDialog(  # Vytvoření dialogu pro nastavení
            parent=self,  # Rodičovské okno
            tracking_interval=self.update_timer.interval() // 1000,  # Aktuální interval sledování (v sekundách)
            screenshot_interval=self.screenshot_timer.interval() // 60000,  # Interval screenshotů (v minutách)
            csv_interval=self.csv_timer.interval() // 60000,  # Interval CSV (v minutách)
            screenshot_path=self.screenshot_directory,  # Výchozí složka screenshotů
            csv_path=self.csv_directory  # Výchozí složka pro CSV
        )

        if dialog.exec_() == QDialog.Accepted:  # Pokud uživatel potvrdil nastavení
            settings = dialog.get_settings()  # Načtení nových nastavení

            # Aktualizace časovačů na základě uživatelských nastavení
            self.update_timer.setInterval(settings["tracking_interval"] * 1000)  # Aktualizace intervalu sledování
            self.screenshot_timer.setInterval(settings["screenshot_interval"] * 60000)  # Aktualizace intervalu screenshotů
            self.csv_timer.setInterval(settings["csv_interval"] * 60000)  # Aktualizace intervalu CSV

            # Aktualizace složek
            self.screenshot_manager.set_screenshot_directory(settings["screenshot_path"])  # Nastavení nové složky pro screenshoty
            self.screenshot_directory = settings["screenshot_path"]  # Aktualizace výchozí složky screenshotů
            self.csv_directory = settings["csv_path"]  # Aktualizace výchozí složky pro CSV

            # Výpis informací o nových nastaveních
            print(f"Nové nastavení: Sledování každých {settings['tracking_interval']} sekund, "
                  f"screenshoty každých {settings['screenshot_interval']} minut do {self.screenshot_directory}, "
                  f"CSV každých {settings['csv_interval']} minut do {self.csv_directory}")


    def take_screenshot(self):
        # Pořídí screenshot pomocí ScreenshotManager
        try:
            self.screenshot_manager.take_screenshot()  # Zavolá metodu pro pořízení screenshotu
        except Exception as e:
            print(f"Chyba při pořizování screenshotu: {e}")  # Vypíše chybu do konzole, pokud něco selže
            
    def exit_app(self):
        QApplication.instance().quit()  # Ukončí běžící instanci aplikace PyQt

    def show_window(self):
        self.show()  # Zobrazí hlavní okno aplikace
        self.raise_()  # Přenese okno do popředí
        self.activateWindow()  # Aktivuje okno

    def closeEvent(self, event):
        event.ignore()  # Ignoruje akci zavření okna
        self.hide()  # Skryje okno místo jeho zavření
        self.tray_icon.showMessage(
            "Aplikace minimalizována",  # Zpráva o minimalizaci
            "TimeTracker běží na pozadí. Otevřete jej kliknutím na ikonu v systémové liště.",  # Detail zprávy
            QSystemTrayIcon.Information,  # Typ zprávy
            2000  # Délka zobrazení zprávy v milisekundách
        )
        
    def write_to_csv(self):
        self.csv_file = os.path.join(self.csv_directory, "activity_log.csv")  # Nastaví cestu k CSV souboru

        # Připraví data k zápisu do CSV
        active_data = [
            (window, data['total_duration'])  # Každé okno a jeho celková doba aktivity
            for window, data in self.window_data.items()
            if data['total_duration'] > 0  # Pouze okna s nějakou aktivitou
        ]

        if not active_data:
            return  # Pokud nejsou žádná aktivní data, nic se nezapisuje

        file_exists = os.path.isfile(self.csv_file)  # Kontrola, zda soubor již existuje

        current_values = self.read_csv()  # Načte stávající hodnoty z CSV

        with open(self.csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["Aplikace", "Čas (s)"])  # Zapisuje hlavičku pouze při prvním vytvoření souboru

            for window, duration in active_data:
                updated_duration = current_values.get(window, 0.0) + duration  # Přičte k existujícím hodnotám
                updated_duration = round(updated_duration)  # Zaokrouhlí na celé číslo
                writer.writerow([window, updated_duration])  # Zapíše řádek do CSV

        print(f"Data zapsána do {self.csv_file}")  # Vypíše potvrzení o zápisu
    
    
    def read_csv(self):
        if not os.path.isfile(self.csv_file):
            return {}  # Pokud soubor neexistuje, vrací prázdný slovník

        current_data = {}
        with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Přeskočí hlavičku
            for row in reader:
                if len(row) == 2:
                    current_data[row[0]] = float(row[1])  # Uloží data do slovníku
        return current_data  # Vrací načtená data
    
    def on_window_changed(self, window_name):
        # Tato metoda se spustí při změně aktivního okna
        current_time = time.time()

        # Pokud je nové aktivní okno odlišné od posledního
        if window_name != self.active_window:
            # Pokud bylo nějaké okno aktivní, vypočteme dobu aktivace a přičteme ji do slovníku
            if self.active_window and self.active_window in self.window_data:
                elapsed_time = current_time - self.active_start_time
                self.window_data[self.active_window]['total_duration'] += elapsed_time

            # Nastavíme nové aktivní okno a začneme měřit dobu jeho aktivace
            if window_name in self.window_data:
                # Pokud už je okno zaznamenáno, aktualizujeme čas poslední aktivace
                self.window_data[window_name]['last_activation_time'] = QDateTime.currentDateTime().toString("hh:mm:ss")
                self.active_start_time = current_time
            else:
                # Pro nové okno vytvoříme záznam
                self.window_data[window_name] = {
                    'last_activation_time': QDateTime.currentDateTime().toString("hh:mm:ss"),
                    'total_duration': 0.0
                }
                self.active_start_time = current_time
            
            # Aktualizujeme aktivní okno
            self.active_window = window_name

        # Aktualizujeme tabulku
        self.update_process_info()
        
    def update_process_info(self):
        # Zakáže řazení během aktualizace, aby nedošlo k nekonzistencím
        self.table_widget.setSortingEnabled(False)
        self.table_widget.setRowCount(0)  # Vymaže stávající řádky
        processes = {}

        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'username']):
            try:
                pid = p.info['pid'] # Získání ID procesu
                process_name = p.info['name'] # Získání názvu procesu
                cpu_usage = p.info['cpu_percent'] # Získání procent využití CPU
                ram_usage = p.info['memory_percent'] # Získání procent využití RAM
                username = p.info['username'] or "Unknown"  # Získání uživatele

                if self.is_user_process(pid, process_name) and cpu_usage is not None and ram_usage is not None:
                    ram_usage = round(ram_usage, 2)

                    if process_name in processes:
                        processes[process_name]['cpu_percent'] += cpu_usage
                        processes[process_name]['memory_percent'] += ram_usage
                    else:
                        processes[process_name] = {
                            'name': process_name, # Uložení názvu 
                            'cpu_percent': cpu_usage, # Uložení procent CPU
                            'memory_percent': ram_usage, # Uložení procent RAM
                            'pid': pid, # Uložení ID uživatele
                            'username': username  # Uložení uživatele
                        }

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        for process_info in processes.values():
            row_position = self.table_widget.rowCount()  # Získání aktuální pozice řádku
            self.table_widget.insertRow(row_position)  # Vložení nového řádku

            if process_info['name'] in self.window_data:
                last_activation_time = self.window_data[process_info['name']]['last_activation_time']
                total_duration = self.window_data[process_info['name']]['total_duration']

                if process_info['name'] == self.active_window:
                    total_duration += time.time() - self.active_start_time
                total_duration = round(total_duration)
            else:
                last_activation_time = "--"
                total_duration = "--"

            # Nastavení všech sloupců pro aktuální řádek
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(process_info['name']))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(last_activation_time))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(f"{total_duration} s"))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(f"{process_info['cpu_percent']}%"))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem(f"{process_info['memory_percent']}%"))
            self.table_widget.setItem(row_position, 5, QTableWidgetItem(str(process_info['pid'])))
            self.table_widget.setItem(row_position, 6, QTableWidgetItem(process_info['username'])) 

        # Povolí řazení po aktualizaci tabulky
        self.table_widget.setSortingEnabled(True)

    def is_user_process(self, pid, process_name):
        # Seznam systémových procesů, které chceme ignorovat
        system_processes = [
            'kernel_task', 'launchd', 'syslogd', 'hidd', 'WindowServer', 'timed', 'usbmuxd', 'locationd',
            'UserEventAgent', 'universalaccessd', 'pboard', 'talagentd', 'ControlCenter', 'SystemUIServer',
            'distnoted', 'nsurlsessiond', 'mdnsresponder', 'appleeventsd', 'coreaudiod', 'symptomsd',
            'airportd', 'configd', 'sandboxd', 'iconservicesagent', 'fileproviderd', 'diskarbitrationd',
            'securityd', 'spindump', 'spotlightd', 'sysmond', 'analyticsd', 'trustd'
        ]
        if process_name.lower() in system_processes:
            return False

        try:
            proc = psutil.Process(pid)
            # Ignorování procesů se statusem ZOMBIE nebo neběžících
            if proc.status() == psutil.STATUS_ZOMBIE or not proc.is_running():
                return False

        except (psutil.AccessDenied, psutil.NoSuchProcess):
            # Přístup odepřen nebo proces již neexistuje
            return False

        return True