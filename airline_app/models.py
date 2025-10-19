from typing import Any
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class Runway(models.Model):
    """
    Represents a runway for aircraft takeoff and landing operations.
    Each runway can only be used by one flight at a time.
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
        Check if runway is available for the given time interval.

        Args:
            start_time: Flight start datetime
            end_time: Flight end datetime
            exclude_flight_id: Optional flight ID to exclude from check (for updates)

        Returns:
            bool: True if available, False otherwise
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
    Represents a boarding gate where passengers board the aircraft.
    Each gate can only be assigned to one flight at a time.
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
        Check if gate is available for the given time interval.

        Args:
            start_time: Flight start datetime
            end_time: Flight end datetime
            exclude_flight_id: Optional flight ID to exclude from check (for updates)

        Returns:
            bool: True if available, False otherwise
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
    Represents airline personnel (pilots and co-pilots).
    Each person can only be assigned to one flight at a time.
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
        """Returns the person's full name."""
        return f"{self.first_name} {self.last_name}"

    def is_available(self, start_time, end_time, exclude_flight_id=None):
        """
        Check if personnel is available for the given time interval.

        Args:
            start_time: Flight start datetime
            end_time: Flight end datetime
            exclude_flight_id: Optional flight ID to exclude from check (for updates)

        Returns:
            bool: True if available, False otherwise
        """
        from django.db.models import Q

        # Check flights where this person is assigned as pilot
        pilot_flights = Flight.objects.filter(
            pilot=self, status__in=["SCHEDULED", "IN_PROGRESS"]
        ).filter(Q(departure_time__lt=end_time) & Q(arrival_time__gt=start_time))

        # Check flights where this person is assigned as co-pilot
        copilot_flights = Flight.objects.filter(
            copilots=self, status__in=["SCHEDULED", "IN_PROGRESS"]
        ).filter(Q(departure_time__lt=end_time) & Q(arrival_time__gt=start_time))

        if exclude_flight_id:
            pilot_flights = pilot_flights.exclude(id=exclude_flight_id)
            copilot_flights = copilot_flights.exclude(id=exclude_flight_id)

        return not (pilot_flights.exists() or copilot_flights.exists())


class Aircraft(models.Model):
    """
    Represents an aircraft in the fleet.
    Aircraft require 24 hours between flights for mandatory maintenance.
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
        Check if aircraft is available for the given time interval.
        Aircraft needs 24 hours between flights for maintenance.

        Args:
            start_time: Flight start datetime
            end_time: Flight end datetime
            exclude_flight_id: Optional flight ID to exclude from check (for updates)

        Returns:
            bool: True if available, False otherwise
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
    Represents a flight event that consumes multiple resources.
    Each flight must have one of each resource type and proper crew assignment.
    Validates time conflicts and resource availability constraints.
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

    # Resource assignments (one of each type required)
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
        Calculate flight duration in hours.

        Returns:
            float: Duration in hours
        """
        if self.departure_time and self.arrival_time:
            delta = self.arrival_time - self.departure_time
            return delta.total_seconds() / 3600
        return 0

    def get_required_copilots(self):
        """
        Calculate the minimum number of co-pilots required based on flight duration.
        - Flights up to 4 hours: 1 co-pilot
        - Flights 4-8 hours: 2 co-pilots
        - Flights over 8 hours: 3 co-pilots

        Returns:
            int: Minimum number of co-pilots required
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
        Validate flight data and resource assignments.
        Checks for time conflicts and constraint violations.
        """
        errors = {}
        duration = self.get_duration()

        # Validate times
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

        if self.origin == self.destination:
            errors["origin"] = ValidationError(
                "El origen y el destino no pueden ser iguales.",
                code="invalid_origin_destination",
            )

        # Validate pilot is actually a pilot
        if self.pilot and self.pilot.personnel_type != "PILOT":
            errors["pilot"] = ValidationError(
                "El personal seleccionado debe ser un piloto.", code="invalid_pilot"
            )

        # Check resource availability
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
        Validate that the flight has the required number of co-pilots
        and that all co-pilots are available.
        Must be called after the flight is saved and copilots are assigned.
        """
        errors = []

        # Check if we have the minimum required co-pilots
        required = self.get_required_copilots()
        assigned = self.copilots.count()

        if assigned < required:
            errors.append(
                ValidationError(
                    f"Flight requires at least {required} co-pilot(s) based on duration of {self.get_duration():.1f} hours. Currently assigned: {assigned}.",
                    code="insufficient_copilots",
                )
            )

        # Validate each co-pilot
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
        """Override save to run validation before saving."""
        self.full_clean()
        super().save(*args, **kwargs)


class ResourceConstraint(models.Model):
    """
    Defines co-requisite and mutual exclusion constraints between resources.
    These rules ensure proper resource combinations in flights.
    """

    CONSTRAINT_TYPES = [
        ("CO_REQUISITE", "Co-requisito"),
        ("MUTUAL_EXCLUSION", "Exclusión Mutua"),
    ]

    name = models.CharField(max_length=200, verbose_name="Nombre")
    constraint_type = models.CharField(
        max_length=20, choices=CONSTRAINT_TYPES, verbose_name="Tipo de Restricción"
    )
    description = models.TextField(verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Restricción de Recursos"
        verbose_name_plural = "Restricciones de Recursos"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_constraint_type_display()})"
