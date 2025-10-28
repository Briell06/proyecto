from typing import Any
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class Runway(models.Model):
    """
    Representa una pista para las operaciones de aterrizaje y despegue del aeropuerto.
    Cada pista puede ser asignada a un vuelo a la vez.
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    runway_code = models.CharField(
        max_length=10, unique=True, verbose_name="Código de Pista"
    )
    length_meters = models.PositiveIntegerField(verbose_name="Longitud (metros)")
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pista"
        verbose_name_plural = "Pistas"
        ordering = ["runway_code"]

    def clean(self):
        if not (800 <= self.length_meters <= 5000):
            raise ValidationError(
                "La longitud de la pista debe estar entre 800 y 5000 metros."
            )

    def __str__(self):
        return f"{self.runway_code} - {self.name}"

    def is_available(self, start_time, end_time, exclude_flight_id=None):
        """
        Checkea si la pista está disponible para el marco de tiempo dado.

        Args:
            start_time: Fecha de inicio
            end_time: Fecha de fin
            exclude_flight_id: ID de vuelo para excluir (para actualizaciones)

        Returns:
            bool: True si está disponible, False si no lo está
        """
        from django.db.models import Q

        conflicting_flights = Flight.objects.filter(
            runway=self, status__in=["SCHEDULED", "IN_PROGRESS"]
        ).filter(Q(departure_time__lt=end_time) & Q(arrival_time__gt=start_time))

        if exclude_flight_id:
            conflicting_flights = conflicting_flights.exclude(id=exclude_flight_id)

        return not conflicting_flights.exists()


class Gate(models.Model):
    """
    Representa una puerta de abordaje donde los pasajeros suben al avión.
    Cada puerta puede ser asignada a un vuelo a la vez.
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    gate_code = models.CharField(
        max_length=10, unique=True, verbose_name="Código de Puerta"
    )
    terminal = models.CharField(max_length=50, verbose_name="Terminal")
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Puerta de Embarque"
        verbose_name_plural = "Puertas de Embarque"
        ordering = ["gate_code"]

    def __str__(self):
        return f"{self.gate_code} - {self.terminal}"

    def is_available(self, start_time, end_time, exclude_flight_id=None):
        """
        Checkea si la puerta de abordaje está disponible para el marco de tiempo dado.

        Args:
            start_time: Fecha de inicio
            end_time: Fecha de fin
            exclude_flight_id: ID de vuelo para excluir (para actualizaciones)

        Returns:
            bool: True si está disponible, False si no lo está
        """
        from django.db.models import Q

        conflicting_flights = Flight.objects.filter(
            gate=self, status__in=["SCHEDULED", "IN_PROGRESS"]
        ).filter(Q(departure_time__lt=end_time) & Q(arrival_time__gt=start_time))

        if exclude_flight_id:
            conflicting_flights = conflicting_flights.exclude(id=exclude_flight_id)

        return not conflicting_flights.exists()


