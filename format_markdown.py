#!/usr/bin/env python3
"""
Markdown Formatter - Formatiert Markdown-Dateien nach spezifischen Regeln
Basierend auf dem Cloudflare-Audit Dokument Format
"""

import re
import sys
import argparse
from pathlib import Path


class MarkdownFormatter:
    def __init__(self):
        self.in_code_block = False
        self.in_table = False
        
    def format_markdown(self, content: str) -> str:
        """Hauptformatierungsfunktion"""
        lines = content.split('\n')
        formatted_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Code-Block-Status verfolgen
            if line.strip().startswith('```'):
                self.in_code_block = not self.in_code_block
                formatted_lines.append(line)
                i += 1
                continue
            
            # Innerhalb von Code-Blocks nichts ändern
            if self.in_code_block:
                formatted_lines.append(line)
                i += 1
                continue
            
            # Tabellen-Status verfolgen
            if self._is_table_line(line):
                if not self.in_table:
                    self.in_table = True
                    # Leerzeile vor Tabelle einfügen
                    if formatted_lines and formatted_lines[-1].strip():
                        formatted_lines.append('')
                
                formatted_lines.append(line)
                i += 1
                
                # Prüfen ob Tabelle endet
                if i < len(lines) and not self._is_table_line(lines[i]):
                    self.in_table = False
                    # Leerzeile nach Tabelle
                    if i < len(lines) and lines[i].strip():
                        formatted_lines.append('')
                continue
            
            # Überschriften formatieren
            if line.strip().startswith('#'):
                formatted_line = self._format_heading(line)
                
                # Leerzeile vor Überschrift (außer am Anfang)
                if formatted_lines and formatted_lines[-1].strip():
                    formatted_lines.append('')
                
                formatted_lines.append(formatted_line)
                
                # Leerzeile nach Überschrift
                if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].strip().startswith('#'):
                    formatted_lines.append('')
                
                i += 1
                continue
            
            # Horizontale Linien
            if self._is_horizontal_rule(line):
                # Leerzeile vor und nach ---
                if formatted_lines and formatted_lines[-1].strip():
                    formatted_lines.append('')
                
                formatted_lines.append('---')
                
                if i + 1 < len(lines) and lines[i + 1].strip():
                    formatted_lines.append('')
                
                i += 1
                continue
            
            # Listen formatieren
            if self._is_list_item(line):
                formatted_line = self._format_list_item(line)
                formatted_lines.append(formatted_line)
                i += 1
                continue
            
            # Links formatieren
            line = self._format_links(line)
            
            # Normale Zeilen
            formatted_lines.append(line)
            i += 1
        
        # Mehrfache Leerzeilen reduzieren
        result = self._reduce_empty_lines(formatted_lines)
        
        # Am Ende genau eine Leerzeile
        result = result.rstrip('\n') + '\n'
        
        return result
    
    def _format_heading(self, line: str) -> str:
        """Formatiert Überschriften: # Heading"""
        line = line.strip()
        match = re.match(r'^(#+)\s*(.*)', line)
        if match:
            hashes, text = match.groups()
            text = text.strip()
            # Fett-Markierungen in Überschriften beibehalten
            return f"{hashes} {text}"
        return line
    
    def _is_horizontal_rule(self, line: str) -> bool:
        """Prüft ob Zeile eine horizontale Linie ist"""
        stripped = line.strip()
        return stripped in ['---', '***', '___'] or \
               re.match(r'^-{3,}$', stripped) or \
               re.match(r'^\*{3,}$', stripped) or \
               re.match(r'^_{3,}$', stripped)
    
    def _is_table_line(self, line: str) -> bool:
        """Prüft ob Zeile Teil einer Tabelle ist"""
        stripped = line.strip()
        if not stripped:
            return False
        
        # Tabellen beginnen und enthalten |
        if '|' in stripped:
            return True
        
        return False
    
    def _is_list_item(self, line: str) -> bool:
        """Prüft ob Zeile ein Listen-Element ist"""
        stripped = line.lstrip()
        # Ungeordnete Listen: - oder *
        if re.match(r'^[-*]\s+', stripped):
            return True
        # Geordnete Listen: 1. oder 1)
        if re.match(r'^\d+[.)]\s+', stripped):
            return True
        return False
    
    def _format_list_item(self, line: str) -> str:
        """Formatiert Listen-Elemente"""
        # Einrückung beibehalten
        indent = len(line) - len(line.lstrip())
        stripped = line.lstrip()
        
        # Ungeordnete Listen mit - standardisieren
        if re.match(r'^[*]\s+', stripped):
            stripped = re.sub(r'^[*]\s+', '- ', stripped)
        
        return ' ' * indent + stripped
    
    def _format_links(self, line: str) -> str:
        """Formatiert Links: [Text](URL)"""
        # Links sind bereits im richtigen Format, nur prüfen
        # [Text](URL) Format beibehalten
        return line
    
    def _reduce_empty_lines(self, lines: list) -> str:
        """Reduziert mehrfache Leerzeilen auf maximal 2"""
        result = []
        empty_count = 0
        
        for line in lines:
            if not line.strip():
                empty_count += 1
                if empty_count <= 2:
                    result.append(line)
            else:
                empty_count = 0
                result.append(line)
        
        return '\n'.join(result)


def main():
    parser = argparse.ArgumentParser(
        description='Formatiert Markdown-Dateien nach spezifischen Regeln'
    )
    parser.add_argument(
        'input',
        help='Input Markdown-Datei'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output-Datei (Standard: überschreibt Input-Datei)',
        default=None
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Erstellt Backup der Original-Datei (.bak)'
    )
    
    args = parser.parse_args()
    
    # Input-Datei einlesen
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Fehler: Datei '{args.input}' nicht gefunden!")
        sys.exit(1)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Fehler beim Lesen der Datei: {e}")
        sys.exit(1)
    
    # Formatieren
    formatter = MarkdownFormatter()
    formatted_content = formatter.format_markdown(content)
    
    # Output-Pfad bestimmen
    output_path = Path(args.output) if args.output else input_path
    
    # Backup erstellen wenn gewünscht
    if args.backup and output_path == input_path:
        backup_path = input_path.with_suffix(input_path.suffix + '.bak')
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Backup erstellt: {backup_path}")
        except Exception as e:
            print(f"⚠️  Warnung: Backup konnte nicht erstellt werden: {e}")
    
    # Formatierte Datei schreiben
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        print(f"✅ Datei erfolgreich formatiert: {output_path}")
    except Exception as e:
        print(f"❌ Fehler beim Schreiben der Datei: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
