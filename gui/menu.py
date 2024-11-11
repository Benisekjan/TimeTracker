from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QVBoxLayout, QGridLayout, QWidget, QGroupBox, QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime, Qt
from utils.activity_tracker import ActivityTracker
import psutil

class Menu(QMainWindow):
    
    MAX_RECORDS = 10  # Maximální počet záznamů, které se zobrazují

    def __init__(self):
        super().__init__()
        self.initUI()  # Inicializace uživatelského rozhraní

        # Inicializace seznamů pro uložení údajů o aktivitách
        self.window_labels = []
        self.activation_time_labels = []
        self.duration_labels = []
        self.cpu_labels_list = []
        self.ram_labels_list = []
        self.disk_labels_list = []

        self.current_window_start = None  # Počáteční čas aktuálního okna
        self.current_window_name = ""  # Název aktuálního okna

        self.activity_tracker = ActivityTracker()  # Inicializace sledovače aktivit
        self.activity_tracker.windowChanged.connect(self.handle_window_change)  # Připojení signálu ke slotu

    def initUI(self):
        # Vytvoření akce pro ukončení aplikace
        exitAct = QAction(QIcon('exit.png'), '&Quit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.exit_app)

        # Vytvoření akce pro zobrazení okna
        showAct = QAction(QIcon('show.png'), '&Show', self)
        showAct.setStatusTip('Show application')
        showAct.triggered.connect(self.show_window)

        # Vytvoření systémové ikony
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icons/icon.png'))  

        # Vytvoření kontextového menu pro ikonu
        tray_menu = QMenu()
        tray_menu.addAction(showAct)  # Přidání akce pro zobrazení okna
        tray_menu.addAction(exitAct)  # Přidání akce pro ukončení aplikace

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.create_activity_widget()  # Zavolání metody pro vytvoření layoutu

    def create_activity_widget(self):
        # Vytvoření hlavního widgetu
        activity_widget = QWidget(self)
        self.setCentralWidget(activity_widget)

        layout = QVBoxLayout(activity_widget)  # Vytvoření vertikálního layoutu
        layout.setContentsMargins(20, 0, 20, 20)  # Nastavení okrajů kolem layoutu
        groupbox = QGroupBox("Window Activity Tracker", activity_widget)  # Vytvoření groupboxu
        layout.addWidget(groupbox)  # Přidání groupboxu do layoutu

        # Vytvoření grid layoutu uvnitř groupboxu a jeho přiřazení do objektu
        self.grid_layout = QGridLayout(groupbox)  # Zde je grid_layout inicializován

        # Přidání hlaviček do gridu
        self.window_label = QLabel("Window Name", groupbox)
        self.activation_time_label = QLabel("Activation Time", groupbox)
        self.duration_label = QLabel("Active Duration", groupbox)
        self.cpu_label = QLabel("CPU Usage", groupbox)
        self.ram_label = QLabel("RAM Usage", groupbox)
        self.disk_label = QLabel("Disk Usage", groupbox)

        self.grid_layout.setAlignment(Qt.AlignTop)


        # Zarovnání pro hlavičky
        self.window_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.activation_time_label.setAlignment(Qt.AlignTop)
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

    def exit_app(self):
        QApplication.instance().quit()

    def show_window(self):
        self.show()  # Zobrazí hlavní okno aplikace
        self.raise_()  # Přenese okno do popředí
        self.activateWindow()  # Aktivuje okno

    def closeEvent(self, event):
        #Když je okno zavřeno, aplikace se minimalizuje do systémové lišty.
        event.ignore()  # Zabrání úplnému zavření okna
        self.hide()  # Skryje hlavní okno aplikace
        self.tray_icon.showMessage(
            "Application Minimized", 
            "TimeTracker běží na pozadí. Otevřete jej kliknutím na ikonu v systémové liště.",
            QSystemTrayIcon.Information,
            2000
        )

    def handle_window_change(self, window_name):
        current_time = QDateTime.currentDateTime()

        if self.current_window_start is not None:
            # Vypočítá dobu trvání předchozího okna
            previous_window_duration = (
                f"{self.current_window_start.toString('hh:mm:ss')} to {current_time.toString('hh:mm:ss')}"
            )

            # Získá systémové zdroje
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')

            # Přidá detaily předchozího okna do zobrazení
            window_label = QLabel(self.current_window_name)
            activation_time_label = QLabel(self.current_window_start.toString('hh:mm:ss'))
            duration_label = QLabel(previous_window_duration)
            cpu_label = QLabel(f"{cpu_usage}%")
            ram_label = QLabel(f"{ram_info.percent}%")
            disk_label = QLabel(f"{disk_info.percent}%")

            # Zarovná každý label
            window_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            activation_time_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            duration_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            cpu_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            ram_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            disk_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

            # Přidá do grid layoutu
            row = len(self.window_labels) + 1
            self.grid_layout.addWidget(window_label, row, 0)
            self.grid_layout.addWidget(activation_time_label, row, 1)
            self.grid_layout.addWidget(duration_label, row, 2)
            self.grid_layout.addWidget(cpu_label, row, 3)
            self.grid_layout.addWidget(ram_label, row, 4)
            self.grid_layout.addWidget(disk_label, row, 5)

            # Uloží do seznamů
            self.window_labels.append(window_label)
            self.activation_time_labels.append(activation_time_label)
            self.duration_labels.append(duration_label)
            self.cpu_labels_list.append(cpu_label)
            self.ram_labels_list.append(ram_label)
            self.disk_labels_list.append(disk_label)

            # Omezí počet záznamů na MAX_RECORDS
            if len(self.window_labels) > self.MAX_RECORDS:
                # Odstraní nejstarší záznam
                self.remove_oldest_record()

        # Aktualizuje aktuální okno
        self.current_window_name = window_name
        self.current_window_start = current_time

    def remove_oldest_record(self):
        # Odstranění nejstaršího záznamu z gridu a seznamů
        self.grid_layout.removeWidget(self.window_labels[0])
        self.grid_layout.removeWidget(self.activation_time_labels[0])
        self.grid_layout.removeWidget(self.duration_labels[0])
        self.grid_layout.removeWidget(self.cpu_labels_list[0])
        self.grid_layout.removeWidget(self.ram_labels_list[0])
        self.grid_layout.removeWidget(self.disk_labels_list[0])

        self.window_labels[0].deleteLater()
        self.activation_time_labels[0].deleteLater()
        self.duration_labels[0].deleteLater()
        self.cpu_labels_list[0].deleteLater()
        self.ram_labels_list[0].deleteLater()
        self.disk_labels_list[0].deleteLater()

        self.window_labels.pop(0)
        self.activation_time_labels.pop(0)
        self.duration_labels.pop(0)
        self.cpu_labels_list.pop(0)
        self.ram_labels_list.pop(0)
        self.disk_labels_list.pop(0)

        # Aktualizace zobrazení gridu
        self.update_grid()

    def update_grid(self):
        # Aktualizace gridu po odstranění záznamu
        for i, label in enumerate(self.window_labels):
            self.grid_layout.addWidget(label, i + 1, 0)
            self.grid_layout.addWidget(self.activation_time_labels[i], i + 1, 1)
            self.grid_layout.addWidget(self.duration_labels[i], i + 1, 2)
            self.grid_layout.addWidget(self.cpu_labels_list[i], i + 1, 3)
            self.grid_layout.addWidget(self.ram_labels_list[i], i + 1, 4)
            self.grid_layout.addWidget(self.disk_labels_list[i], i + 1, 5)
