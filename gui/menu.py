from PyQt5.QtWidgets import QMainWindow, QAction, QVBoxLayout, QTableWidget, QTableWidgetItem, QMenu, QSystemTrayIcon, QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QDateTime
import psutil
import time
from utils.activity_tracker import ActivityTracker  # Import ActivityTracker
from utils.screenshot import ScreenshotTaker  # Import ScreenshotTaker

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Vytvoření instance ActivityTracker pro sledování aktivního okna
        self.activity_tracker = ActivityTracker()
        self.activity_tracker.windowChanged.connect(self.on_window_changed)

        # Slovník pro uchování časů aktivace a kumulované doby aktivace
        self.window_data = {}
        self.active_window = None
        self.active_start_time = None

        # Nastavení časovače pro aktualizaci každou sekundu
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_process_info)
        self.update_timer.start(1000)

        # Instance ScreenshotTaker a nastavení časovače pro screenshoty
        self.screenshot_taker = ScreenshotTaker()  # Třída z utils/screenshot.py
        self.screenshot_timer = QTimer(self)
        self.screenshot_timer.timeout.connect(self.take_screenshot)
        self.screenshot_timer.start(10000)  # 10000 ms = 10 sekund

    def initUI(self):
        # Ikona pro tray a menu
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icons/icon.png'))

        tray_menu = QMenu()  # Vytvoření menu pro tray ikonu
        showAct = QAction("Zobrazit", self)  # Akce pro zobrazení okna
        showAct.triggered.connect(self.show_window)
        tray_menu.addAction(showAct)

        exitAct = QAction("Ukončit", self)  # Akce pro ukončení aplikace
        exitAct.triggered.connect(self.exit_app)
        tray_menu.addAction(exitAct)

        self.tray_icon.setContextMenu(tray_menu)  # Nastavení menu pro tray ikonu
        self.tray_icon.show()  # Zobrazení tray ikony

        # Widget pro zobrazení tabulky s procesy
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Tabulka s informacemi o procesech
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)  # Počet sloupců upravený pro PID
        self.table_widget.setHorizontalHeaderLabels([
            "Název okna", "Poslední aktivace", "Doba aktivace", 
            "CPU", "RAM", "PID"
        ])
        layout.addWidget(self.table_widget)

        self.setWindowTitle("Sledování aktivit oken")  # Nastavení názvu okna
        self.resize(800, 600)  # Nastavení velikosti okna

    def take_screenshot(self):
        try:
            timestamp = QDateTime.currentDateTime().toString("yyyy.MM.dd-HH-mm-ss")
            filename = f"/tmp/"
            self.screenshot_taker.take_screenshot(filename)
        except Exception as e:
            print(f"Chyba při pořizování screenshotu: {e}")
            
    def exit_app(self):
        QApplication.instance().quit()  # Ukončení aplikace

    def show_window(self):
        self.show()  # Zobrazení okna
        self.raise_()  # Přenesení okna do popředí
        self.activateWindow()  # Aktivace okna

    def closeEvent(self, event):
        event.ignore()  # Ignorování události zavření okna
        self.hide()  # Skrytí okna
        self.tray_icon.showMessage(
            "Aplikace minimalizována",
            "TimeTracker běží na pozadí. Otevřete jej kliknutím na ikonu v systémové liště.",
            QSystemTrayIcon.Information,
            2000
        )

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

        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                pid = p.info['pid']
                process_name = p.info['name']
                cpu_usage = p.info['cpu_percent']
                ram_usage = p.info['memory_percent']

                if self.is_user_process(pid, process_name) and cpu_usage is not None and ram_usage is not None:
                    ram_usage = round(ram_usage, 2)

                    if process_name in processes:
                        processes[process_name]['cpu_percent'] += cpu_usage
                        processes[process_name]['memory_percent'] += ram_usage
                    else:
                        processes[process_name] = {
                            'name': process_name,
                            'cpu_percent': cpu_usage,
                            'memory_percent': ram_usage,
                            'pid': pid
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
            if proc.username() == 'root' or proc.status() == psutil.STATUS_ZOMBIE or not proc.is_running():
                return False
        except psutil.AccessDenied:
            return False
        return True
