from PyQt5.QtCore import QObject, pyqtSignal
from Foundation import NSWorkspace
from AppKit import NSWorkspaceDidActivateApplicationNotification

class ActivityTracker(QObject):
    # Signál emitující změnu okna (jméno aktuálního okna)
    windowChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_window = None  # Ukládá jméno aktuálního okna

        # Nastavení sledování změn aktivního okna pomocí NSWorkspace
        self.workspace = NSWorkspace.sharedWorkspace()
        self.notification_center = self.workspace.notificationCenter()
        self.notification_center.addObserver_selector_name_object_(
            self,
            "applicationActivated:",  # Metoda, která bude volána při aktivaci okna
            NSWorkspaceDidActivateApplicationNotification,  # Notifikace pro aktivaci okna
            None
        )

    def applicationActivated_(self, notification):
        # Získání jména aktuálního aktivního okna
        active_app = self.workspace.frontmostApplication()
        window_name = active_app.localizedName() if active_app else "Unknown"  
        # Pokud není okno rozpoznáno, nastaví "Unknown"
        
        # Vyvolá signál, jen pokud se změnilo aktivní okno
        if window_name != self.current_window:
            self.current_window = window_name  # Aktualizuje jméno aktuálního okna
            self.windowChanged.emit(window_name)  # Vyvolá signál, že okno bylo změněno
