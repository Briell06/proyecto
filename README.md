# Sistema de Gestión de Aeropuerto

Sistema Django para la coordinación de operaciones de vuelo, asignación de recursos y programación de personal.
Implementa detección automática de conflictos, validación de restricciones operacionales y reglas de negocio
aeroportuarias.

## Características

- **Gestión de pistas, puertas, aeronaves y personal**
- **Programación de vuelos con validación automática de conflictos**
- **Sistema de restricciones de recursos** (Co-requisitos y Exclusión Mutua)
- **Búsqueda inteligente de horarios disponibles**
- **Ventana de mantenimiento de 24 horas para aeronaves**
- **Requisitos dinámicos de copilotos según duración del vuelo**
- **Prevención de reservas dobles de recursos**
- **Búsqueda y filtrado de vuelos y recursos**

## Tecnologías

- Django 5.2.7
- Python 3.8+
- SQLite3
- django-mathfilters 1.0.0

## Instalación

### 0. Configuración inicial

(si desea correr el proyecto de esta forma "forma local" debería configurar el archivo settings.py y cambiar la variable
DEBUG a True)

```python
# old
DEBUG = False

# new
DEBUG = True
```

si no es asi puede visitar la pagina online accediendo
a [https://briell.pythonanywhere.com/](https://briell.pythonanywhere.com/)

### 1. Clonar repositorio

```bash
git clone https://github.com/Briell06/proyecto.git
cd "proyecto"
```

### 2. Configurar entorno virtual

### Windows

```bash
#crear el entorno virtual
python -m venv .venv

# Activar el entorno virtual
.venv\Scripts\activate

# instalar dependencias
pip install -r requirements.txt
```

### Linux/macOS

```bash
# crear el entorno virtual
python3 -m venv .venv

# activar el entorno virtual
source .venv/bin/activate

# instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar base de datos

#### Windows

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python3 manage.py migrate
```

#### Linux/macOS

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python3 manage.py migrate
```

### 4. Crear usuario administrador

#### Windows

```bash
python manage.py createsuperuser
```

#### Linux/macOS

```bash
python3 manage.py createsuperuser
```

### 5. Iniciar servidor

#### Windows

```bash
python manage.py runserver
```

#### Linux/macOS

```bash
python3 manage.py runserver
```

Acceder a [http://localhost:8000/](http://localhost:8000/)

## Uso

### Flujo de trabajo

1. **Crear recursos** (en orden):
    - Pistas: `/pistas/crear/`
    - Puertas: `/puertas/crear/`
    - Personal: `/personal/crear/` (pilotos y copilotos)
    - Aeronaves: `/aeronaves/crear/`

2. **Configurar restricciones** (opcional): `/restricciones/crear/`
    - Define correquisitos entre recursos que deben usarse juntos
    - Define exclusiones mutuas entre recursos incompatibles
    - Consulta ejemplos en la sección "Reglas de negocio"

3. **Crear vuelo**: `/vuelos/crear/`
    - Asignar pista, puerta, aeronave, piloto y copilotos
    - El sistema valida la disponibilidad y restricciones automáticamente

4. **Buscar horario disponible**: `/buscar-horario/`
    - Selecciona recursos y duración del vuelo
    - El sistema encuentra el próximo slot disponible automáticamente

5. **Consultar disponibilidad**: `/disponibilidad/`
    - Verificar recursos libres en un rango de tiempo específico

6. **Administración**: `/admin/`
    - Gestión avanzada de todos los recursos

### Ejemplo de vuelo

```text
Número: AA123
Origen: New York
Destino: Miami
Salida: 2025-10-20 10:00
Llegada: 2025-10-20 13:00
Estado: Programado
```

Seleccionar pista, puerta, aeronave, piloto y copilotos (mínimo 1 para vuelo de 3 horas).

## Reglas de negocio

### Sistema de Restricciones de Recursos

El sistema implementa dos tipos de restricciones que validan automáticamente las combinaciones de recursos en cada
vuelo:

#### 1. Co-requisitos (Inclusión Obligatoria)

Cuando se usa un recurso primario, **DEBE** incluirse un recurso complementario específico.

**Ejemplos implementables en el dominio de aeropuerto:**

- **Pista grande requiere puerta grande**: Si se asigna la Pista 01L (para aviones grandes como Boeing 747), DEBE
  asignarse una puerta grande (A1-A5) capaz de recibir aviones de esa categoría.
- **Aeronave internacional requiere personal de aduana**: Si se usa una aeronave configurada para vuelos
  internacionales, DEBE incluirse personal de aduana en el vuelo.

- **Piloto senior requiere aeronave certificada**: Si se asigna un piloto certificado en aeronaves especiales (ej:
  Boeing 787), DEBE usarse una aeronave de ese tipo específico.

**Cómo crear un co-requisito:**

1. Ve a `/restricciones/crear/`
2. Selecciona "Co-requisito" como tipo
3. Define el recurso primario (el que dispara la regla)
4. Define el recurso requerido (el que debe estar presente)

#### 2. Exclusión Mutua

Cuando se usa un recurso primario, **NO PUEDE** usarse un recurso específico en el mismo vuelo.

**Ejemplos implementables en el dominio de aeropuerto:**

- **Pistas paralelas en uso simultáneo**: Si se asigna la Pista 01L, NO PUEDE usarse la Pista 01R (pistas paralelas que
  no pueden operar simultáneamente por seguridad).

- **Puertas adyacentes**: Si un vuelo usa la Puerta A1, NO PUEDE usar la Puerta A2 (puertas adyacentes reservadas para
  aviones grandes que requieren espacio extra).

- **Incompatibilidad de aeronave-puerta**: Si se asigna un Boeing 747 (avión grande), NO PUEDE usarse la Puerta C1 (
  puerta pequeña para aviones regionales).

**Cómo crear una exclusión mutua:**

1. Ve a `/restricciones/crear/`
2. Selecciona "Exclusión Mutua" como tipo
3. Define el recurso primario
4. Define el recurso excluido (el que no puede estar presente)

#### Validación Automática

Todas las restricciones activas se validan automáticamente cuando:

- Se crea un nuevo vuelo
- Se actualiza un vuelo existente
- Se modifican los recursos asignados

Si se viola una restricción, el sistema mostrará un mensaje de error claro indicando qué regla se violó y qué recurso
falta o sobra.

### Búsqueda Inteligente de Horarios ("Buscar Hueco")

Función avanzada que encuentra automáticamente el próximo horario disponible para un vuelo.

**Cómo funciona:**

1. Especificas los recursos que necesitas (pista, puerta, aeronave, piloto)
2. Defines la duración del vuelo en horas
3. El sistema busca en los próximos 30 días
4. Valida que TODOS los recursos estén disponibles simultáneamente
5. Verifica que no se violen restricciones activas
6. Considera el período de mantenimiento de 24 horas de aeronaves

**Acceso:** `/buscar-horario/`

El algoritmo busca en incrementos de 1 hora y retorna el primer slot completamente válido encontrado.

### Requisitos de copilotos

- Vuelos ≤ 4 horas: 1 copiloto
- Vuelos 4-8 horas: 2 copilotos
- Vuelos > 8 horas: 3 copilotos

### Mantenimiento de aeronaves

Las aeronaves requieren 24 horas entre vuelos para mantenimiento obligatorio.

### Validaciones

- Longitud de pista: 800-5000 metros
- Capacidad de aeronave: 1-700 pasajeros
- Año de fabricación: 1990-presente
- Experiencia del personal: 0-50 años
- Duración máxima de vuelo: 20 horas

## Estructura del proyecto

```text
proyecto v2/
├── airline_app/      # Aplicación principal
│   ├── models.py     # Modelos de datos
│   ├── views.py      # Lógica de vistas
│   ├── forms.py      # Formularios
│   ├── urls.py       # Rutas
│   └── templates/    # Plantillas HTML
├── config/           # Configuración Django
├── manage.py         # Script de gestión
└── requirements.txt  # Dependencias
```

## Modelos principales

- **Runway**: Pistas de aterrizaje/despegue
- **Gate**: Puertas de embarque
- **Aircraft**: Aeronaves de la flota
- **Personnel**: Pilotos y copilotos
- **Flight**: Vuelos programados
- **ResourceConstraint**: Restricciones de recursos (Correquisitos y Exclusión Mutua)

## Endpoints

- `/` - Dashboard principal
- `/pistas/` - Gestión de pistas
- `/puertas/` - Gestión de puertas
- `/aeronaves/` - Gestión de aeronaves
- `/personal/` - Gestión de personal
- `/vuelos/` - Gestión de vuelos
- `/restricciones/` - Gestión de restricciones de recursos
- `/buscar-horario/` - Búsqueda inteligente de horarios
- `/disponibilidad/` - Consulta de disponibilidad
- `/admin/` - Interfaz de administración

## Configuración

Archivo principal: `config/settings.py`

- `DEBUG = True` - Activar solo en desarrollo
- `LANGUAGE_CODE = "es-mx"` - Localización en español
- `TIME_ZONE = "America/Havana"` - Zona horaria

## Licencia

Proyecto desarrollado para la Universidad de la Habana en la carrera de Ciencias de la Computación.

© Briell Quintana Hernández 2025