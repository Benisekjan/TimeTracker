import pyscreenshot as ImageGrab
import os
from datetime import datetime

class ScreenshotTaker:
    def __init__(self, default_directory="/tmp/"):
        self.default_directory = default_directory

        # Pokud složka neexistuje, vytvoříme ji
        if not os.path.exists(self.default_directory):
            os.makedirs(self.default_directory)

    def take_screenshot(self, directory_path=None):
        # Použití zadané složky, jinak výchozí
        directory = directory_path or self.default_directory

        # Zajištění, že složka existuje
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Vytvoření názvu souboru na základě aktuálního času
        timestamp = datetime.now().strftime("%Y.%m.%d-%H-%M-%S")
        file_path = os.path.join(directory, f"{timestamp}.png")

        # Pořízení screenshotu a jeho uložení
        screenshot = ImageGrab.grab()
        screenshot.save(file_path)

        return file_path  # Vrátí cestu k souboru pro další použití