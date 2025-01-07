import os
from PyQt5.QtCore import QDateTime
import pyautogui
class ScreenshotManager:
    def __init__(self):
        # Výchozí cesta pro screenshoty
        self.screenshot_directory = "/tmp/screenshot"
        self.ensure_directory_exists(self.screenshot_directory)

    def ensure_directory_exists(self, directory):
        # Vytvoří složku, pokud neexistuje
        os.makedirs(directory, exist_ok=True)

    def set_screenshot_directory(self, new_directory):
        # Změní výchozí složku pro ukládání screenshotů
        self.screenshot_directory = new_directory
        self.ensure_directory_exists(self.screenshot_directory)

    def take_screenshot(self):
        try:
            os.makedirs(self.screenshot_directory, exist_ok=True)  # Zajistí vytvoření složky, pokud neexistuje

            timestamp = QDateTime.currentDateTime().toString("yyyy.MM.dd-HH-mm-ss")  # Získání časového razítka
            filename = f"screenshot-{timestamp}.png"
            file_path = os.path.join(self.screenshot_directory, filename)  # Spojení cesty a názvu souboru

            # Pořízení snímku obrazovky pomocí pyautogui
            screenshot = pyautogui.screenshot()
            screenshot.save(file_path)  # Uloží screenshot na specifikované místo

            print(f"Screenshot uložen do: {file_path}")

        except Exception as e:
            print(f"Chyba při pořizování screenshotu: {e}")

