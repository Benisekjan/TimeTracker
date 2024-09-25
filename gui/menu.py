from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QVBoxLayout, QGridLayout, QWidget, QGroupBox, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime, Qt
from utils.activity_tracker import ActivityTracker

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.window_periods = []
        self.current_window_start = None
        self.current_window_name = ""

        self.activity_tracker = ActivityTracker()
        self.activity_tracker.windowChanged.connect(self.handle_window_change)

    def initUI(self):
        exitAct = QAction(QIcon('exit.png'), '&Quit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.instance().quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Simple menu')

        self.create_activity_widget()

    def create_activity_widget(self):
        activity_widget = QWidget(self)
        self.setCentralWidget(activity_widget)

        layout = QVBoxLayout(activity_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Odstranit okraje kolem rozložení
        groupbox = QGroupBox("Window Activity Tracker", activity_widget)
        layout.addWidget(groupbox)

        self.grid_layout = QGridLayout(groupbox)

        # Přidání hlaviček do gridu
        self.window_label = QLabel("Window Name", groupbox)
        self.activation_time_label = QLabel("Activation Time", groupbox)
        self.duration_label = QLabel("Active Duration", groupbox)

        # Zarovnání pro hlavičky
        self.window_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.activation_time_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.duration_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Přidání hlavičkových labelů do gridu
        self.grid_layout.addWidget(self.window_label, 0, 0)
        self.grid_layout.addWidget(self.activation_time_label, 0, 1)
        self.grid_layout.addWidget(self.duration_label, 0, 2)

        # Nastavení rozestupů
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(5)  # Mírné vertikální rozestupy

        # Seznamy pro uchování detailů aktivit okna
        self.window_labels = []  
        self.activation_time_labels = []  
        self.duration_labels = []  

    def handle_window_change(self, window_name):
        current_time = QDateTime.currentDateTime()

        if self.current_window_start is not None:
            previous_window_duration = (
                f"{self.current_window_start.toString('hh:mm:ss')} to {current_time.toString('hh:mm:ss')}"
            )

            # Přidání detailů předchozího okna do zobrazení
            window_label = QLabel(self.current_window_name)
            activation_time_label = QLabel(self.current_window_start.toString('hh:mm:ss'))
            duration_label = QLabel(previous_window_duration)

            # Nastavení zarovnání pro každý label
            window_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            activation_time_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            duration_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

            # Přidání do gridu na další dostupný řádek
            row = len(self.window_labels) + 1  # +1 pro hlavičkový řádek
            self.grid_layout.addWidget(window_label, row, 0)
            self.grid_layout.addWidget(activation_time_label, row, 1)
            self.grid_layout.addWidget(duration_label, row, 2)

            # Přidání labelů do příslušných seznamů (volitelné)
            self.window_labels.append(window_label)
            self.activation_time_labels.append(activation_time_label)
            self.duration_labels.append(duration_label)

        # Aktualizace aktuálního okna a jeho času spuštění
        self.current_window_name = window_name
        self.current_window_start = current_time

    def update_display(self):
        pass  # Není třeba dalších aktualizací zobrazení
