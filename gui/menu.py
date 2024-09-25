from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QVBoxLayout, QGridLayout, QWidget, QGroupBox, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime
from utils.activity_tracker import ActivityTracker

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.window_periods = []
        self.current_window_start = None

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
        groupbox = QGroupBox("Window Activity Tracker", activity_widget)
        layout.addWidget(groupbox)

        self.grid_layout = QGridLayout(groupbox)
        self.window_label = QLabel("Window Name", groupbox)
        self.activation_time_label = QLabel("Activation Time", groupbox)
        self.duration_label = QLabel("Active Duration", groupbox)

        # Adding headers to the grid
        self.grid_layout.addWidget(self.window_label, 0, 0)
        self.grid_layout.addWidget(self.activation_time_label, 0, 1)
        self.grid_layout.addWidget(self.duration_label, 0, 2)

        # Setting some spacing
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(10)

        self.window_labels = []  # List for window name labels
        self.activation_time_labels = []  # List for activation time labels
        self.duration_labels = []  # List for active duration labels

    def handle_window_change(self, window_name):
        current_time = QDateTime.currentDateTime()

        if self.current_window_start is not None:
            previous_window_duration = (
                f"{self.current_window_start.toString('hh:mm:ss')} to {current_time.toString('hh:mm:ss')}"
            )

            # Adding previous window details to the display
            window_label = QLabel(self.current_window_name, self)
            activation_time_label = QLabel(self.current_window_start.toString('hh:mm:ss'), self)
            duration_label = QLabel(previous_window_duration, self)

            # Append labels to their respective lists
            self.window_labels.append(window_label)
            self.activation_time_labels.append(activation_time_label)
            self.duration_labels.append(duration_label)

            # Add to the grid layout in the next available row
            row = len(self.window_labels)
            self.grid_layout.addWidget(window_label, row, 0)
            self.grid_layout.addWidget(activation_time_label, row, 1)
            self.grid_layout.addWidget(duration_label, row, 2)

        # Update current window and its start time
        self.current_window_name = window_name
        self.current_window_start = current_time

    def update_display(self):
        pass  # No need for additional display updates
