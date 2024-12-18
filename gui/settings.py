from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton

class SettingsDialog(QDialog):
    def __init__(self, parent=None, tracking_interval=1, screenshot_interval=5):
        super().__init__(parent)
        self.setWindowTitle("Nastavení")
        self.setModal(True)
        self.tracking_interval = tracking_interval
        self.screenshot_interval = screenshot_interval

        layout = QVBoxLayout(self)

        # Pole pro nastavení intervalu sledování oken
        self.tracking_label = QLabel("Interval sledování oken (v sekundách):")
        self.tracking_spinbox = QSpinBox()
        self.tracking_spinbox.setRange(1, 60)
        self.tracking_spinbox.setValue(self.tracking_interval)

        layout.addWidget(self.tracking_label)
        layout.addWidget(self.tracking_spinbox)

        # Pole pro nastavení intervalu pořizování screenshotů
        self.screenshot_label = QLabel("Interval screenshotů (v minutách):")
        self.screenshot_spinbox = QSpinBox()
        self.screenshot_spinbox.setRange(1, 60)
        self.screenshot_spinbox.setValue(self.screenshot_interval)

        layout.addWidget(self.screenshot_label)
        layout.addWidget(self.screenshot_spinbox)

        # Tlačítka pro uložení nebo zrušení
        self.save_button = QPushButton("Uložit")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Zrušit")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

    def get_settings(self):
        # Vrací nová nastavení
        return {
            "tracking_interval": self.tracking_spinbox.value(),
            "screenshot_interval": self.screenshot_spinbox.value()
        }
