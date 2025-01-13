### VERZE PRO MACOS

# TimeTracker

**TimeTracker** je aplikace pro sledování aktivit na počítači, která umožňuje uživatelům monitorovat aktivitu, pořizovat snímky obrazovky a ukládat data o aktivitách do souboru CSV pro pozdější analýzu.

## Funkce

- **Sledování aktivity:** Aplikace monitoruje aktivitu na počítači, detekuje aktivní okna a zobrazuje je v reálném čase.
- **Snímky obrazovky:** Uživatelé mohou pořizovat snímky obrazovky v nastavených intervalech nebo na základě konkrétních událostí.
- **Ukládání dat:** Data o aktivitách a snímky obrazovky jsou ukládány do CSV souborů pro pozdější analýzu.
- **Uživatelské nastavení:** Aplikace umožňuje přizpůsobit různé parametry, jako jsou intervaly pro pořizování snímků nebo soubor, do kterého se ukládají data.


### Budoucí vylepšení

- **Detailnější uživatelské nastavení**: Možnost úplného vypnutí pořizování screenshotů a výpisu CSV statistik.
- **Pokročilé monitorování**: Možnost výběru aplikací, které budou sledovány.
- **Rozšíření funkcí**: Zavedení možnosti označit aplikace jako oblíbené („pin“) a ikony aplikací vedle názvu, pokud ikonu mají.
- **Uložení nastavení při dalším spuštění**: Uložení nastavení ať už screenshotů nebo exportu dat nebo strávený čas v aplikacích momentálně se nastavení ukládá pouze po dobu kdy je aplikace spuštěna.


## Instalace

1. Naklonujte tento repozitář:
   ```bash
   git clone https://github.com/Benisekjan/TimeTracker
   ```
2. Vytvořte virtuální prostředí :
   ```bash
    python -m venv .env
   ```
3. Nainstalujte požadavky:

   ```bash
   pip install requirements.txt
   ```

4. Pro instalaci a nastavení automatického spouštění při startu použijte:

   ```bash
    python main.py
   ```

5. **Pro build aplikace**
   ```bash
    pyinstaller --windowed --name "TimeTracker" --icon=icons/icon.icns --add-data "icons:icons" main.py
   ``` 

## Technologie

| Technologie       | Popis                                                                                          |
|-------------------|------------------------------------------------------------------------------------------------|
| **Programovací jazyk** | Python – flexibilní jazyk pro vývoj desktopových aplikací a skriptů.                          |
| **Grafické rozhraní**  | PyQt5 – knihovna pro tvorbu nativních desktopových aplikací s grafickým rozhraním.           |
| **Snímky obrazovky**   | pyautogui – knihovna pro pořízení snímků obrazovky a jejich ukládání do specifikované složky. |
| **Sledování aktivity** | pynput – knihovna pro monitorování klávesnice a myši, použita pro sledování aktivity uživatele.|
| **Ukládání dat**      | pandas – knihovna pro práci s daty, použita pro ukládání aktivit do CSV souboru.              |
| **Automatizace**      | os, shutil – standardní knihovny pro práci se soubory a spouštění skriptů při startu počítače.   |


## Použité zdroje

- **[OpenAI ChatGPT](https://chatgpt.com/)**: Oficiální dokumentace k ChatGPT, obsahuje informace o funkcích a použití.
- **[Qt for Python Documentation](https://doc.qt.io/qtforpython-6/)**: Dokumentace k Qt for Python, zahrnuje informace o instalaci a použití.
- **[psutil Documentation](https://psutil.readthedocs.io/en/latest/#)**: Dokumentace k psutil, nástroj pro správu systémových prostředků.
- **[PyAutoGUI Documentation](https://pyautogui.readthedocs.io/en/latest/screenshot.html#)**: Dokumentace k PyAutoGUI, modul pro pořizování snímků obrazovky v Pythonu.
- **[AppKit Documentation](https://developer.apple.com/documentation/appkit)**: Dokumentace k AppKit, framework pro tvorbu uživatelských rozhraní na macOS.