class Personnel(models.Model):
    """
    Representa el personal del aeropuerto (pilotos y copilotos).
    Cada persona puede ser asignada a un vuelo a la vez.
    """

    PERSONNEL_TYPES = [
        ("PILOT", "Piloto"),
        ("COPILOT", "Copiloto"),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    employee_id = models.CharField(
        max_length=20, unique=True, verbose_name="ID de Empleado"
    )
    personnel_type = models.CharField(
        max_length=10, choices=PERSONNEL_TYPES, verbose_name="Tipo de Personal"
    )
    license_number = models.CharField(
        max_length=50, unique=True, verbose_name="Número de Licencia"
    )
    years_of_experience = models.PositiveIntegerField(
        verbose_name="Años de Experiencia"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Personal"
        verbose_name_plural = "Personal"
        ordering = ["last_name", "first_name"]

    def clean(self):
        errors = {}
        if self.years_of_experience > 50:
            errors["years_of_experience"] = [
                ValidationError(
                    "El personal no puede tener más de 50 años de experiencia."
                )
            ]

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.get_personnel_type_display()} - {self.first_name} {self.last_name} ({self.employee_id})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_available(self, start_time, end_time, exclude_flight_id=None):
        """
        Checkea si el personal seleccionado está disponible para el marco de tiempo dado.

        Args:
            start_time: Fecha de inicio
            end_time: Fecha de fin
            exclude_flight_id: ID de vuelo para excluir (para actualizaciones)

        Returns:
            bool: True si está disponible, False si no lo está
        """
        from django.db.models import Q

        # Checkea los vuelos donde este piloto está asignado
        pilot_flights = Flight.objects.filter(
            pilot=self, status__in=["SCHEDULED", "IN_PROGRESS"]
        ).filter(Q(departure_time__lt=end_time) & Q(arrival_time__gt=start_time))

        # Checkea los vuelos donde este copiloto está asignado
        copilot_flights = Flight.objects.filter(
            copilots=self, status__in=["SCHEDULED", "IN_PROGRESS"]
        ).filter(Q(departure_time__lt=end_time) & Q(arrival_time__gt=start_time))

        if exclude_flight_id:
            pilot_flights = pilot_flights.exclude(id=exclude_flight_id)
            copilot_flights = copilot_flights.exclude(id=exclude_flight_id)

        return not (pilot_flights.exists() or copilot_flights.exists())


class Aircraft(models.Model):
    """
    Representa los aviones del aeropuerto.
    Los aviones requieren 24 horas de mantenimiento obligatorio entre vuelos [pequeño toque personal :)].
    """

    AIRCRAFT_STATUS = [
        ("OPERATIONAL", "Operacional"),
        ("MAINTENANCE", "Mantenimiento"),
        ("OUT_OF_SERVICE", "Fuera de Servicio"),
    ]

    registration_number = models.CharField(
        max_length=20, unique=True, verbose_name="Número de Registro"
    )
    model = models.CharField(max_length=100, verbose_name="Modelo")
    manufacturer = models.CharField(max_length=100, verbose_name="Fabricante")
    capacity = models.PositiveIntegerField(verbose_name="Capacidad de Pasajeros")
    year_manufactured = models.PositiveIntegerField(verbose_name="Año de Fabricación")
    status = models.CharField(
        max_length=20,
        choices=AIRCRAFT_STATUS,
        default="OPERATIONAL",
        verbose_name="Estado",
    )
    last_maintenance_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Última Fecha de Mantenimiento"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Aeronave"
        verbose_name_plural = "Aeronaves"
        ordering = ["registration_number"]

    def __str__(self):
        return f"{self.registration_number} - {self.manufacturer} {self.model}"

    def is_available(self, start_time, end_time, exclude_flight_id=None):
        """
        Checkea si el avión está disponible para el marco de tiempo dado.

        Args:
            start_time: Fecha de inicio
            end_time: Fecha de fin
            exclude_flight_id: ID de vuelo para excluir (para actualizaciones)

        Returns:
            bool: True si está disponible, False si no lo está
        """
        from django.db.models import Q

        # Check if aircraft is operational
        if self.status != "OPERATIONAL":
            return False

        # Add 24-hour maintenance buffer before and after the requested time
        buffer_start = start_time - timedelta(hours=24)
        buffer_end = end_time + timedelta(hours=24)

        conflicting_flights = Flight.objects.filter(
            aircraft=self, status__in=["SCHEDULED", "IN_PROGRESS", "COMPLETED"]
        ).filter(Q(departure_time__lt=buffer_end) & Q(arrival_time__gt=buffer_start))

        if exclude_flight_id:
            conflicting_flights = conflicting_flights.exclude(id=exclude_flight_id)

        return not conflicting_flights.exists()

    def clean(self):
        errors = {}
        if self.capacity == 0 or self.capacity > 700:
            errors["capacity"] = [
                ValidationError(
                    "La capacidad de pasajeros debe ser mayor a 0 y menor a 700."
                )
            ]

        if (
            self.year_manufactured < 1990
            or self.year_manufactured > timezone.now().year
        ):
            errors["year_manufactured"] = [
                ValidationError(
                    "El año de fabricación debe ser mayor a 1990 y menor al año actual."
                )
            ]

        if errors:
            raise ValidationError(errors)


class Flight(models.Model):
    """
    Representa el evento de "vuelo", evento principal del programa que consume los recursos asignados.
    Cada vuelo tiene que tener asignado 1 recurso de cada tipo y el personal correspondiente en dependencia de la duración del vuelo.
    Este modelo valida los conflictos de vuelos simultáneos y recursos asignados simultáneamente.
    """

    FLIGHT_STATUS = [
        ("SCHEDULED", "Programado"),
        ("IN_PROGRESS", "En Progreso"),
        ("COMPLETED", "Completado"),
        ("CANCELLED", "Cancelado"),
        ("DELAYED", "Retrasado"),
    ]

    flight_number = models.CharField(
        max_length=20, unique=True, verbose_name="Número de Vuelo"
    )
    origin = models.CharField(max_length=100, verbose_name="Origen")
    destination = models.CharField(max_length=100, verbose_name="Destino")
    departure_time = models.DateTimeField(verbose_name="Hora de Salida")
    arrival_time = models.DateTimeField(verbose_name="Hora de Llegada")
    status = models.CharField(
        max_length=20, choices=FLIGHT_STATUS, default="SCHEDULED", verbose_name="Estado"
    )

    # Asignación de recursos (requerido que sea 1 de cada tipo)
    runway = models.ForeignKey(
        Runway, on_delete=models.PROTECT, related_name="flights", verbose_name="Pista"
    )
    gate = models.ForeignKey(
        Gate, on_delete=models.PROTECT, related_name="flights", verbose_name="Puerta"
    )
    aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.PROTECT,
        related_name="flights",
        verbose_name="Aeronave",
    )
    pilot = models.ForeignKey(
        Personnel,
        on_delete=models.PROTECT,
        related_name="flights_as_pilot",
        limit_choices_to={"personnel_type": "PILOT", "is_active": True},
        verbose_name="Piloto",
    )
    copilots = models.ManyToManyField(
        Personnel,
        related_name="flights_as_copilot",
        limit_choices_to={"personnel_type": "COPILOT", "is_active": True},
        verbose_name="Copilotos",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vuelo"
        verbose_name_plural = "Vuelos"
        ordering = ["-departure_time"]

    def __str__(self):
        return f"Vuelo {self.flight_number}: {self.origin} → {self.destination}"

    def get_duration(self):
        """
        Calcula la duración del vuelo en horas.

        Returns:
            float: Duración en horas
        """
        if self.departure_time and self.arrival_time:
            delta = self.arrival_time - self.departure_time
            return delta.total_seconds() / 3600
        return 0

    def get_required_copilots(self):
        """
        Calcula la minima cantidad de copilotos requeridos en base a la duración del vuelo.
        - Vuelos de hasta 4 horas: 1 copiloto
        - Vuelos de 4-8 horas: 2 copilotos
        - Vuelos de más de 8 horas: 3 copilotos

        Returns:
            int: mínima cantidad de copilotos requeridos
        """
        duration = self.get_duration()
        if duration <= 4:
            return 1
        elif duration <= 8:
            return 2
        else:
            return 3

    def clean(self):
        """
        Valida los datos proporcionados para crear el vuelo y los recursos asignados.
        Checkea los conflictos de tiempo y overlapping de recursos.
        """
        errors = {}
        duration = self.get_duration()

        # Valida las fechas de salida y llegada
        if self.departure_time and self.arrival_time:
            if self.departure_time < timezone.now():
                errors["departure_time"] = ValidationError(
                    "La fecha de salida no puede ser anterior a la fecha actual.",
                    code="invalid_departure_time",
                )

            if self.arrival_time < timezone.now():
                errors["arrival_time"] = ValidationError(
                    "La fecha de llegada no puede ser anterior a la fecha actual.",
                    code="invalid_arrival_time",
                )

            if duration > 20:
                errors["arrival_time"] = ValidationError(
                    "El vuelo no puede durar más de 20 horas.",
                    code="invalid_time_range",
                )

            if self.arrival_time <= self.departure_time:
                errors["arrival_time"] = ValidationError(
                    "La fecha de llegada debe ser posterior a la fecha de salida.",
                    code="invalid_time_range",
                )

        if self.origin.lower() == self.destination.lower():
            errors["origin"] = ValidationError(
                "El origen y el destino no pueden ser iguales.",
                code="invalid_origin_destination",
            )

        # Valida que los pilotos sean pilotos
        if self.pilot and self.pilot.personnel_type != "PILOT":
            errors["pilot"] = ValidationError(
                "El personal seleccionado debe ser un piloto.", code="invalid_pilot"
            )

        # Checkea la disponibilidad de los recursos
        exclude_id = self.pk if self.pk else None

        if self.runway and not self.runway.is_available(
            self.departure_time, self.arrival_time, exclude_id
        ):
            errors["runway"] = ValidationError(
                "La pista seleccionada no está disponible durante el tiempo seleccionado.",
                code="runway_conflict",
            )

        if self.gate and not self.gate.is_available(
            self.departure_time, self.arrival_time, exclude_id
        ):
            errors["gate"] = ValidationError(
                "La puerta seleccionada no está disponible durante el tiempo seleccionado.",
                code="gate_conflict",
            )

        if self.aircraft and not self.aircraft.is_available(
            self.departure_time, self.arrival_time, exclude_id
        ):
            errors["aircraft"] = ValidationError(
                "El avión seleccionado no está disponible (requiere un mantenimiento de 24 horas entre vuelos).",
                code="aircraft_conflict",
            )

        if self.pilot and not self.pilot.is_available(
            self.departure_time, self.arrival_time, exclude_id
        ):
            errors["pilot"] = ValidationError(
                "El piloto seleccionado no está disponible durante el tiempo seleccionado.",
                code="pilot_conflict",
            )

        if errors:
            raise ValidationError(errors)

    def validate_copilots(self):
        """
        Valida que el vuelo tenga la cantidad de copilotos requerida y valida que los copilotos estén disponibles en el rango de tiempo dado.
        """
        errors = []

        # verificar si tenemos la cantidad minima de copilotos asignados
        required = self.get_required_copilots()
        assigned = self.copilots.count()

        if assigned < required:
            errors.append(
                ValidationError(
                    f"Flight requires at least {required} co-pilot(s) based on duration of {self.get_duration():.1f} hours. Currently assigned: {assigned}.",
                    code="insufficient_copilots",
                )
            )

        # Valida cada copiloto
        exclude_id = self.pk if self.pk else None
        for copilot in self.copilots.all():
            if copilot.personnel_type != "COPILOT":
                errors.append(
                    ValidationError(
                        f"Personnel {copilot.get_full_name()} no es un co-piloto.",
                        code="invalid_copilot",
                    )
                )

            if not copilot.is_available(
                self.departure_time, self.arrival_time, exclude_id
            ):
                errors.append(
                    ValidationError(
                        f"Co-pilot {copilot.get_full_name()} no está disponible durante el tiempo seleccionado.",
                        code="copilot_conflict",
                    )
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Corre una validación completa antes salvar los datos a la base de datos."""
        self.full_clean()
        super().save(*args, **kwargs)
