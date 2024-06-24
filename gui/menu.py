import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QLabel, QVBoxLayout, QWidget, QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime
from utils.activity_tracker import ActivityTracker
from PyObjCTools import AppHelper

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.active_periods = []
        self.inactive_periods = []
        self.current_activity_start = None
        self.current_inactivity_start = None

        self.activity_tracker = ActivityTracker()
        self.activity_tracker.activityChanged.connect(self.handle_activity_change)

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

        self.create_activity_widget()
        self.show()

    def create_activity_widget(self):
        activity_widget = QWidget(self)
        self.setCentralWidget(activity_widget)

        vbox = QVBoxLayout(activity_widget)
        groupbox = QGroupBox("Activity Tracker", activity_widget)
        vbox.addWidget(groupbox)

        self.activity_label = QLabel("Tracking activity here...", groupbox)
        groupbox_layout = QVBoxLayout(groupbox)
        groupbox_layout.addWidget(self.activity_label)

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
                self.current_inactivity_start = current_time

        self.update_display()

    def update_display(self):
        active_periods_str = "\n".join(self.active_periods)
        inactive_periods_str = "\n".join(self.inactive_periods)

        activity_text = f"Aktivní období:\n{active_periods_str}\n\nNeaktivní období:\n{inactive_periods_str}"
        self.activity_label.setText(activity_text)

    def main(self):
        self.activity_tracker.start()  # Start activity tracking
        AppHelper.runEventLoop()  # Start PyQt event loop
        self.activity_tracker.stop()  # Stop activity tracking

