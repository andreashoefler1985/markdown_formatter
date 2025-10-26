# Markdown Formatter

Ein **Python-basierter Markdown-Formatter**, der deine Markdown-Dateien nach konsistenten Regeln formatiert und bereinigt.

---

## 📋 Inhaltsverzeichnis
- [Features](#✨-features)
- [Voraussetzungen](#📦-voraussetzungen)
- [Installation](#🚀-installation)
- [Verwendung](#💻-verwendung)
- [Formatierungsregeln](#📐-formatierungsregeln)
- [Beispiele](#📝-beispiele)
- [Joplin Integration](#📓-joplin-integration)
- [Troubleshooting](#🔧-troubleshooting)
- [Lizenz](#📄-lizenz)

---

## ✨ Features
- **Überschriften-Formatierung**: Konsistente Abstände und Format für alle Überschriftsebenen
- **Leerzeilen-Management**: Automatisches Einfügen und Bereinigen von Leerzeilen
- **Horizontale Linien**: Standardisierung zu `---`
- **Listen-Formatierung**: Einheitliche Formatierung von Listen-Elementen
- **Tabellen-Erkennung**: Erhält Tabellen-Strukturen
- **Code-Block-Schutz**: Lässt Code-Blocks unverändert
- **Link-Formatierung**: Behält `[Text](URL)` Format bei
- **Backup-Funktion**: Optional Backup vor Formatierung

---

## 📦 Voraussetzungen
- **Python 3.6 oder höher**
- Keine externen Abhängigkeiten erforderlich (nur Python Standard Library)

---

## 🚀 Installation

### Variante 1: Direkte Verwendung
1. Repository klonen oder Script herunterladen:
   ```bash
   git clone https://github.com/dein-username/markdown-formatter.git
   cd markdown-formatter
   ```
2. Script ausführbar machen (optional):
   ```bash
   chmod +x format_markdown.py
   ```

### Variante 2: Globale Installation
Um das Script von überall aufrufen zu können:
```bash
# Script nach /usr/local/bin kopieren
sudo cp format_markdown.py /usr/local/bin/format-markdown
sudo chmod +x /usr/local/bin/format-markdown
# Dann von überall verwendbar:
format-markdown deine-datei.md
```

---

## 💻 Verwendung

### Basis-Verwendung
```bash
# Datei direkt formatieren (überschreibt Original)
python3 format_markdown.py deine-datei.md

# Mit Backup (erstellt .bak Datei)
python3 format_markdown.py deine-datei.md --backup

# In neue Datei schreiben
python3 format_markdown.py input.md -o output.md

# Hilfe anzeigen
python3 format_markdown.py --help
```

### Parameter
| Parameter       | Beschreibung                                      |
|-----------------|--------------------------------------------------|
| `input`         | Pfad zur Markdown-Datei (erforderlich)           |
| `-o, --output` | Output-Datei (Standard: überschreibt Input)      |
| `--backup`      | Erstellt Backup der Original-Datei (.bak)        |
| `-h, --help`    | Zeigt Hilfe an                                    |

---

## 📐 Formatierungsregeln

### Überschriften
**Vorher:**
```markdown
#Überschrift ohne Leerzeichen
##  Überschrift mit zu vielen Leerzeichen
```
**Nachher:**
```markdown
# Überschrift ohne Leerzeichen
## Überschrift mit zu vielen Leerzeichen
```
- Genau ein Leerzeichen nach `#`
- Leerzeile vor Überschrift (außer am Dokumentanfang)
- Leerzeile nach Überschrift

### Horizontale Linien
**Vorher:**
```markdown
***
___
----------
```
**Nachher:**
```markdown
---
---
---
```
- Standardisiert zu `---`
- Leerzeile vor und nach der Linie

### Listen
**Vorher:**
```markdown
* Element 1
* Element 2
  * Unterelement
```
**Nachher:**
```markdown
- Element 1
- Element 2
  - Unterelement
```
- Ungsortierte Listen nutzen `-` statt `*`
- Einrückung wird beibehalten

### Tabellen
Tabellen werden erkannt und in ihrer Struktur beibehalten:
```markdown
| Spalte 1 | Spalte 2 |
|----------|----------|
| Wert 1   | Wert 2   |
```
- Leerzeile vor und nach Tabelle
- Struktur bleibt unverändert

### Code-Blocks
Code-Blocks werden nicht formatiert:
````markdown
```python
def hello():
    print("Bleibt unverändert!")
```
````
- Leerzeilen: Mehrfache Leerzeilen werden auf maximal 2 reduziert
- Konsistente Abstände zwischen Elementen
- Dokument endet mit genau einer Leerzeile

---

## 📝 Beispiele

### Beispiel 1: Einfache Formatierung
**Input (beispiel.md):**
```markdown
#Überschrift
Text ohne Abstand
##Unterüberschrift
***
* Liste 1
* Liste 2
```
**Befehl:**
```bash
python3 format_markdown.py beispiel.md --backup
```
**Output:**
```markdown
# Überschrift

Text ohne Abstand

## Unterüberschrift

---
- Liste 1
- Liste 2
```

### Beispiel 2: Mehrere Dateien formatieren
```bash
# Bash-Script für mehrere Dateien
for file in *.md; do
    python3 format_markdown.py "$file" --backup
done
```

### Beispiel 3: Vor dem Commit formatieren
```bash
# Git Hook (.git/hooks/pre-commit)
#!/bin/bash
for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.md$'); do
    python3 format_markdown.py "$file"
    git add "$file"
done
```

---

## 📓 Joplin Integration

### Export-Import-Workflow
1. Notiz aus Joplin exportieren:
   - Rechtsklick auf Notiz → "Export" → "Markdown"
   - Datei speichern (z.B. `notiz.md`)
2. Formatieren:
   ```bash
   python3 format_markdown.py notiz.md --backup
   ```
3. Zurück in Joplin importieren:
   - "File" → "Import" → "MD - Markdown"
   - Formatierte Datei auswählen

### Empfohlene Joplin-Einstellungen
| Aktiviert | Deaktiviert |
|-----------|-------------|
| ✅ Weiche Zeilenumbrüche aktivieren | ❌ Syntax `==mark==` aktivieren |
| ✅ Unterstützung von Typographie aktivieren | ❌ Syntax `sub` aktivieren |
| ✅ Linkify aktivieren | ❌ Syntax `^sup^` aktivieren |
| | ❌ Markdown Emoji aktivieren |
| | ❌ Syntax `++insert++` aktivieren |

---

## 🔧 Troubleshooting

| Problem | Lösung |
|---------|--------|
| **"Permission denied"** | `chmod +x format_markdown.py` |
| **"File not found"** | Absoluten Pfad verwenden oder ins richtige Verzeichnis wechseln |
| **Encoding-Fehler** | Datei zu UTF-8 konvertieren: `iconv -f ISO-8859-1 -t UTF-8 input.md > output.md` |
| **Code-Blocks werden formatiert** | Stelle sicher, dass Code-Blocks korrekt mit ```` ``` ```` geöffnet und geschlossen werden. |

---

## 🛠️ Anpassungen
### Eigene Formatierungsregeln hinzufügen
```python
def _custom_format(self, line: str) -> str:
    """Deine eigene Formatierungsregel"""
    # Beispiel: Alle TODO in Großbuchstaben
    return line.replace('todo', 'TODO')
```
Füge die Funktion in die `MarkdownFormatter`-Klasse ein und rufe sie in `format_markdown()` auf.

---

## 📊 Features Roadmap
- Tabellen automatisch ausrichten
- Sortier-Optionen für Listen
- Unterstützung für Frontmatter (YAML)
- Interaktiver Modus
- Konfigurations-Datei (`.mdformat.json`)
- Watch-Modus für automatische Formatierung
- Integration mit VS Code Extension

---

## 🤝 Beitragen
Contributions sind willkommen! Bitte:
1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

---

## 📄 Lizenz
**MIT License** – siehe [LICENSE](LICENSE) Datei für Details.

---

## 👤 Autor
Erstellt von Andreas Höfler für Standard-Markdown-Dokumenten.
```
