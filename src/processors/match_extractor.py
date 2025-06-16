"""Extractor de información del partido"""

import re
from typing import Optional
from ..models.data_models import PartidoInfo


class ExtractorPartido:
    """Extrae información del partido del primer tweet"""
    
    REGEX_PARTIDO = re.compile(r'partido\s*(\d+)', re.IGNORECASE)
    REGEX_FECHA = re.compile(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})')
    REGEX_RIVAL = re.compile(r'[^\w\s]*([A-Za-zÀ-ÿ\s]+)')
    
    def extraer(self, article) -> PartidoInfo:
        """Extrae información del partido del primer tweet"""
        tweet_text = article.find('div', {'data-testid': 'tweetText'})
        if not tweet_text:
            return PartidoInfo(None, None, None)
        
        texto = tweet_text.get_text().strip()
        
        numero = self._extraer_numero_partido(texto)
        fecha = self._extraer_fecha(texto)
        rival = self._extraer_rival(texto, fecha)
        
        return PartidoInfo(numero, fecha, rival)
    
    def _extraer_numero_partido(self, texto: str) -> Optional[int]:
        """Extrae el número del partido"""
        match = self.REGEX_PARTIDO.search(texto)
        return int(match.group(1)) if match else None
    
    def _extraer_fecha(self, texto: str) -> Optional[str]:
        """Extrae la fecha del partido"""
        match = self.REGEX_FECHA.search(texto)
        return match.group(1) if match else None
    
    def _extraer_rival(self, texto: str, fecha: Optional[str]) -> Optional[str]:
        """Extrae el nombre del rival"""
        if not fecha:
            return None
        
        fecha_match = self.REGEX_FECHA.search(texto)
        if not fecha_match:
            return None
        
        end_pos = fecha_match.end()
        texto_despues_fecha = texto[end_pos:].strip()
        
        rival_match = self.REGEX_RIVAL.search(texto_despues_fecha)
        return rival_match.group(1).strip() if rival_match else None