from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from pynput import mouse, keyboard
from Foundation import NSWorkspace
from AppKit import NSWorkspaceDidActivateApplicationNotification, NSWorkspaceDidDeactivateApplicationNotification

class ActivityTracker(QObject):
    # Signál emitující změnu aktivity (aktivní/neaktivní)
    activityChanged = pyqtSignal(bool)
    # Signál emitující změnu okna (jméno aktuálního okna)
    windowChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.active = False  # Ukládá stav aktivity uživatele (True = aktivní, False = neaktivní)
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
        self.notification_center.addObserver_selector_name_object_(
            self,
            "applicationDeactivated:",  # Metoda, která bude volána při deaktivaci okna
            NSWorkspaceDidDeactivateApplicationNotification,  # Notifikace pro deaktivaci okna
            None
        )

        # Nastavení posluchače pro myš a klávesnici
        # Myš sleduje pohyb a kliknutí
        self.mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity)
        # Klávesnice sleduje stisk kláves
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)

        # Nastavení časovače pro sledování neaktivity
        self.inactivity_timer = QTimer()
        self.inactivity_timer.setInterval(3000)  # Interval pro neaktivitu je 3 sekundy
        self.inactivity_timer.timeout.connect(self.check_inactivity)  # Po 3 sekundách zkontroluje neaktivitu

    def start(self):
        # Spustí posluchače myši a klávesnice a časovač neaktivity
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.inactivity_timer.start()

    def stop(self):
        # Zastaví posluchače myši a klávesnice a časovač neaktivity
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.inactivity_timer.stop()

    def on_activity(self, *args):
        # Když je detekována aktivita (pohyb myši, stisk klávesy), aktualizuje stav
        if not self.active:
            self.active = True  # Nastaví uživatele jako aktivního
            self.activityChanged.emit(True)  # Vyvolá signál, že uživatel je aktivní
        self.inactivity_timer.start()  # Restartuje časovač neaktivity

    def check_inactivity(self):
        # Tato metoda je volána po uplynutí 3 sekund bez aktivity
        if self.active:
            self.active = False  # Nastaví uživatele jako neaktivního
            self.activityChanged.emit(False)  # Vyvolá signál, že uživatel je neaktivní
            self.inactivity_timer.stop()  # Zastaví časovač neaktivity

    def applicationActivated_(self, notification):
        # Tato metoda se spustí, když je okno aktivováno
        self.on_activity()  # Po aktivaci okna se zaznamená aktivita

    def applicationDeactivated_(self, notification):
        # Tato metoda se spustí, když je okno deaktivováno (přepnutí na jiné okno)
        self.check_inactivity()  # Zaznamená neaktivitu při přepnutí okna

        # Získání jména aktuálního aktivního okna
        active_app = self.workspace.frontmostApplication()
        window_name = active_app.localizedName() if active_app else "Unknown"  # Pokud není okno rozpoznáno, nastaví "Unknown"
        
        # Vyvolá signál, jen pokud se změnilo aktivní okno
        if window_name != self.current_window:
            self.current_window = window_name  # Aktualizuje jméno aktuálního okna
            self.windowChanged.emit(window_name)  # Vyvolá signál, že okno bylo změněno
