VERZE PRO MACOS

Time Tracker

Autor: Jan Beníšek

Třída: IT4

Ročník: 2024/2025


Tato aplikace, nazvaná TimeTracker, slouží k monitorování a sledování aktivity uživatelských oken na počítači. 

Umožňuje:

Sledování aktivních oken – Aplikace zaznamenává, které okno je v daném okamžiku aktivní, a sleduje dobu jeho aktivace.
Zobrazení tabulky s informacemi o procesech – V reálném čase zobrazuje seznam běžících procesů, včetně jejich využití CPU, RAM, a PID, seřazený podle různých kritérií.
Pořízení screenshotů – Aplikace pravidelně pořizuje screenshoty a ukládá je do specifikované složky, což umožňuje sledování aktivity na obrazovce.


Hlavní součásti aplikace zahrnují:

Sledování aktivních oken pomocí modulu ActivityTracker.
Pořizování screenshotů pomocí modulu ScreenshotTaker.
Zobrazení informací o procesech v hlavním okně pomocí PyQt5.
Minimalizace na pozadí a správa aplikace prostřednictvím ikony v systémové liště.
Aplikace je postavena na PyQt5 a využívá knihovny pro sledování systémových procesů (psutil), pořizování screenshotů (pyscreenshot), a práci s notifikacemi v macOS (AppKit, Foundation).


Manuál:

git clone https://github.com/Benisekjan/TimeTracker

python -m venv .env

pip install requirements.txt 

python main.py

Pro build aplikace : pyinstaller --windowed --name "TimeTracker" --icon=icons/icon.icns --add-data "icons:icons" main.py 
