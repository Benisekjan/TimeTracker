from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton, QLineEdit, QFileDialog

class SettingsDialog(QDialog):
    def __init__(self, parent=None, tracking_interval=1, screenshot_interval=5, csv_interval=5, screenshot_path="/tmp", csv_path="/tmp"):
        super().__init__(parent)
        self.setWindowTitle("Nastavení")
        self.setModal(True)

        self.tracking_interval = tracking_interval
        self.screenshot_interval = screenshot_interval
        self.csv_interval = csv_interval
        self.screenshot_path = screenshot_path
        self.csv_path = csv_path

        layout = QVBoxLayout(self)

        # Interval sledování oken
        self.tracking_label = QLabel("Interval sledování oken (v sekundách):")
        self.tracking_spinbox = QSpinBox()
        self.tracking_spinbox.setRange(1, 60)
        self.tracking_spinbox.setValue(self.tracking_interval)
        layout.addWidget(self.tracking_label)
        layout.addWidget(self.tracking_spinbox)

        # Interval screenshotů
        self.screenshot_label = QLabel("Interval screenshotů (v minutách):")
        self.screenshot_spinbox = QSpinBox()
        self.screenshot_spinbox.setRange(1, 60)
        self.screenshot_spinbox.setValue(self.screenshot_interval)
        layout.addWidget(self.screenshot_label)
        layout.addWidget(self.screenshot_spinbox)

        # Interval logování do CSV
        self.csv_label = QLabel("Interval logů do CSV (v minutách):")
        self.csv_spinbox = QSpinBox()
        self.csv_spinbox.setRange(1, 60)
        self.csv_spinbox.setValue(self.csv_interval)
        layout.addWidget(self.csv_label)
        layout.addWidget(self.csv_spinbox)

        # Cesta pro ukládání screenshotů
        self.screenshot_path_label = QLabel("Cesta pro ukládání screenshotů:")
        self.screenshot_path_edit = QLineEdit(self.screenshot_path)
        self.screenshot_browse_button = QPushButton("Vybrat...")
        self.screenshot_browse_button.clicked.connect(self.browse_screenshot_path)
        layout.addWidget(self.screenshot_path_label)
        layout.addWidget(self.screenshot_path_edit)
        layout.addWidget(self.screenshot_browse_button)

        # Cesta pro ukládání CSV logů
        self.csv_path_label = QLabel("Cesta pro ukládání CSV logů:")
        self.csv_path_edit = QLineEdit(self.csv_path)
        self.csv_browse_button = QPushButton("Vybrat...")
        self.csv_browse_button.clicked.connect(self.browse_csv_path)
        layout.addWidget(self.csv_path_label)
        layout.addWidget(self.csv_path_edit)
        layout.addWidget(self.csv_browse_button)
        
        
        # Uložit a Zrušit
        self.save_button = QPushButton("Uložit")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Zrušit")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

    def browse_screenshot_path(self):
        path = QFileDialog.getExistingDirectory(self, "Vyberte složku pro screenshoty")
        if path:
            self.screenshot_path_edit.setText(path)

    def browse_csv_path(self):
        path = QFileDialog.getExistingDirectory(self, "Vyberte složku pro CSV logy")
        if path:
            self.csv_path_edit.setText(path)

    def get_settings(self):
        # Validace, aby uživatel nemohl nastavit prázdnou cestu
        if not self.screenshot_path_edit.text():
            self.screenshot_path_edit.setText("/tmp/screenshots")
        if not self.csv_path_edit.text():
            self.csv_path_edit.setText("/tmp/csv_logs")

        return {
            "tracking_interval": self.tracking_spinbox.value(),
            "screenshot_interval": self.screenshot_spinbox.value(),
            "csv_interval": self.csv_spinbox.value(),
            "screenshot_path": self.screenshot_path_edit.text(),
            "csv_path": self.csv_path_edit.text()
        }

