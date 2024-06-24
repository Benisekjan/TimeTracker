from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QVBoxLayout, QWidget, QGroupBox, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QDateTime
from Foundation import NSWorkspace
from AppKit import NSWorkspaceDidActivateApplicationNotification, NSWorkspaceDidDeactivateApplicationNotification
from utils.activity_tracker import ActivityTracker

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.active_periods = []
        self.inactive_periods = []
        self.current_activity_start = None
        self.current_inactivity_start = None
        self.active = False
        self.inactivity_timer = QTimer()
        self.inactivity_timer.setInterval(3000)  # 3 sekundy
        self.inactivity_timer.timeout.connect(self.check_inactivity)
        self.inactivity_timer.start()

        self.activity_tracker = ActivityTracker()
        self.activity_tracker.activityChanged.connect(self.handle_activity_change)
        self.activity_tracker.start()

    def initUI(self):
        exitAct = QAction(QIcon('exit.png'), '&Quit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.instance().quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction('New')

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Simple menu')
        self.show()

        self.create_activity_widget()

    def create_activity_widget(self):
        activity_widget = QWidget(self)
        self.setCentralWidget(activity_widget)

        vbox = QVBoxLayout(activity_widget)
        groupbox = QGroupBox("Activity Tracker", activity_widget)
        vbox.addWidget(groupbox)

        self.activity_label = QLabel("Tracking activity here...", groupbox)
        groupbox_layout = QVBoxLayout(groupbox)
        groupbox_layout.addWidget(self.activity_label)

    def update_display(self):
        active_periods_str = "\n".join(self.active_periods)
        inactive_periods_str = "\n".join(self.inactive_periods)

        activity_text = f"Aktivní období:\n{active_periods_str}\n\nNeaktivní období:\n{inactive_periods_str}"
        self.activity_label.setText(activity_text)

    def handle_activity_change(self, active):
        current_time = QDateTime.currentDateTime()
        if active:
            if self.current_inactivity_start is not None:
                self.inactive_periods.append(
                    f"neaktivní od {self.current_inactivity_start.toString('hh:mm:ss')} do {current_time.toString('hh:mm:ss')}"
                )
                self.current_inactivity_start = None
            self.current_activity_start = current_time
        else:
            if self.current_activity_start is not None:
                self.active_periods.append(
                    f"aktivní od {self.current_activity_start.toString('hh:mm:ss')} do {current_time.toString('hh:mm:ss')}"
                )
                self.current_activity_start = None
            self.current_inactivity_start = current_time

        self.update_display()

    def check_inactivity(self):
        if self.active:
            current_time = QDateTime.currentDateTime()
            self.active = False
            if self.current_activity_start is not None:
                self.active_periods.append(
                    f"aktivní od {self.current_activity_start.toString('hh:mm:ss')} do {current_time.toString('hh:mm:ss')}"
                )
                self.current_activity_start = None
                self.current_inactivity_start = current_time
                self.update_display()

    def applicationActivated_(self, notification):
        if not self.active:
            self.active = True
            if self.current_inactivity_start is not None:
                current_time = QDateTime.currentDateTime()
                self.inactive_periods.append(
                    f"neaktivní od {self.current_inactivity_start.toString('hh:mm:ss')} do {current_time.toString('hh:mm:ss')}"
                )
                self.current_inactivity_start = None
            self.current_activity_start = QDateTime.currentDateTime()
            self.update_display()

    def applicationDeactivated_(self, notification):
        if self.active:
            self.active = False
            current_time = QDateTime.currentDateTime()
            self.active_periods.append(
                f"aktivní od {self.current_activity_start.toString('hh:mm:ss')} do {current_time.toString('hh:mm:ss')}"
            )
            self.current_activity_start = None
            self.current_inactivity_start = current_time
            self.update_display()
