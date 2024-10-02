from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QVBoxLayout, QGridLayout, QWidget, QGroupBox, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime, Qt
from utils.activity_tracker import ActivityTracker
import psutil

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()  # Inicializace uživatelského rozhraní

        self.window_periods = []  # Seznam pro uchování období oken
        self.current_window_start = None  # Počáteční čas aktuálního okna
        self.current_window_name = ""  # Název aktuálního okna

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
        self.disk_label = QLabel("Disk Usage", groupbox)

        # Zarovnání pro hlavičky
        self.window_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.activation_time_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.duration_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.cpu_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.ram_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.disk_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Přidání hlavičkových labelů do gridu
        self.grid_layout.addWidget(self.window_label, 0, 0)
        self.grid_layout.addWidget(self.activation_time_label, 0, 1)
        self.grid_layout.addWidget(self.duration_label, 0, 2)
        self.grid_layout.addWidget(self.cpu_label, 0, 3)
        self.grid_layout.addWidget(self.ram_label, 0, 4)
        self.grid_layout.addWidget(self.disk_label, 0, 5)

        # Nastavení rozestupů
        self.grid_layout.setAlignment(Qt.AlignTop)

        # Seznamy pro uchování detailů aktivit okna
        self.window_labels = []  # Seznam pro názvy oken
        self.activation_time_labels = []  # Seznam pro časy aktivace
        self.duration_labels = []  # Seznam pro trvání aktivit
        self.cpu_labels_list = []  # Seznam pro CPU
        self.ram_labels_list = []  # Seznam pro RAM
        self.disk_labels_list = []  # Seznam pro disk

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
            disk_info = psutil.disk_usage('/')

            # Přidání detailů předchozího okna do zobrazení
            window_label = QLabel(self.current_window_name)
            activation_time_label = QLabel(self.current_window_start.toString('hh:mm:ss'))
            duration_label = QLabel(previous_window_duration)
            cpu_label = QLabel(f"{cpu_usage}%")
            ram_label = QLabel(f"{ram_info.percent}%")
            disk_label = QLabel(f"{disk_info.percent}%")

            # Nastavení zarovnání pro každý label
            window_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            activation_time_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            duration_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            cpu_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            ram_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            disk_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

            # Přidání do gridu na další dostupný řádek
            row = len(self.window_labels) + 1  # +1 pro hlavičkový řádek
            self.grid_layout.addWidget(window_label, row, 0)
            self.grid_layout.addWidget(activation_time_label, row, 1)
            self.grid_layout.addWidget(duration_label, row, 2)
            self.grid_layout.addWidget(cpu_label, row, 3)
            self.grid_layout.addWidget(ram_label, row, 4)
            self.grid_layout.addWidget(disk_label, row, 5)

            # Přidání labelů do příslušných seznamů (volitelné)
            self.window_labels.append(window_label)
            self.activation_time_labels.append(activation_time_label)
            self.duration_labels.append(duration_label)
            self.cpu_labels_list.append(cpu_label)
            self.ram_labels_list.append(ram_label)
            self.disk_labels_list.append(disk_label)

        # Aktualizace aktuálního okna a jeho času spuštění
        self.current_window_name = window_name
        self.current_window_start = current_time
