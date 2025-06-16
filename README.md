# Xcrapper ⚽

**Extractor de datos de encuestas de X (Twitter) para análisis de rendimiento de jugadores**

Xcrapper es una herramienta que permite extraer y procesar automáticamente los datos de encuestas sobre rendimiento de jugadores publicadas en X (anteriormente Twitter), convirtiendo archivos MHTML en datos estructurados JSON.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso](#uso)
- [Casos de Uso](#casos-de-uso)
- [Arquitectura](#arquitectura)
- [Datos de Salida](#datos-de-salida)
- [Contribuir](#contribuir)

## ✨ Características

- ✅ Procesamiento automático de archivos MHTML
- ✅ Extracción de información del partido (número, fecha, rival)
- ✅ Detección automática de encuestas de jugadores
- ✅ Manejo de caracteres especiales (tildes, eñes)
- ✅ Prevención de duplicados entre archivos
- ✅ Salida en formato JSON estructurado
- ✅ Arquitectura modular y extensible

## 🚀 Instalación

### Prerequisitos

- Python 3.8+
- pip

### Dependencias

```bash
pip install beautifulsoup4 lxml
```

### Configuración

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/xcrapper.git
cd xcrapper
```

2. Crear las carpetas necesarias:
```bash
mkdir pages data
```

## 📁 Estructura del Proyecto

```
xcrapper/
├── main.py                    # Punto de entrada principal
├── README.md                  # Documentación
├── src/                       # Código fuente
│   ├── __init__.py
│   ├── models/                # Modelos de datos
│   │   ├── __init__.py
│   │   └── data_models.py     # Estructuras de datos (PartidoInfo, JugadorEncuesta)
│   ├── processors/            # Procesadores de datos
│   │   ├── __init__.py
│   │   ├── file_processor.py  # Manejo de archivos MHTML
│   │   ├── match_extractor.py # Extracción info del partido
│   │   └── poll_extractor.py  # Extracción datos de encuestas
│   ├── storage/               # Almacenamiento
│   │   ├── __init__.py
│   │   └── json_storage.py    # Guardado en formato JSON
│   └── core/                  # Lógica principal
│       ├── __init__.py
│       └── application.py     # Coordinador principal
├── pages/                     # Archivos MHTML de entrada
│   ├── partido1.mhtml
│   ├── partido2.mhtml
│   └── ...
└── data/                      # Archivos JSON de salida
    ├── partido.json
    └── ...
```

## 🎯 Uso

### Uso Básico

```bash
# Procesar archivos por defecto (prueba1.mhtml y prueba2.mhtml)
python main.py

# Procesar archivos específicos
python main.py partido5
# Esto procesará partido51.mhtml y partido52.mhtml
```

### Preparación de Archivos

1. **Guardar páginas de Twitter como MHTML:**
   - Navega al perfil o hilo de tweets con las encuestas
   - Presiona `Ctrl+S` (Windows/Linux) o `Cmd+S` (Mac)
   - Selecciona formato "Página web, archivos únicos (*.mhtml)"
   - Guarda como `nombre1.mhtml` y `nombre2.mhtml` en la carpeta `pages/`

2. **Estructura esperada de los tweets:**
   - **Primer tweet:** Información del partido (ej: "Partido 15 12/03/2024 ⚔️ Real Madrid")
   - **Tweets siguientes:** Encuestas con nombre del jugador y opciones de rendimiento

## 💼 Casos de Uso

### 1. Análisis de Rendimiento Post-Partido

**Escenario:** Después de cada partido, quieres analizar las opiniones de los aficionados sobre el rendimiento de cada jugador.

**Proceso:**
1. Recopilar encuestas de Twitter sobre jugadores
2. Guardar como MHTML (dividido en 2 archivos por limitaciones de tamaño)
3. Ejecutar `python main.py partido15`
4. Obtener datos estructurados en `data/partido15.json`

### 2. Seguimiento de Temporada

**Escenario:** Mantener un registro completo de evaluaciones de jugadores durante toda la temporada.

**Estructura de archivos:**
```
pages/
├── jornada01_1.mhtml
├── jornada01_2.mhtml
├── jornada02_1.mhtml
├── jornada02_2.mhtml
└── ...
```

**Ejecución:**
```bash
python main.py jornada01
python main.py jornada02
# ... para cada jornada
```

### 3. Análisis Comparativo

**Escenario:** Comparar el rendimiento percibido de jugadores entre diferentes partidos.

**Resultado:** Archivos JSON que permiten análisis posterior con herramientas como pandas, Excel, etc.

## 🏗️ Arquitectura

### Componentes Principales

#### 1. `data_models.py` - Modelos de Datos
**Propósito:** Define las estructuras de datos inmutables.

```python
@dataclass
class PartidoInfo:
    numero: Optional[int]    # Número del partido
    fecha: Optional[str]     # Fecha del partido  
    rival: Optional[str]     # Equipo rival

@dataclass
class JugadorEncuesta:
    nombre: str             # Nombre del jugador
    muy_bueno: float        # Porcentaje "Muy bueno"
    bueno: float           # Porcentaje "Bueno"
    neutral: float         # Porcentaje "Neutral"
    mal: float             # Porcentaje "Mal"
    total_votos: int       # Total de votos
```

#### 2. `file_processor.py` - Procesador de Archivos
**Propósito:** Maneja la lectura y procesamiento de archivos MHTML.

**Funcionalidades:**
- Detección automática de codificación
- Extracción de HTML desde MHTML
- Manejo robusto de errores de codificación
- Parseo con BeautifulSoup

#### 3. `match_extractor.py` - Extractor de Información del Partido
**Propósito:** Extrae metadatos del partido desde el primer tweet.

**Patrones de extracción:**
- `partido\s*(\d+)` → Número del partido
- `(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})` → Fecha
- Texto después de la fecha → Nombre del rival

#### 4. `poll_extractor.py` - Extractor de Encuestas
**Propósito:** Extrae datos de encuestas de jugadores.

**Proceso:**
1. Detecta presencia de encuesta (busca elementos con '%')
2. Extrae nombre del jugador desde `<span>` dentro del tweet
3. Extrae porcentajes usando regex `(\d+(?:[,\.]\d+)?)\s*%`
4. Extrae total de votos buscando texto con "votos"/"votes"

#### 5. `json_storage.py` - Almacenamiento JSON
**Propósito:** Guarda los datos procesados en formato JSON.

**Características:**
- Codificación UTF-8 para caracteres especiales
- Formato indentado para legibilidad
- Creación automática de directorios

#### 6. `application.py` - Coordinador Principal
**Propósito:** Orquesta todo el proceso de extracción.

**Flujo:**
1. Valida existencia de archivos
2. Extrae información del partido
3. Procesa jugadores de ambos archivos
4. Elimina duplicados
5. Guarda resultado en JSON

## 📊 Datos de Salida

### Formato JSON

```json
{
  "partido": 15,
  "fecha": "12/03/2024",
  "rival": "Real Madrid",
  "jugadores": [
    {
      "nombre": "Lionel Messi",
      "muyBueno": 45.2,
      "bueno": 38.1,
      "neutral": 12.4,
      "mal": 4.3,
      "total": 1256
    },
    {
      "nombre": "Ángel Di María",
      "muyBueno": 12.7,
      "bueno": 45.8,
      "neutral": 31.2,
      "mal": 10.3,
      "total": 987
    }
  ]
}
```

### Campos Explicados

- **partido:** Número identificador del partido
- **fecha:** Fecha del partido en formato original
- **rival:** Nombre del equipo rival
- **jugadores:** Array de evaluaciones por jugador
  - **nombre:** Nombre completo del jugador
  - **muyBueno/bueno/neutral/mal:** Porcentajes de cada categoría
  - **total:** Número total de votos en la encuesta

## 🔧 Personalización

### Agregar Nuevos Extractores

Para agregar soporte a nuevos tipos de datos:

1. Crear nuevo extractor en `src/processors/`
2. Implementar interfaz similar a extractores existentes
3. Integrar en `application.py`

### Cambiar Formato de Salida

Para soportar otros formatos (CSV, XML, etc.):

1. Crear nuevo guardador en `src/storage/`
2. Implementar método `guardar()`
3. Configurar en `AplicacionPrincipal`

### Modificar Patrones de Extracción

Los patrones regex están centralizados en cada extractor:

```python
# En match_extractor.py
REGEX_PARTIDO = re.compile(r'partido\s*(\d+)', re.IGNORECASE)
REGEX_FECHA = re.compile(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})')

# En poll_extractor.py  
REGEX_PORCENTAJE = re.compile(r'(\d+(?:[,\.]\d+)?)\s*%')
REGEX_VOTOS = re.compile(r'(\d+(?:\.\d{3})*)')
```

## 🐛 Solución de Problemas

### Caracteres Especiales Corruptos

**Problema:** Nombres como "Martínez" aparecen como "Mart��nez"

**Solución:** El procesador intenta múltiples codificaciones automáticamente. Si persiste:

```bash
# Verificar codificación del archivo
file -I pages/archivo.mhtml

# Ejecutar con variables de entorno
export PYTHONIOENCODING=utf-8
python main.py
```

### Archivos No Encontrados

**Problema:** `FileNotFoundError`

**Verificar:**
1. Archivos están en carpeta `pages/`
2. Nombres siguen el patrón `nombre1.mhtml` y `nombre2.mhtml`
3. Permisos de lectura correctos

### Encuestas No Detectadas

**Problema:** No se extraen datos de jugadores

**Verificar:**
1. Los tweets contienen elementos con símbolo '%'
2. La estructura HTML corresponde a encuestas de Twitter/X
3. Los articles están siendo extraídos correctamente

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙋‍♂️ Soporte

Para reportar bugs o solicitar funcionalidades, crear un issue en GitHub.

---

**Desarrollado con ❤️ para el análisis de datos deportivos**