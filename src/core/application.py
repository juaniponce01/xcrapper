"""Aplicación principal y procesador de partidos"""

import os
from typing import Dict, List
from ..models.data_models import PartidoInfo, JugadorEncuesta
from ..processors.file_processor import ArchivoProcesador
from ..processors.match_extractor import ExtractorPartido
from ..processors.poll_extractor import ExtractorEncuesta
from ..storage.json_storage import GuardadorJSON


class ProcesadorPartido:
    """Procesador principal para extraer datos de un partido"""
    
    def __init__(self, base_name: str):
        self.base_name = base_name
        self.archivo1_path = f"pages/{base_name}1.mhtml"
        self.archivo2_path = f"pages/{base_name}2.mhtml"
        self.extractor_partido = ExtractorPartido()
        self.extractor_encuesta = ExtractorEncuesta()
    
    def procesar(self) -> Dict:
        """Procesa ambos archivos y genera los datos del partido"""
        if not self._validar_archivos():
            raise FileNotFoundError(f"No se encontraron ambos archivos {self.archivo1_path} y {self.archivo2_path}")
        
        partido_info = self._extraer_info_partido()
        jugadores = self._extraer_jugadores()
        
        return {
            "partido": partido_info.numero,
            "fecha": partido_info.fecha,
            "rival": partido_info.rival,
            "jugadores": [jugador.to_dict() for jugador in jugadores]
        }
    
    def _validar_archivos(self) -> bool:
        """Valida que ambos archivos existan"""
        return os.path.exists(self.archivo1_path) and os.path.exists(self.archivo2_path)
    
    def _extraer_info_partido(self) -> PartidoInfo:
        """Extrae información del partido del primer archivo"""
        procesador = ArchivoProcesador(self.archivo1_path)
        articles = procesador.extraer_articles()
        
        if articles:
            return self.extractor_partido.extraer(articles[0])
        
        return PartidoInfo(None, None, None)
    
    def _extraer_jugadores(self) -> List[JugadorEncuesta]:
        """Extrae datos de jugadores de ambos archivos"""
        jugadores = []
        nombres_procesados = set()
        
        # Procesar primer archivo (saltando el primer tweet)
        jugadores.extend(self._procesar_archivo(self.archivo1_path, nombres_procesados, skip_first=True))
        
        # Procesar segundo archivo
        jugadores.extend(self._procesar_archivo(self.archivo2_path, nombres_procesados, skip_first=False))
        
        return jugadores
    
    def _procesar_archivo(self, ruta_archivo: str, nombres_procesados: set, skip_first: bool = False) -> List[JugadorEncuesta]:
        """Procesa un archivo individual y extrae jugadores"""
        procesador = ArchivoProcesador(ruta_archivo)
        articles = procesador.extraer_articles()
        jugadores = []
        
        start_index = 1 if skip_first else 0
        
        for article in articles[start_index:]:
            jugador = self.extractor_encuesta.extraer(article)
            if jugador and jugador.nombre not in nombres_procesados:
                jugadores.append(jugador)
                nombres_procesados.add(jugador.nombre)
        
        return jugadores


class AplicacionPrincipal:
    """Aplicación principal que coordina todo el proceso"""
    
    def __init__(self):
        self.guardador = GuardadorJSON()
    
    def ejecutar(self, base_name: str):
        """Ejecuta el proceso completo de extracción"""
        try:
            procesador = ProcesadorPartido(base_name)
            datos_partido = procesador.procesar()
            
            ruta_archivo = self.guardador.guardar(datos_partido, base_name)
            
            self._mostrar_resultados(ruta_archivo, datos_partido)
            
        except Exception as e:
            print(f"Error: {e}")
    
    def _mostrar_resultados(self, ruta_archivo: str, datos: Dict):
        """Muestra los resultados del procesamiento"""
        jugadores = datos.get('jugadores', [])
        
        print(f"✅ Datos guardados en {ruta_archivo}")
        print(f"Total de jugadores únicos procesados: {len(jugadores)}")