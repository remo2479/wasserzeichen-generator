"""
Build-Script für den Wasserzeichen Generator
Konvertiert das Python-Programm in eine ausführbare .exe-Datei
"""

import subprocess
import sys
import os

def install_requirements():
    """Installiert die benötigten Pakete"""
    print("Installiere benötigte Pakete...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_exe():
    """Erstellt die .exe-Datei"""
    print("Erstelle .exe-Datei...")
    
    # PyInstaller Befehl
    cmd = [
        "pyinstaller",
        "--onefile",                    # Alles in eine Datei packen
        "--windowed",                   # Kein Konsolen-Fenster
        "--name=WasserzeichenGenerator", # Name der .exe-Datei
        "--icon=NONE",                  # Kein Icon (kann später hinzugefügt werden)
        "wasserzeichen_generator.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ Erfolgreich! Die .exe-Datei befindet sich im 'dist' Ordner.")
        print("📁 Pfad: dist/WasserzeichenGenerator.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Erstellen der .exe-Datei: {e}")
        return False
    
    return True

def main():
    print("=== Wasserzeichen Generator - Build Script ===\n")
    
    # Prüfen ob wir im richtigen Ordner sind
    if not os.path.exists("wasserzeichen_generator.py"):
        print("❌ Fehler: wasserzeichen_generator.py nicht gefunden!")
        print("Bitte führen Sie das Script im Projektordner aus.")
        return
    
    try:
        # Pakete installieren
        install_requirements()
        print("✅ Pakete erfolgreich installiert.\n")
        
        # .exe erstellen
        if build_exe():
            print("\n🎉 Build erfolgreich abgeschlossen!")
            print("\nSie können jetzt die Datei 'dist/WasserzeichenGenerator.exe' verwenden.")
            print("Diese Datei ist eigenständig und kann ohne Python-Installation ausgeführt werden.")
        
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    main()
