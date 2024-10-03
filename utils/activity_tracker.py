from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import pygetwindow as gw

class ActivityTracker(QObject):
    # Signál emitující změnu okna (jméno aktuálního okna)
    windowChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_window = None  # Ukládá jméno aktuálního okna
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_active_window)
        self.timer.start(1000)  # Kontrola každou sekundu

    def check_active_window(self):
        try:
            # Získání aktuálního aktivního okna
            active_window = gw.getActiveWindow()
            if active_window:
                window_name = active_window.title
            else:
                window_name = "Unknown"
        except Exception as e:
            window_name = "Unknown"

        # Vyvolá signál, jen pokud se změnilo aktivní okno
        if window_name != self.current_window:
            self.current_window = window_name  # Aktualizuje jméno aktuálního okna
            self.windowChanged.emit(window_name)  # Vyvolá signál, že okno bylo změněno
