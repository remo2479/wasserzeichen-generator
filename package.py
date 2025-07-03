"""
Verpackungsscript für den Wasserzeichen Generator
Erstellt ein ZIP-Paket zum Versenden
"""

import zipfile
import os
import shutil
from datetime import datetime

def create_distribution_package():
    """Erstellt ein fertiges Verpackungs-ZIP für den Versand"""
    
    # Prüfen ob .exe existiert
    exe_path = "dist/WasserzeichenGenerator.exe"
    if not os.path.exists(exe_path):
        print("❌ Fehler: WasserzeichenGenerator.exe nicht gefunden!")
        print("Bitte führen Sie zuerst 'python build.py' aus.")
        return False
    
    # Verpackungsordner erstellen
    package_dir = "WasserzeichenGenerator_Package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # .exe kopieren
    shutil.copy2(exe_path, os.path.join(package_dir, "WasserzeichenGenerator.exe"))
    
    # Anleitung für Endbenutzer erstellen
    user_manual = """# Wasserzeichen Generator - Anleitung

## 🚀 Schnellstart

1. **Doppelklick** auf `WasserzeichenGenerator.exe`
2. **Ordner auswählen** mit den Bildern, die ein Wasserzeichen erhalten sollen
3. **Wasserzeichen-Datei auswählen** (am besten PNG-Format)
4. **"Okay" klicken** - Fertig!

## 📁 Was passiert?

- Ihre **Originalbilder bleiben unverändert**
- Es werden **Kopien erstellt** mit dem Zusatz "_wasserzeichen"
- Das Wasserzeichen wird **transparent in der Mitte** platziert

## 💡 Tipps

- **PNG-Dateien** eignen sich am besten als Wasserzeichen
- **Transparente Wasserzeichen** funktionieren am besten
- Das Programm verarbeitet **alle Bilder im Ordner** automatisch

## 🔧 Unterstützte Formate

**Bilder:** JPEG, PNG, GIF, BMP, TIFF
**Wasserzeichen:** PNG (empfohlen), JPEG, GIF, BMP, TIFF

## ❓ Probleme?

- Stellen Sie sicher, dass der gewählte Ordner Bilddateien enthält
- Bei Fehlern wird eine Meldung angezeigt
- Das Programm benötigt **keine Installation** - einfach ausführen!

---
Erstellt mit Python - Keine Installation erforderlich
"""
    
    # Anleitung speichern
    with open(os.path.join(package_dir, "ANLEITUNG.txt"), "w", encoding="utf-8") as f:
        f.write(user_manual)
    
    # Beispiel-Wasserzeichen Info erstellen
    example_info = """# Beispiel-Wasserzeichen

Für beste Ergebnisse sollte Ihr Wasserzeichen:

✅ **PNG-Format** verwenden (unterstützt Transparenz)
✅ **Transparenten Hintergrund** haben
✅ **Kontrastreiche Farben** verwenden
✅ **Nicht zu klein** sein (mindestens 200x200 Pixel)

## Wasserzeichen erstellen

Sie können Wasserzeichen erstellen mit:
- **GIMP** (kostenlos)
- **Photoshop**
- **Paint.NET** (kostenlos)
- **Canva** (online, kostenlos)

Speichern Sie das Wasserzeichen als PNG-Datei mit transparentem Hintergrund.
"""
    
    with open(os.path.join(package_dir, "Wasserzeichen_Tipps.txt"), "w", encoding="utf-8") as f:
        f.write(example_info)
    
    # ZIP erstellen
    datum = datetime.now().strftime("%Y-%m-%d")
    zip_name = f"WasserzeichenGenerator_{datum}.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arc_name)
    
    # Aufräumen
    shutil.rmtree(package_dir)
    
    # Dateigröße anzeigen
    size_mb = os.path.getsize(zip_name) / (1024 * 1024)
    
    print(f"✅ Verpackung erfolgreich erstellt!")
    print(f"📦 Datei: {zip_name}")
    print(f"📊 Größe: {size_mb:.1f} MB")
    print(f"\n📨 Versandfertig!")
    print("Diese ZIP-Datei können Sie per E-Mail versenden oder auf einen USB-Stick kopieren.")
    
    return True

def main():
    print("=== Wasserzeichen Generator - Verpackung ===\n")
    create_distribution_package()

if __name__ == "__main__":
    main()
