"""Modelos de datos para el proyecto"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class PartidoInfo:
    """Información básica del partido"""
    numero: Optional[int]
    fecha: Optional[str]
    rival: Optional[str]


@dataclass
class JugadorEncuesta:
    """Datos de encuesta de un jugador"""
    nombre: str
    muy_bueno: float
    bueno: float
    neutral: float
    mal: float
    total_votos: int
    
    def to_dict(self) -> Dict:
        return {
            "nombre": self.nombre,
            "muyBueno": self.muy_bueno,
            "bueno": self.bueno,
            "neutral": self.neutral,
            "mal": self.mal,
            "total": self.total_votos
        }