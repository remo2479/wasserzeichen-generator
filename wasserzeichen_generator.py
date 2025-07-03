import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
import shutil
import threading


class WasserzeichenGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Wasserzeichen Generator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Pfade speichern
        self.bilder_pfad = ""
        self.wasserzeichen_pfad = ""
        
        # Größe und Vorschau
        self.wasserzeichen_groesse = 20  # Prozent der Bildbreite
        self.vorschau_bild = None
        self.original_vorschau = None
        self.wasserzeichen_original = None
        self.preview_update_pending = False  # Debouncing für Vorschau-Updates
        
        self.create_widgets()
        
    def create_widgets(self):
        # Hauptcontainer mit zwei Bereichen
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Linker Bereich - Steuerung
        control_frame = ttk.Frame(main_container)
        main_container.add(control_frame, weight=1)
        
        # Rechter Bereich - Vorschau
        preview_frame = ttk.Frame(main_container)
        main_container.add(preview_frame, weight=1)
        
        # === STEUERUNGSBEREICH ===
        control_inner = ttk.Frame(control_frame, padding="10")
        control_inner.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title_label = ttk.Label(control_inner, text="Wasserzeichen Generator", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Bilder Ordner Auswahl
        ttk.Label(control_inner, text="Ordner mit Bildern:").pack(anchor=tk.W, pady=(0, 5))
        self.bilder_pfad_var = tk.StringVar()
        
        bilder_frame = ttk.Frame(control_inner)
        bilder_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.bilder_entry = ttk.Entry(bilder_frame, textvariable=self.bilder_pfad_var, state="readonly")
        self.bilder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(bilder_frame, text="Durchsuchen...", 
                  command=self.waehle_bilder_ordner).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Wasserzeichen Auswahl
        ttk.Label(control_inner, text="Wasserzeichen Datei:").pack(anchor=tk.W, pady=(0, 5))
        self.wasserzeichen_pfad_var = tk.StringVar()
        
        wasserzeichen_frame = ttk.Frame(control_inner)
        wasserzeichen_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.wasserzeichen_entry = ttk.Entry(wasserzeichen_frame, textvariable=self.wasserzeichen_pfad_var, 
                                           state="readonly")
        self.wasserzeichen_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(wasserzeichen_frame, text="Durchsuchen...", 
                  command=self.waehle_wasserzeichen).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Größensteuerung
        groesse_frame = ttk.LabelFrame(control_inner, text="Wasserzeichen-Größe", padding="10")
        groesse_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Slider
        self.groesse_var = tk.DoubleVar(value=self.wasserzeichen_groesse)
        ttk.Label(groesse_frame, text="Größe (% der Bildbreite):").pack(anchor=tk.W)
        
        slider_frame = ttk.Frame(groesse_frame)
        slider_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.groesse_slider = ttk.Scale(slider_frame, from_=5, to=60, 
                                       variable=self.groesse_var, orient=tk.HORIZONTAL,
                                       command=self.on_groesse_change)
        self.groesse_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.groesse_label = ttk.Label(slider_frame, text="20%", width=6)
        self.groesse_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Transparenz-Steuerung
        transparenz_frame = ttk.Frame(groesse_frame)
        transparenz_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(transparenz_frame, text="Transparenz:").pack(side=tk.LEFT)
        
        self.transparenz_var = tk.DoubleVar(value=50)
        self.transparenz_slider = ttk.Scale(transparenz_frame, from_=10, to=90,
                                          variable=self.transparenz_var, orient=tk.HORIZONTAL,
                                          command=self.on_groesse_change, length=150)
        self.transparenz_slider.pack(side=tk.LEFT, padx=(10, 10))
        
        self.transparenz_label = ttk.Label(transparenz_frame, text="50%", width=6)
        self.transparenz_label.pack(side=tk.LEFT)
        
        # Position
        position_frame = ttk.Frame(groesse_frame)
        position_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(position_frame, text="Position:").pack(side=tk.LEFT)
        
        self.position_var = tk.StringVar(value="Mitte")
        position_combo = ttk.Combobox(position_frame, textvariable=self.position_var, 
                                     values=["Oben Links", "Oben Mitte", "Oben Rechts",
                                            "Mitte Links", "Mitte", "Mitte Rechts", 
                                            "Unten Links", "Unten Mitte", "Unten Rechts"],
                                     state="readonly", width=15)
        position_combo.pack(side=tk.LEFT, padx=(10, 0))
        position_combo.bind('<<ComboboxSelected>>', self.on_groesse_change)
        
        # Buttons
        button_frame = ttk.Frame(control_inner)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        self.okay_button = ttk.Button(button_frame, text="Alle Bilder verarbeiten", 
                                     command=self.verarbeite_bilder, state="disabled")
        self.okay_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Abbrechen", 
                  command=self.root.quit).pack(side=tk.LEFT)
        
        # === VORSCHAUBEREICH ===
        preview_inner = ttk.Frame(preview_frame, padding="10")
        preview_inner.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(preview_inner, text="Live-Vorschau", 
                 font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        # Canvas für Bildvorschau
        self.preview_canvas = tk.Canvas(preview_inner, bg="#f0f0f0", relief=tk.SUNKEN, bd=2)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars für Canvas
        h_scroll = ttk.Scrollbar(preview_inner, orient=tk.HORIZONTAL, command=self.preview_canvas.xview)
        v_scroll = ttk.Scrollbar(preview_inner, orient=tk.VERTICAL, command=self.preview_canvas.yview)
        self.preview_canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        # Status Label
        self.status_label = ttk.Label(preview_inner, text="Wählen Sie Bilder und Wasserzeichen aus...")
        self.status_label.pack(pady=(10, 0))
        
    def waehle_bilder_ordner(self):
        """Ordner mit Bildern auswählen"""
        ordner = filedialog.askdirectory(title="Ordner mit Bildern auswählen")
        if ordner:
            self.bilder_pfad = ordner
            self.bilder_pfad_var.set(ordner)
            self.check_okay_button()
            self.update_preview()
            
    def waehle_wasserzeichen(self):
        """Wasserzeichen-Datei auswählen"""
        datei = filedialog.askopenfilename(
            title="Wasserzeichen auswählen",
            filetypes=[
                ("Bilddateien", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("PNG Dateien", "*.png"),
                ("JPEG Dateien", "*.jpg *.jpeg"),
                ("Alle Dateien", "*.*")
            ]
        )
        if datei:
            self.wasserzeichen_pfad = datei
            self.wasserzeichen_pfad_var.set(datei)
            self.wasserzeichen_original = None  # Reset für neue Vorschau
            self.check_okay_button()
            self.update_preview()
            
    def on_groesse_change(self, value=None):
        """Wird aufgerufen wenn Größe, Transparenz oder Position geändert wird"""
        self.wasserzeichen_groesse = self.groesse_var.get()
        self.groesse_label.config(text=f"{int(self.wasserzeichen_groesse)}%")
        self.transparenz_label.config(text=f"{int(self.transparenz_var.get())}%")
        
        # Debouncing: Nur ein Update-Thread gleichzeitig
        if not self.preview_update_pending:
            self.preview_update_pending = True
            self.root.after(100, self._delayed_preview_update)  # 100ms Verzögerung
    
    def _delayed_preview_update(self):
        """Verzögertes Vorschau-Update um Flackern zu vermeiden"""
        self.preview_update_pending = False
        self.update_preview()
        
    def update_preview(self):
        """Aktualisiert die Live-Vorschau"""
        if not self.bilder_pfad or not self.wasserzeichen_pfad:
            self.status_label.config(text="Wählen Sie Bilder und Wasserzeichen aus...")
            self.preview_canvas.delete("all")
            return
            
        try:
            # Erstes Bild aus dem Ordner finden
            bild_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
            erstes_bild = None
            
            for datei in os.listdir(self.bilder_pfad):
                if os.path.splitext(datei.lower())[1] in bild_extensions:
                    erstes_bild = os.path.join(self.bilder_pfad, datei)
                    break
            
            if not erstes_bild:
                self.status_label.config(text="Keine Bilddateien im Ordner gefunden")
                self.preview_canvas.delete("all")
                return
            
            # Threading für bessere Performance
            threading.Thread(target=self._create_preview, args=(erstes_bild,), daemon=True).start()
            
        except Exception as e:
            self.status_label.config(text=f"Vorschau-Fehler: {str(e)}")
            
    def _create_preview(self, bild_pfad):
        """Erstellt die Vorschau in einem separaten Thread"""
        try:
            # Wasserzeichen laden (nur einmal)
            if self.wasserzeichen_original is None:
                self.wasserzeichen_original = Image.open(self.wasserzeichen_pfad).convert("RGBA")
            
            # Bild laden und für Vorschau skalieren
            original_bild = Image.open(bild_pfad).convert("RGBA")
            
            # Auf maximale Vorschaugröße skalieren (400x400)
            max_preview_size = 400
            bild_breite, bild_hoehe = original_bild.size
            
            if bild_breite > max_preview_size or bild_hoehe > max_preview_size:
                ratio = min(max_preview_size / bild_breite, max_preview_size / bild_hoehe)
                neue_breite = int(bild_breite * ratio)
                neue_hoehe = int(bild_hoehe * ratio)
                preview_bild = original_bild.resize((neue_breite, neue_hoehe), Image.Resampling.LANCZOS)
            else:
                preview_bild = original_bild.copy()
            
            # Wasserzeichen für Vorschau anpassen
            preview_mit_wz = self._apply_watermark_preview(preview_bild, self.wasserzeichen_original)
            
            # Für tkinter konvertieren
            self.vorschau_bild = ImageTk.PhotoImage(preview_mit_wz)
            
            # UI im Hauptthread aktualisieren
            self.root.after(0, self._update_preview_ui, preview_mit_wz.size)
            
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text=f"Vorschau-Fehler: {str(e)}"))
            
    def _apply_watermark_preview(self, bild, wasserzeichen):
        """Wendet Wasserzeichen für Vorschau an"""
        bild_kopie = bild.copy()
        bild_breite, bild_hoehe = bild_kopie.size
        
        # Wasserzeichen skalieren
        max_wz_breite = int(bild_breite * (self.wasserzeichen_groesse / 100))
        wz_breite, wz_hoehe = wasserzeichen.size
        
        # IMMER skalieren auf die gewünschte Größe (auch wenn das Original kleiner ist)
        skalierung = max_wz_breite / wz_breite
        neue_wz_breite = int(wz_breite * skalierung)
        neue_wz_hoehe = int(wz_hoehe * skalierung)
        wasserzeichen_skaliert = wasserzeichen.resize((neue_wz_breite, neue_wz_hoehe), Image.Resampling.LANCZOS)
        
        # Transparenz anwenden
        wasserzeichen_transparent = wasserzeichen_skaliert.copy()
        alpha = wasserzeichen_transparent.split()[-1]
        transparenz_faktor = self.transparenz_var.get() / 100
        alpha = alpha.point(lambda p: int(p * transparenz_faktor))
        wasserzeichen_transparent.putalpha(alpha)
        
        # Position berechnen
        wz_breite, wz_hoehe = wasserzeichen_transparent.size
        position = self.position_var.get()
        
        # Sicherheitsabstand von den Rändern (proportional zur Bildgröße)
        rand_abstand = max(5, int(min(bild_breite, bild_hoehe) * 0.02))
        
        if position == "Oben Links":
            x, y = rand_abstand, rand_abstand
        elif position == "Oben Mitte":
            x, y = (bild_breite - wz_breite) // 2, rand_abstand
        elif position == "Oben Rechts":
            x, y = bild_breite - wz_breite - rand_abstand, rand_abstand
        elif position == "Mitte Links":
            x, y = rand_abstand, (bild_hoehe - wz_hoehe) // 2
        elif position == "Mitte":
            x, y = (bild_breite - wz_breite) // 2, (bild_hoehe - wz_hoehe) // 2
        elif position == "Mitte Rechts":
            x, y = bild_breite - wz_breite - rand_abstand, (bild_hoehe - wz_hoehe) // 2
        elif position == "Unten Links":
            x, y = rand_abstand, bild_hoehe - wz_hoehe - rand_abstand
        elif position == "Unten Mitte":
            x, y = (bild_breite - wz_breite) // 2, bild_hoehe - wz_hoehe - rand_abstand
        elif position == "Unten Rechts":
            x, y = bild_breite - wz_breite - rand_abstand, bild_hoehe - wz_hoehe - rand_abstand
        else:
            # Fallback auf Mitte
            x, y = (bild_breite - wz_breite) // 2, (bild_hoehe - wz_hoehe) // 2
        
        # Sicherstellen, dass das Wasserzeichen im Bildbereich bleibt
        x = max(0, min(x, bild_breite - wz_breite))
        y = max(0, min(y, bild_hoehe - wz_hoehe))
        
        # Wasserzeichen anwenden
        bild_kopie.paste(wasserzeichen_transparent, (x, y), wasserzeichen_transparent)
        return bild_kopie
        
    def _update_preview_ui(self, image_size):
        """Aktualisiert die Vorschau im UI (Hauptthread)"""
        # Canvas nicht leeren wenn bereits ein Bild vorhanden ist
        if self.vorschau_bild:
            # Altes Bild entfernen
            self.preview_canvas.delete("preview_image")
            
            # Canvas-Größe an Bild anpassen
            canvas_width, canvas_height = image_size
            self.preview_canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))
            
            # Neues Bild in Canvas einfügen
            self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.vorschau_bild, tags="preview_image")
            
            self.status_label.config(text=f"Vorschau: {image_size[0]}x{image_size[1]} px | "
                                         f"Größe: {int(self.wasserzeichen_groesse)}% | "
                                         f"Transparenz: {int(self.transparenz_var.get())}%")
            
    def check_okay_button(self):
        """Okay-Button nur aktivieren wenn beide Pfade gewählt sind"""
        if self.bilder_pfad and self.wasserzeichen_pfad:
            self.okay_button.config(state="normal")
        else:
            self.okay_button.config(state="disabled")
            
    def verarbeite_bilder(self):
        """Hauptfunktion zur Bildverarbeitung"""
        try:
            # Wasserzeichen laden
            wasserzeichen = Image.open(self.wasserzeichen_pfad).convert("RGBA")
            
            # Alle Bilddateien im Ordner finden
            bild_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
            bilder = []
            
            for datei in os.listdir(self.bilder_pfad):
                if os.path.splitext(datei.lower())[1] in bild_extensions:
                    bilder.append(datei)
            
            if not bilder:
                messagebox.showwarning("Keine Bilder", "Keine Bilddateien im gewählten Ordner gefunden!")
                return
            
            # Progress Dialog erstellen
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Verarbeitung läuft...")
            progress_window.geometry("300x100")
            progress_window.resizable(False, False)
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            ttk.Label(progress_window, text="Bilder werden verarbeitet...").pack(pady=10)
            progress_bar = ttk.Progressbar(progress_window, maximum=len(bilder), mode='determinate')
            progress_bar.pack(pady=10, padx=20, fill=tk.X)
            
            verarbeitete_bilder = 0
            fehler_bilder = []
            
            # Jedes Bild verarbeiten
            for i, bild_datei in enumerate(bilder):
                try:
                    bild_pfad = os.path.join(self.bilder_pfad, bild_datei)
                    
                    # Bild laden
                    bild = Image.open(bild_pfad).convert("RGBA")
                    
                    # Wasserzeichen auf Bildgröße anpassen
                    bild_breite, bild_hoehe = bild.size
                    max_wasserzeichen_breite = int(bild_breite * (self.wasserzeichen_groesse / 100))
                    
                    # Wasserzeichen IMMER proportional skalieren (auch wenn es kleiner ist)
                    wz_breite, wz_hoehe = wasserzeichen.size
                    skalierung = max_wasserzeichen_breite / wz_breite
                    neue_wz_breite = int(wz_breite * skalierung)
                    neue_wz_hoehe = int(wz_hoehe * skalierung)
                    wasserzeichen_skaliert = wasserzeichen.resize((neue_wz_breite, neue_wz_hoehe), Image.Resampling.LANCZOS)
                    
                    # Wasserzeichen transparent machen (benutzerdefinierte Transparenz)
                    wasserzeichen_transparent = wasserzeichen_skaliert.copy()
                    alpha = wasserzeichen_transparent.split()[-1]
                    transparenz_faktor = self.transparenz_var.get() / 100
                    alpha = alpha.point(lambda p: int(p * transparenz_faktor))
                    wasserzeichen_transparent.putalpha(alpha)
                    
                    # Position für Wasserzeichen berechnen (benutzerdefiniert)
                    wz_breite, wz_hoehe = wasserzeichen_transparent.size
                    position = self.position_var.get()
                    
                    # Sicherheitsabstand von den Rändern
                    rand_abstand = max(10, int(min(bild_breite, bild_hoehe) * 0.02))
                    
                    if position == "Oben Links":
                        x, y = rand_abstand, rand_abstand
                    elif position == "Oben Mitte":
                        x, y = (bild_breite - wz_breite) // 2, rand_abstand
                    elif position == "Oben Rechts":
                        x, y = bild_breite - wz_breite - rand_abstand, rand_abstand
                    elif position == "Mitte Links":
                        x, y = rand_abstand, (bild_hoehe - wz_hoehe) // 2
                    elif position == "Mitte":
                        x, y = (bild_breite - wz_breite) // 2, (bild_hoehe - wz_hoehe) // 2
                    elif position == "Mitte Rechts":
                        x, y = bild_breite - wz_breite - rand_abstand, (bild_hoehe - wz_hoehe) // 2
                    elif position == "Unten Links":
                        x, y = rand_abstand, bild_hoehe - wz_hoehe - rand_abstand
                    elif position == "Unten Mitte":
                        x, y = (bild_breite - wz_breite) // 2, bild_hoehe - wz_hoehe - rand_abstand
                    elif position == "Unten Rechts":
                        x, y = bild_breite - wz_breite - rand_abstand, bild_hoehe - wz_hoehe - rand_abstand
                    else:
                        # Fallback auf Mitte
                        x, y = (bild_breite - wz_breite) // 2, (bild_hoehe - wz_hoehe) // 2
                    
                    # Sicherstellen, dass das Wasserzeichen im Bildbereich bleibt
                    x = max(0, min(x, bild_breite - wz_breite))
                    y = max(0, min(y, bild_hoehe - wz_hoehe))
                    
                    # Wasserzeichen auf Bild anwenden
                    bild.paste(wasserzeichen_transparent, (x, y), wasserzeichen_transparent)
                    
                    # Dateiname für Kopie erstellen
                    datei_name, datei_ext = os.path.splitext(bild_datei)
                    neuer_datei_name = f"{datei_name}_wasserzeichen{datei_ext}"
                    neuer_pfad = os.path.join(self.bilder_pfad, neuer_datei_name)
                    
                    # Bild speichern
                    if datei_ext.lower() in ['.jpg', '.jpeg']:
                        # JPEG Format unterstützt keine Transparenz
                        rgb_bild = Image.new('RGB', bild.size, (255, 255, 255))
                        rgb_bild.paste(bild, mask=bild.split()[-1] if bild.mode == 'RGBA' else None)
                        rgb_bild.save(neuer_pfad, 'JPEG', quality=95)
                    else:
                        bild.save(neuer_pfad)
                    
                    verarbeitete_bilder += 1
                    
                except Exception as e:
                    fehler_bilder.append(f"{bild_datei}: {str(e)}")
                
                # Progress bar aktualisieren
                progress_bar['value'] = i + 1
                progress_window.update()
            
            # Progress Dialog schließen
            progress_window.destroy()
            
            # Ergebnis anzeigen
            if fehler_bilder:
                fehler_text = "\n".join(fehler_bilder[:5])  # Nur erste 5 Fehler anzeigen
                if len(fehler_bilder) > 5:
                    fehler_text += f"\n... und {len(fehler_bilder) - 5} weitere Fehler"
                
                messagebox.showwarning(
                    "Verarbeitung abgeschlossen", 
                    f"Erfolgreich verarbeitet: {verarbeitete_bilder} Bilder\n"
                    f"Fehler bei: {len(fehler_bilder)} Bildern\n\n"
                    f"Fehlerdetails:\n{fehler_text}"
                )
            else:
                messagebox.showinfo(
                    "Erfolgreich abgeschlossen", 
                    f"Alle {verarbeitete_bilder} Bilder wurden erfolgreich mit Wasserzeichen versehen!\n\n"
                    f"Die neuen Dateien haben das Suffix '_wasserzeichen' und befinden sich im gleichen Ordner."
                )
                
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{str(e)}")


def main():
    root = tk.Tk()
    app = WasserzeichenGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
