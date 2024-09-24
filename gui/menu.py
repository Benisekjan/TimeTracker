from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QVBoxLayout, QWidget, QGroupBox, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime, QTimer, QObject, pyqtSignal, QThread, pyqtSlot
from utils.activity_tracker import ActivityTracker

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Seznamy pro ukládání aktivních a neaktivních období
        self.active_periods = []
        self.inactive_periods = []
        self.current_activity_start = None  # Ukládá čas začátku aktuální aktivity
        self.current_inactivity_start = None  # Ukládá čas začátku aktuální neaktivity

        # Vytvoření instance třídy ActivityTracker, která sleduje aktivitu
        self.activity_tracker = ActivityTracker()
        # Připojení signálů ze sledovače aktivit k funkcím pro zpracování změn
        self.activity_tracker.activityChanged.connect(self.handle_activity_change)
        self.activity_tracker.windowChanged.connect(self.handle_window_change)

    def initUI(self):
        # Vytvoření akce pro ukončení aplikace
        exitAct = QAction(QIcon('exit.png'), '&Quit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.instance().quit)

        # Vytvoření menu
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        # Přidání položek do menu
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction('New')

        # Nastavení okna aplikace
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Simple menu')

        # Vytvoření widgetu pro zobrazení aktivity
        self.create_activity_widget()

    def create_activity_widget(self):
        # Widget, který zobrazuje aktivitu
        activity_widget = QWidget(self)
        self.setCentralWidget(activity_widget)

        # Layout pro zobrazení obsahu
        vbox = QVBoxLayout(activity_widget)
        groupbox = QGroupBox("Activity Tracker", activity_widget)
        vbox.addWidget(groupbox)

        # Štítek pro zobrazení informací o aktivitě
        self.activity_label = QLabel("Tracking activity here...", groupbox)
        groupbox_layout = QVBoxLayout(groupbox)
        groupbox_layout.addWidget(self.activity_label)

    def handle_activity_change(self, active):
        # Zpracování změny aktivity (aktivní/neaktivní)
        current_time = QDateTime.currentDateTime()  # Získá aktuální čas
        if active:
            # Pokud uživatel začne být aktivní
            if self.current_inactivity_start is not None:
                # Pokud bylo předtím neaktivní období, zaznamená ho
                if self.current_inactivity_start != current_time:
                    self.inactive_periods.append(
                        f"Inactive from {self.current_inactivity_start.toString('hh:mm:ss')} to {current_time.toString('hh:mm:ss')}"
                    )
                self.current_inactivity_start = None  # Resetuje čas začátku neaktivity
            self.current_activity_start = current_time  # Uloží čas začátku aktivity
        else:
            # Pokud uživatel přestane být aktivní
            if self.current_activity_start is not None:
                # Pokud bylo předtím aktivní období, zaznamená ho
                if self.current_activity_start != current_time:
                    self.active_periods.append(
                        f"Active from {self.current_activity_start.toString('hh:mm:ss')} to {current_time.toString('hh:mm:ss')}"
                    )
                self.current_activity_start = None  # Resetuje čas začátku aktivity
                self.current_inactivity_start = current_time  # Uloží čas začátku neaktivity

        self.update_display()  # Aktualizuje zobrazení aktivity

    def handle_window_change(self, window_name):
        # Zpracování změny aktivního okna
        current_time = QDateTime.currentDateTime()  # Získá aktuální čas
        # Zaznamená změnu okna do seznamu aktivních období
        self.active_periods.append(
            f"Window changed to {window_name} at {current_time.toString('hh:mm:ss')}"
        )
        self.update_display()  # Aktualizuje zobrazení aktivity

    def update_display(self):
        # Zobrazení seznamu aktivních a neaktivních období v rozhraní
        active_periods_str = "\n".join(self.active_periods)  # Převede seznam aktivních období na text
        inactive_periods_str = "\n".join(self.inactive_periods)  # Převede seznam neaktivních období na text

        # Kombinuje oba seznamy do textu, který se zobrazí na štítku
        activity_text = f"Active periods:\n{active_periods_str}\n\nInactive periods:\n{inactive_periods_str}"
        self.activity_label.setText(activity_text)  # Zobrazí text na štítku
