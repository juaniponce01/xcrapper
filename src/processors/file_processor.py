"""Procesador de archivos MHTML"""

import os
import email
from email import policy
from typing import List, Optional
from bs4 import BeautifulSoup


class ArchivoProcesador:
    """Maneja la lectura y procesamiento de archivos MHTML"""
    
    ENCODINGS = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    def __init__(self, ruta_archivo: str):
        self.ruta_archivo = ruta_archivo
    
    def extraer_articles(self) -> List:
        """Extrae articles de un archivo MHTML"""
        content = self._leer_archivo()
        if not content:
            return []
        
        html_content = self._extraer_html_de_mhtml(content)
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.find_all('article')
    
    def _leer_archivo(self) -> Optional[str]:
        """Lee el archivo con diferentes codificaciones"""
        try:
            for encoding in self.ENCODINGS:
                try:
                    with open(self.ruta_archivo, 'r', encoding=encoding) as file:
                        return file.read()
                except UnicodeDecodeError:
                    continue
            
            # Último intento: leer como binario
            with open(self.ruta_archivo, 'rb') as file:
                raw_content = file.read()
                return raw_content.decode('utf-8', errors='replace')
                
        except Exception:
            return None
    
    def _extraer_html_de_mhtml(self, content: str) -> str:
        """Extrae el contenido HTML de un archivo MHTML"""
        if not (content.startswith('MIME-Version:') or 'Content-Type: multipart/related' in content):
            return content
        
        try:
            msg = email.message_from_string(content, policy=policy.default)
            for part in msg.walk():
                if part.get_content_type() == 'text/html':
                    return part.get_content()
        except Exception:
            pass
        
        return content