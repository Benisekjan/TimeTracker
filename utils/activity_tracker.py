import sys
from PyQt5.QtCore import QTimer, QDateTime
from Foundation import NSWorkspace
from AppKit import NSWorkspaceDidActivateApplicationNotification, NSWorkspaceDidDeactivateApplicationNotification
from PyObjCTools import AppHelper

class ActivityTracker:
    def __init__(self):
        self.active = False
        self.inactivity_timer = QTimer()
        self.inactivity_timer.setInterval(3000)  # 3 sekundy
        self.inactivity_timer.timeout.connect(self.check_activity)

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

    def start(self):
        self.inactivity_timer.start()

    def stop(self):
        self.inactivity_timer.stop()

    def on_activity(self, *args):
        if not self.active:
            self.active = True
            self.inactivity_timer.stop()  # Reset timer on activity
            self.inactivity_timer.start()

    def check_activity(self):
        if self.active:
            self.active = False

    def applicationActivated_(self, notification):
        if not self.active:
            self.active = True
            self.inactivity_timer.stop()  # Reset timer on activity
            self.inactivity_timer.start()

    def applicationDeactivated_(self, notification):
        if self.active:
            self.active = False
            self.inactivity_timer.stop()
