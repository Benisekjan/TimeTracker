from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QVBoxLayout, QGridLayout, QWidget, QGroupBox, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime, Qt
from utils.activity_tracker import ActivityTracker
import psutil

class Menu(QMainWindow):
    
    MAX_RECORDS = 30  # Maximální počet záznamů, které se zobrazují

    def __init__(self):
        super().__init__()
        self.initUI()  # Inicializace uživatelského rozhraní

        self.current_window_start = None  # Počáteční čas aktuálního okna

        self.activity_tracker = ActivityTracker()  # Inicializace sledovače aktivit
        self.activity_tracker.windowChanged.connect(self.handle_window_change)  # Připojení signálu ke slotu

    def initUI(self):
        # Vytvoření akce pro ukončení aplikace
        exitAct = QAction(QIcon('exit.png'), '&Quit', self)
        exitAct.setShortcut('Ctrl+Q')  # Nastavení klávesové zkratky
        exitAct.setStatusTip('Exit application')  # Nastavení popisku
        exitAct.triggered.connect(QApplication.instance().quit)  # Připojení akce k ukončení aplikace

        menubar = self.menuBar()  # Vytvoření menu baru
        menubar.setNativeMenuBar(False)  # Nastavení nativního menu baru na False

        fileMenu = menubar.addMenu('&File')  # Přidání položky File do menu baru
        fileMenu.addAction(exitAct)  # Přidání akce do položky File

        self.setGeometry(100, 100, 800, 600)  # Nastavení velikosti a pozice okna
        self.setWindowTitle('Time Tracker')  # Nastavení titulku okna

        self.create_activity_widget()  # Vytvoření widgetu pro sledování aktivit

    def create_activity_widget(self):
        activity_widget = QWidget(self)  # Vytvoření hlavního widgetu
        self.setCentralWidget(activity_widget)  # Nastavení hlavního widgetu jako centrálního

        layout = QVBoxLayout(activity_widget)  # Vytvoření vertikálního layoutu
        layout.setContentsMargins(20, 0, 20, 20)  # Nastavení okrajů kolem layoutu
        groupbox = QGroupBox("Window Activity Tracker", activity_widget)  # Vytvoření groupboxu
        layout.addWidget(groupbox)  # Přidání groupboxu do layoutu

        self.grid_layout = QGridLayout(groupbox)  # Vytvoření grid layoutu uvnitř groupboxu

        # Přidání hlaviček do gridu
        self.window_label = QLabel("Window Name", groupbox)
        self.activation_time_label = QLabel("Activation Time", groupbox)
        self.duration_label = QLabel("Active Duration", groupbox)
        self.cpu_label = QLabel("CPU Usage", groupbox)
        self.ram_label = QLabel("RAM Usage", groupbox)

        # Zarovnání pro hlavičky
        for label in [self.window_label, self.activation_time_label, self.duration_label, 
                      self.cpu_label, self.ram_label]:
            label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Přidání hlavičkových labelů do gridu
        self.grid_layout.addWidget(self.window_label, 0, 0)
        self.grid_layout.addWidget(self.activation_time_label, 0, 1)
        self.grid_layout.addWidget(self.duration_label, 0, 2)
        self.grid_layout.addWidget(self.cpu_label, 0, 3)
        self.grid_layout.addWidget(self.ram_label, 0, 4)

        # Nastavení rozestupů
        self.grid_layout.setAlignment(Qt.AlignTop)

        # Seznamy pro uchování detailů aktivit okna
        self.window_labels = []  # Seznam pro názvy oken
        self.activation_time_labels = []  # Seznam pro časy aktivace
        self.duration_labels = []  # Seznam pro trvání aktivit
        self.cpu_labels_list = []  # Seznam pro CPU
        self.ram_labels_list = []  # Seznam pro RAM

    def handle_window_change(self, window_name):
        current_time = QDateTime.currentDateTime()  # Získání aktuálního času

        if self.current_window_start is not None:
            # Výpočet trvání předchozího okna
            previous_window_duration = (
                f"{self.current_window_start.toString('hh:mm:ss')} to {current_time.toString('hh:mm:ss')}"
            )

            # Získání systémových prostředků
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_info = psutil.virtual_memory()

            # Přidání detailů předchozího okna do zobrazení
            window_label = QLabel(window_name)
            activation_time_label = QLabel(self.current_window_start.toString('hh:mm:ss'))
            duration_label = QLabel(previous_window_duration)
            cpu_label = QLabel(f"{cpu_usage}%")
            ram_label = QLabel(f"{ram_info.percent}%")

            # Přidání do gridu na další dostupný řádek
            row = len(self.window_labels) + 1  # +1 pro hlavičkový řádek
            self.grid_layout.addWidget(window_label, row, 0)
            self.grid_layout.addWidget(activation_time_label, row, 1)
            self.grid_layout.addWidget(duration_label, row, 2)
            self.grid_layout.addWidget(cpu_label, row, 3)
            self.grid_layout.addWidget(ram_label, row, 4)

            # Přidání labelů do příslušných seznamů
            self.window_labels.append(window_label)
            self.activation_time_labels.append(activation_time_label)
            self.duration_labels.append(duration_label)
            self.cpu_labels_list.append(cpu_label)
            self.ram_labels_list.append(ram_label)

            # Omezit počet záznamů na MAX_RECORDS
            if len(self.window_labels) > self.MAX_RECORDS:
                # Odebrání nejstaršího záznamu z gridu a seznamů
                self.grid_layout.removeWidget(self.window_labels[0])
                self.grid_layout.removeWidget(self.activation_time_labels[0])
                self.grid_layout.removeWidget(self.duration_labels[0])
                self.grid_layout.removeWidget(self.cpu_labels_list[0])
                self.grid_layout.removeWidget(self.ram_labels_list[0])

                # Odebrání prvního záznamu ze seznamu
                self.window_labels.pop(0)
                self.activation_time_labels.pop(0)
                self.duration_labels.pop(0)
                self.cpu_labels_list.pop(0)
                self.ram_labels_list.pop(0)

        # Aktualizace aktuálního okna a jeho času spuštění
        self.current_window_start = current_time


# Hlavní program
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    menu = Menu()
    menu.show()
    sys.exit(app.exec_())
