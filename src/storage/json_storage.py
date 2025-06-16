"""Guardado de datos en formato JSON"""

import os
import json
from typing import Dict


class GuardadorJSON:
    """Maneja el guardado de datos en formato JSON"""
    
    def __init__(self, directorio_output: str = "data"):
        self.directorio_output = directorio_output
    
    def guardar(self, datos: Dict, nombre_archivo: str) -> str:
        """Guarda los datos en un archivo JSON"""
        os.makedirs(self.directorio_output, exist_ok=True)
        ruta_archivo = os.path.join(self.directorio_output, f"{nombre_archivo}.json")
        
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        
        return ruta_archivo