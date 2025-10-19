# Sistema de Gestión de Aeropuerto

Sistema Django para la coordinación de operaciones de vuelo, asignación de recursos y programación de personal. Implementa detección automática de conflictos, validación de restricciones operacionales y reglas de negocio aeroportuarias.

## Características

- Gestión de pistas, puertas, aeronaves y personal
- Programación de vuelos con validación automática de conflictos
- Ventana de mantenimiento de 24 horas para aeronaves
- Requisitos dinámicos de copilotos según duración del vuelo
- Prevención de reservas dobles de recursos
- Búsqueda y filtrado de vuelos y recursos

## Tecnologías

- Django 5.2.7
- Python 3.8+
- SQLite3
- django-mathfilters 1.0.0

## Instalación

### 1. Clonar repositorio

```bash
git clone <repository-url>
cd "proyecto v2"
```

### 2. Configurar entorno virtual

#### Windows

```bash
# Crear entorno virtual
python -m venv env

# Activar entorno virtual
env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

#### Linux

```bash
# Crear entorno virtual
python3 -m venv env

# Activar entorno virtual
source env/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### macOS

```bash
# Crear entorno virtual
python3 -m venv env

# Activar entorno virtual
source env/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar base de datos

#### Windows

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

#### Linux/macOS

```bash
# Crear migraciones
python3 manage.py makemigrations

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

2. **Crear vuelo**: `/vuelos/crear/`

   - Asignar pista, puerta, aeronave, piloto y copilotos
   - El sistema valida disponibilidad automáticamente

3. **Consultar disponibilidad**: `/disponibilidad/`

   - Verificar recursos libres en un rango de tiempo

4. **Administración**: `/admin/`
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

## Endpoints

- `/pistas/` - Gestión de pistas
- `/puertas/` - Gestión de puertas
- `/aeronaves/` - Gestión de aeronaves
- `/personal/` - Gestión de personal
- `/vuelos/` - Gestión de vuelos
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
