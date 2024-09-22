from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from pynput import mouse, keyboard
from Foundation import NSWorkspace
from AppKit import NSWorkspaceDidActivateApplicationNotification, NSWorkspaceDidDeactivateApplicationNotification

class ActivityTracker(QObject):
    activityChanged = pyqtSignal(bool)
    windowChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.active = False
        self.current_window = None

        # Setup workspace notifications
        self.workspace = NSWorkspace.sharedWorkspace()
        self.notification_center = self.workspace.notificationCenter()
        self.notification_center.addObserver_selector_name_object_(
            self,
            "applicationActivated:",
            NSWorkspaceDidActivateApplicationNotification,
            None
        )
        self.notification_center.addObserver_selector_name_object_(
            self,
            "applicationDeactivated:",
            NSWorkspaceDidDeactivateApplicationNotification,
            None
        )

        # Setup mouse and keyboard listeners
        self.mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)

        # Setup inactivity timer
        self.inactivity_timer = QTimer()
        self.inactivity_timer.setInterval(3000)  # 3 seconds
        self.inactivity_timer.timeout.connect(self.check_inactivity)

    def start(self):
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.inactivity_timer.start()

    def stop(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.inactivity_timer.stop()

    def on_activity(self, *args):
        if not self.active:
            self.active = True
            self.activityChanged.emit(True)
        self.inactivity_timer.start()  # Reset the inactivity timer

    def check_inactivity(self):
        if self.active:
            self.active = False
            self.activityChanged.emit(False)
            self.inactivity_timer.stop()

    def applicationActivated_(self, notification):
        self.on_activity()

    def applicationDeactivated_(self, notification):
        self.check_inactivity()

        # Get the name of the current active window
        active_app = self.workspace.frontmostApplication()
        window_name = active_app.localizedName() if active_app else "Unknown"
        
        # Emit signal only if window has changed
        if window_name != self.current_window:
            self.current_window = window_name
            self.windowChanged.emit(window_name)
