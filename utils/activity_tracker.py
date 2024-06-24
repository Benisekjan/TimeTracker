from PyQt5.QtCore import QObject, pyqtSignal
from Foundation import NSWorkspace
from AppKit import NSWorkspaceDidActivateApplicationNotification, NSWorkspaceDidDeactivateApplicationNotification
from pynput import mouse, keyboard

class ActivityTracker(QObject):
    activityChanged = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.active = False

        # Sledování změn aktivní aplikace pomocí NSWorkspace
        workspace = NSWorkspace.sharedWorkspace()
        notification_center = workspace.notificationCenter()
        notification_center.addObserver_selector_name_object_(
            self,
            "applicationActivated:",
            NSWorkspaceDidActivateApplicationNotification,
            None
        )
        notification_center.addObserver_selector_name_object_(
            self,
            "applicationDeactivated:",
            NSWorkspaceDidDeactivateApplicationNotification,
            None
        )

        # Sledování myši a klávesnice
        self.mouse_listener = mouse.Listener(on_move=self.on_activity)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)

    def start(self):
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def on_activity(self, *args):
        if not self.active:
            self.active = True
            self.activityChanged.emit(True)

    def applicationActivated_(self, notification):
        if not self.active:
            self.active = True
            self.activityChanged.emit(True)

    def applicationDeactivated_(self, notification):
        if self.active:
            self.active = False
            self.activityChanged.emit(False)
