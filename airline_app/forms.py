from django import forms
from django.core.exceptions import ValidationError
from .models import Runway, Gate, Personnel, Aircraft, Flight


class RunwayForm(forms.ModelForm):
    """Form for creating and editing runways."""

    class Meta:
        model = Runway
        fields = ["name", "runway_code", "length_meters", "is_active"]
        labels = {
            "name": "Nombre",
            "runway_code": "Código de Pista",
            "length_meters": "Longitud (metros)",
            "is_active": "Activa",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Pista Principal"}
            ),
            "runway_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: RWY-01"}
            ),
            "length_meters": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Ej: 3500"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class GateForm(forms.ModelForm):
    """Form for creating and editing gates."""

    class Meta:
        model = Gate
        fields = ["name", "gate_code", "terminal", "is_active"]
        labels = {
            "name": "Nombre",
            "gate_code": "Código de Puerta",
            "terminal": "Terminal",
            "is_active": "Activa",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Puerta A1"}
            ),
            "gate_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: A1"}
            ),
            "terminal": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Terminal A"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class PersonnelForm(forms.ModelForm):
    """Form for creating and editing personnel."""

    class Meta:
        model = Personnel
        fields = [
            "first_name",
            "last_name",
            "employee_id",
            "personnel_type",
            "license_number",
            "years_of_experience",
            "is_active",
        ]
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
            "employee_id": "ID de Empleado",
            "personnel_type": "Tipo de Personal",
            "license_number": "Número de Licencia",
            "years_of_experience": "Años de Experiencia",
            "is_active": "Activo",
        }
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Juan"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Pérez"}
            ),
            "employee_id": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: PIL-001"}
            ),
            "personnel_type": forms.Select(attrs={"class": "p-3"}),
            "license_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: ATP-12345"}
            ),
            "years_of_experience": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Ej: 10"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class AircraftForm(forms.ModelForm):
    """Form for creating and editing aircraft."""

    class Meta:
        model = Aircraft
        fields = [
            "registration_number",
            "model",
            "manufacturer",
            "capacity",
            "year_manufactured",
            "status",
            "last_maintenance_date",
        ]
        labels = {
            "registration_number": "Número de Registro",
            "model": "Modelo",
            "manufacturer": "Fabricante",
            "capacity": "Capacidad de Pasajeros",
            "year_manufactured": "Año de Fabricación",
            "status": "Estado",
            "last_maintenance_date": "Última Fecha de Mantenimiento",
        }
        widgets = {
            "registration_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: N12345"}
            ),
            "model": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: 737-800"}
            ),
            "manufacturer": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Boeing"}
            ),
            "capacity": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Ej: 189"}
            ),
            "year_manufactured": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Ej: 2020"}
            ),
            "status": forms.Select(attrs={"class": "p-3.5"}),
            "last_maintenance_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.last_maintenance_date:
            self.initial["last_maintenance_date"] = (
                self.instance.last_maintenance_date.strftime("%Y-%m-%dT%H:%M")
            )


