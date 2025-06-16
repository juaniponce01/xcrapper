"""Extractor de encuestas de jugadores"""

import re
from typing import List, Optional
from ..models.data_models import JugadorEncuesta


class ExtractorEncuesta:
    """Extrae datos de encuestas de jugadores"""
    
    REGEX_PORCENTAJE = re.compile(r'(\d+(?:[,\.]\d+)?)\s*%')
    REGEX_VOTOS = re.compile(r'(\d+(?:\.\d{3})*)')
    
    def extraer(self, article) -> Optional[JugadorEncuesta]:
        """Extrae datos de una encuesta individual"""
        if not self._tiene_encuesta(article):
            return None
        
        nombre = self._extraer_nombre_jugador(article)
        porcentajes = self._extraer_porcentajes(article)
        total_votos = self._extraer_total_votos(article)
        
        return JugadorEncuesta(
            nombre=nombre,
            muy_bueno=porcentajes[0] if len(porcentajes) > 0 else 0,
            bueno=porcentajes[1] if len(porcentajes) > 1 else 0,
            neutral=porcentajes[2] if len(porcentajes) > 2 else 0,
            mal=porcentajes[3] if len(porcentajes) > 3 else 0,
            total_votos=total_votos
        )
    
    def _tiene_encuesta(self, article) -> bool:
        """Verifica si un article tiene una encuesta"""
        opciones_encuesta = article.find_all('div', string=lambda text: text and '%' in text)
        return len(opciones_encuesta) > 0
    
    def _extraer_nombre_jugador(self, article) -> str:
        """Extrae el nombre del jugador del tweet"""
        tweet_text = article.find('div', {'data-testid': 'tweetText'})
        
        if tweet_text:
            nombre_span = tweet_text.find('span')
            if nombre_span:
                nombre_completo = nombre_span.get_text().strip()
            else:
                nombre_completo = tweet_text.get_text().strip()
        else:
            nombre_completo = "Desconocido"
        
        return ' '.join(nombre_completo.split())
    
    def _extraer_porcentajes(self, article) -> List[float]:
        """Extrae los porcentajes de la encuesta"""
        opciones_encuesta = article.find_all('div', string=lambda text: text and '%' in text)
        porcentajes = []
        opciones_unicas = set()
        
        for opcion in opciones_encuesta:
            texto = opcion.get_text().strip()
            
            if texto not in opciones_unicas and '%' in texto:
                opciones_unicas.add(texto)
                match = self.REGEX_PORCENTAJE.search(texto)
                if match:
                    porcentaje_str = match.group(1).replace(',', '.')
                    porcentajes.append(float(porcentaje_str))
        
        return porcentajes
    
    def _extraer_total_votos(self, article) -> int:
        """Extrae el total de votos de la encuesta"""
        poll_containers = article.find_all('div', recursive=True)
        
        for container in poll_containers:
            spans = container.find_all('span')
            for span in spans:
                texto_span = span.get_text().strip()
                if 'votos' in texto_span.lower() or 'votes' in texto_span.lower():
                    match = self.REGEX_VOTOS.search(texto_span)
                    if match:
                        numero_votos = match.group(1).replace('.', '')
                        return int(numero_votos)
        
        return 0