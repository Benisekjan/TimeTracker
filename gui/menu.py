from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QVBoxLayout, QWidget, QGroupBox, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime
from utils.activity_tracker import ActivityTracker

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.active_periods = []
        self.current_window_start = None
        self.current_window = None

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

        vbox = QVBoxLayout(activity_widget)
        groupbox = QGroupBox("Activity Tracker", activity_widget)
        vbox.addWidget(groupbox)

        self.activity_label = QLabel("Tracking window changes...", groupbox)
        groupbox_layout = QVBoxLayout(groupbox)
        groupbox_layout.addWidget(self.activity_label)

    def handle_window_change(self, window_name):
        current_time = QDateTime.currentDateTime()

        # Zaznamenat konec předchozího okna, pokud existuje
        if self.current_window is not None:
            self.active_periods.append(
                f"Window active {self.current_window} from {self.current_window_start.toString('hh:mm:ss')} to {current_time.toString('hh:mm:ss')}"
            )

        # Aktualizovat aktuální okno
        self.current_window = window_name
        self.current_window_start = current_time

        # Zaznamenat změnu okna
        self.active_periods.append(
            f"Window changed to {window_name} at {current_time.toString('hh:mm:ss')}"
        )

        self.update_display()

    def update_display(self):
        active_periods_str = "\n".join(self.active_periods)
        activity_text = f"Window periods:\n{active_periods_str}"
        self.activity_label.setText(activity_text)
