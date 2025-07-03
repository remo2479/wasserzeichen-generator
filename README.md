# Wasserzeichen Generator

Ein professioneller Python-basierter Wasserzeichen-Generator mit grafischer Benutzeroberfläche und Live-Vorschau.

## 🌟 Features

- **🖼️ Batch-Verarbeitung**: Verarbeitet alle Bilder in einem Ordner automatisch
- **👁️ Live-Vorschau**: Sofortige Anzeige des Ergebnisses mit allen Einstellungen
- **🎛️ Vollständige Kontrolle**: 
  - Größensteuerung (5% - 60% der Bildbreite)
  - Transparenz-Einstellung (10% - 90%)
  - 9 verschiedene Positionierungsoptionen
- **💧 Professionelle Wasserzeichen**: Transparente Überlagerung mit hoher Qualität
- **📁 Sichere Verarbeitung**: Originalbilder bleiben unverändert
- **🔧 Benutzerfreundlich**: Intuitive GUI mit Drag & Drop-ähnlicher Bedienung
- **📊 Fortschrittsanzeige**: Echtzeit-Updates während der Verarbeitung
- **⚡ Standalone .exe**: Funktioniert ohne Python-Installation

## 📸 Screenshots

### Hauptoberfläche
- Zwei-Panel-Layout mit Steuerung und Live-Vorschau
- Intuitive Slider für Größe und Transparenz
- Dropdown-Menü für präzise Positionierung

### Live-Vorschau
- Sofortige Anzeige aller Änderungen
- Scrollbare Vorschau für große Bilder
- Detaillierte Status-Informationen

## 🚀 Installation & Verwendung

### Option 1: Fertige .exe-Datei (Empfohlen)

1. **Build-Script ausführen**:
   ```bash
   python build.py
   ```

2. **Programm starten**:
   - Doppelklick auf `dist/WasserzeichenGenerator.exe`
   - Keine weitere Installation erforderlich!

### Option 2: Python-Script direkt

1. **Repository klonen**:
   ```bash
   git clone https://github.com/remo2479/wasserzeichen-generator.git
   cd wasserzeichen-generator
   ```

2. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Programm starten**:
   ```bash
   python wasserzeichen_generator.py
   ```

## 📋 Systemanforderungen

- **Windows**: 7, 8, 10, 11
- **Python**: 3.7+ (nur für Entwicklung)
- **RAM**: Mindestens 512 MB
- **Speicher**: 50 MB freier Speicherplatz

## 🎯 Schnellstart

1. **Programm öffnen**
2. **Bildordner auswählen** - Klick auf "Durchsuchen..." bei "Ordner mit Bildern"
3. **Wasserzeichen auswählen** - Klick auf "Durchsuchen..." bei "Wasserzeichen Datei"
4. **Einstellungen anpassen**:
   - Größe mit dem Slider einstellen
   - Transparenz nach Wunsch anpassen
   - Position aus Dropdown wählen
5. **Live-Vorschau prüfen** - Das Ergebnis wird sofort rechts angezeigt
6. **"Alle Bilder verarbeiten"** - Fertig! ✨

## 🖼️ Unterstützte Bildformate

### Eingabebilder
- **JPEG** (.jpg, .jpeg)
- **PNG** (.png)
- **GIF** (.gif)
- **BMP** (.bmp)
- **TIFF** (.tiff)

### Wasserzeichen
- **PNG** (empfohlen für beste Transparenz)
- **JPEG, GIF, BMP, TIFF** (vollständig unterstützt)

## 🔧 Erweiterte Features

### Intelligente Skalierung
- Automatische proportionale Anpassung
- Erhaltung der Bildqualität
- Optimierung für verschiedene Bildgrößen

### Positionierungsoptionen
```
Oben Links    | Oben Mitte    | Oben Rechts
Mitte Links   | Mitte         | Mitte Rechts  
Unten Links   | Unten Mitte   | Unten Rechts
```

### Ausgabequalität
- **JPEG**: 95% Qualität, optimiert für Web und Druck
- **PNG**: Verlustfreie Kompression mit Alpha-Kanal
- **Andere Formate**: Originalqualität beibehalten

## 📁 Projektstruktur

```
wasserzeichen-generator/
├── wasserzeichen_generator.py  # Hauptprogramm
├── build.py                    # Build-Script für .exe
├── package.py                  # Verpackungs-Script
├── requirements.txt            # Python-Abhängigkeiten
├── README.md                   # Diese Datei
├── .gitignore                  # Git-Ausschlüsse
├── bilder/                     # Beispielbilder (optional)
├── logo/                       # Beispiel-Wasserzeichen (optional)
└── dist/                       # Generierte .exe-Datei
```

## �️ Entwicklung

### Lokale Entwicklung
```bash
# Repository forken und klonen
git clone https://github.com/remo2479/wasserzeichen-generator.git
cd wasserzeichen-generator

# Virtual Environment erstellen
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Abhängigkeiten installieren
pip install -r requirements.txt

# Programm starten
python wasserzeichen_generator.py
```

### Build erstellen
```bash
# .exe-Datei generieren
python build.py

# Verpackung für Distribution
python package.py
```

## 🤝 Beitragen

Wir freuen uns über Beiträge! So können Sie helfen:

1. **Fork** des Repositories erstellen
2. **Feature Branch** erstellen (`git checkout -b feature/neue-funktion`)
3. **Änderungen committen** (`git commit -am 'Neue Funktion hinzugefügt'`)
4. **Branch pushen** (`git push origin feature/neue-funktion`)
5. **Pull Request** erstellen

### Entwicklungsrichtlinien
- Code sollte Python PEP 8 Standards folgen
- Neue Features sollten getestet werden
- Dokumentation für neue Funktionen hinzufügen

## 📜 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für Details.

**Kurz gesagt**: Verwenden Sie es frei für private und kommerzielle Zwecke!

## 🐛 Probleme melden

Haben Sie einen Bug gefunden oder eine Funktionsanfrage?

- **Bug-Reports**: [Issues auf GitHub](https://github.com/remo2479/wasserzeichen-generator/issues)
- **Feature-Requests**: Beschreiben Sie Ihre Idee in einem Issue
- **Diskussionen**: [Discussions-Bereich](https://github.com/remo2479/wasserzeichen-generator/discussions)

## 📞 Kontakt & Support

- **GitHub Issues**: Für Bugs und Features
- **Diskussionen**: Für allgemeine Fragen
- **Wiki**: Detaillierte Dokumentation und Tutorials

## 🎉 Danksagungen

- **Pillow (PIL)**: Für exzellente Bildverarbeitung
- **tkinter**: Für die GUI-Funktionalität
- **PyInstaller**: Für Standalone-Executable-Erstellung
- **Community**: Für Feedback und Beiträge

## 🔄 Changelog

### Version 1.0.0 (2025-07-03)
- ✨ Erste Veröffentlichung
- 🎛️ Live-Vorschau implementiert
- 📊 Slider-Steuerung für Größe und Transparenz
- 🎯 9 Positionierungsoptionen
- 🔧 Standalone .exe-Generation
- 📱 Responsive GUI-Design
- 🚀 Batch-Verarbeitung optimiert

---

**⭐ Gefällt Ihnen das Projekt? Geben Sie uns einen Stern auf GitHub!**

**🚀 Erstellt mit ❤️ für die Community**
