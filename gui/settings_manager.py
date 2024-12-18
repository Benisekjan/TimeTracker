import json
import os

class SettingsManager:
    SETTINGS_FILE = "settings.json"

    @staticmethod
    def load_settings():
        """Načte nastavení ze souboru nebo vrátí výchozí hodnoty."""
        if os.path.exists(SettingsManager.SETTINGS_FILE):
            with open(SettingsManager.SETTINGS_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    pass  # Pokud je soubor poškozený, použijeme výchozí hodnoty
        # Výchozí nastavení
        return {
            "tracking_interval": 1,  # 1 sekunda
            "screenshot_interval": 5  # 5 minut
        }

    @staticmethod
    def save_settings(settings):
        """Uloží nastavení do souboru."""
        with open(SettingsManager.SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