class FlightForm(forms.ModelForm):
    """Form for creating and editing flights with comprehensive validation."""

    class Meta:
        model = Flight
        fields = [
            "flight_number",
            "origin",
            "destination",
            "departure_time",
            "arrival_time",
            "status",
            "runway",
            "gate",
            "aircraft",
            "pilot",
            "copilots",
        ]
        labels = {
            "flight_number": "Número de Vuelo",
            "origin": "Origen",
            "destination": "Destino",
            "departure_time": "Hora de Salida",
            "arrival_time": "Hora de Llegada",
            "status": "Estado",
            "runway": "Pista",
            "gate": "Puerta de Embarque",
            "aircraft": "Aeronave",
            "pilot": "Piloto",
            "copilots": "Copilotos",
        }
        widgets = {
            "flight_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: AA123"}
            ),
            "origin": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: New York"}
            ),
            "destination": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Miami"}
            ),
            "departure_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "arrival_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "status": forms.Select(attrs={"class": "p-3.5"}),
            "runway": forms.Select(attrs={"class": "p-3.5"}),
            "gate": forms.Select(attrs={"class": "p-3.5"}),
            "aircraft": forms.Select(attrs={"class": "p-3.5"}),
            "pilot": forms.Select(attrs={"class": "p-3.5"}),
            "copilots": forms.CheckboxSelectMultiple(
                attrs={"class": "p-3.5", "size": "5"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter querysets for active resources only
        self.fields["runway"].queryset = Runway.objects.filter(is_active=True)
        self.fields["gate"].queryset = Gate.objects.filter(is_active=True)
        self.fields["aircraft"].queryset = Aircraft.objects.filter(status="OPERATIONAL")
        self.fields["pilot"].queryset = Personnel.objects.filter(
            personnel_type="PILOT", is_active=True
        )
        self.fields["copilots"].queryset = Personnel.objects.filter(
            personnel_type="COPILOT", is_active=True
        )

        # Format datetime fields for editing
        if self.instance.pk:
            if self.instance.departure_time:
                self.initial["departure_time"] = self.instance.departure_time.strftime(
                    "%Y-%m-%dT%H:%M"
                )
            if self.instance.arrival_time:
                self.initial["arrival_time"] = self.instance.arrival_time.strftime(
                    "%Y-%m-%dT%H:%M"
                )

    def clean(self):
        """Validate form data including copilots."""
        cleaned_data = super().clean()

        departure_time = cleaned_data.get("departure_time")
        arrival_time = cleaned_data.get("arrival_time")
        copilots = cleaned_data.get("copilots")

        # Basic time validation
        if departure_time and arrival_time:
            if arrival_time <= departure_time:
                raise ValidationError(
                    {
                        "arrival_time": "La hora de llegada debe ser posterior a la hora de salida."
                    }
                )

            # Calculate required copilots
            duration = (arrival_time - departure_time).total_seconds() / 3600
            if duration <= 4:
                required_copilots = 1
            elif duration <= 8:
                required_copilots = 2
            else:
                required_copilots = 3

            # Validate copilot count
            if copilots and len(copilots) < required_copilots:
                raise ValidationError(
                    {
                        "copilots": f"Este vuelo requiere al menos {required_copilots} copiloto(s) "
                        f"debido a su duración de {duration:.1f} horas. "
                        f"Actualmente tiene {len(copilots)} copiloto(s) seleccionado(s)."
                    }
                )

        return cleaned_data


class FlightSearchForm(forms.Form):
    """Form for searching and filtering flights."""

    flight_number = forms.CharField(
        required=False,
        label="Número de Vuelo",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: AA123"}
        ),
    )

    origin = forms.CharField(
        required=False,
        label="Origen",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: New York"}
        ),
    )

    destination = forms.CharField(
        required=False,
        label="Destino",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: Miami"}
        ),
    )

    status = forms.ChoiceField(
        required=False,
        label="Estado",
        choices=[("", "Todos")] + Flight.FLIGHT_STATUS,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    date_from = forms.DateField(
        required=False,
        label="Desde",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    date_to = forms.DateField(
        required=False,
        label="Hasta",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )


class ResourceAvailabilityForm(forms.Form):
    """Form for checking resource availability."""

    resource_type = forms.ChoiceField(
        label="Tipo de Recurso",
        choices=[
            ("runway", "Pista"),
            ("gate", "Puerta de Embarque"),
            ("aircraft", "Aeronave"),
            ("personnel", "Personal"),
        ],
        widget=forms.Select(attrs={"class": "form-control p-3.5"}),
    )

    start_time = forms.DateTimeField(
        label="Hora de Inicio",
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    end_time = forms.DateTimeField(
        label="Hora de Fin",
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    def clean(self):
        """Validate time range."""
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and end_time <= start_time:
            raise ValidationError(
                "La hora de fin debe ser posterior a la hora de inicio."
            )

        return cleaned_data
