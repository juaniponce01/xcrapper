#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Xcrapper - Extractor de datos de encuestas de X (Twitter)
Punto de entrada principal de la aplicación
"""

import sys
from src.core.application import AplicacionPrincipal


def main():
    """Función principal de la aplicación"""
    if len(sys.argv) == 1:
        base_name = "prueba"
    elif len(sys.argv) == 2:
        base_name = sys.argv[1]
    else:
        print("Uso: python main.py [nombre_base]")
        print("Ejemplo: python main.py prueba")
        print("Esto procesará prueba1.mhtml y prueba2.mhtml")
        sys.exit(1)
    
    app = AplicacionPrincipal()
    app.ejecutar(base_name)


if __name__ == "__main__":
    main()