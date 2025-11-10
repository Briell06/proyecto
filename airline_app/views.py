from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    AircraftForm,
    FlightForm,
    FlightSearchForm,
    GateForm,
    PersonnelForm,
    ResourceAvailabilityForm,
    RunwayForm,
)
from .models import Aircraft, Flight, Gate, Personnel, Runway


def home(request):
    """View que conecta al dashboard."""
    context = {
        "total_runways": Runway.objects.filter(is_active=True).count(),
        "total_gates": Gate.objects.filter(is_active=True).count(),
        "total_aircraft": Aircraft.objects.filter(status="OPERATIONAL").count(),
        "total_personnel": Personnel.objects.filter(is_active=True).count(),
        "total_flights": Flight.objects.count(),
        "upcoming_flights": Flight.objects.filter(
            status="SCHEDULED", departure_time__gte=datetime.now()
        ).order_by("departure_time")[:5],
    }
    return render(request, "airline_app/home.html", context)


# Vistas pata trabajar con pistas
class RunwayListView(ListView):
    """Listar pistas."""

    model = Runway
    template_name = "airline_app/runway_list.html"
    context_object_name = "runways"
    paginate_by = 10
    ordering = ["runway_code"]


class RunwayCreateView(CreateView):
    """Crear pista."""

    model = Runway
    form_class = RunwayForm
    template_name = "airline_app/runway_form.html"
    success_url = reverse_lazy("runway_list")

    def form_valid(self, form):
        messages.success(self.request, "Pista creada exitosamente.")
        return super().form_valid(form)


class RunwayUpdateView(UpdateView):
    """Actualizar una pista."""

    model = Runway
    form_class = RunwayForm
    template_name = "airline_app/runway_form.html"
    success_url = reverse_lazy("runway_list")

    def form_valid(self, form):
        messages.success(self.request, "Pista actualizada exitosamente.")
        return super().form_valid(form)


class RunwayDeleteView(DeleteView):
    """Borrar una pistas."""

    model = Runway
    template_name = "airline_app/runway_confirm_delete.html"
    success_url = reverse_lazy("runway_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Pista eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)


class RunwayDetailView(DetailView):
    """Detallar una pista."""

    model = Runway
    template_name = "airline_app/runway_detail.html"
    context_object_name = "runway"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flights"] = self.object.flights.filter(
            status__in=["SCHEDULED", "IN_PROGRESS"]
        ).order_by("departure_time")
        return context


# Vistas de puertas de embargue
class GateListView(ListView):
    """Listar todas las puertas de embargue."""

    model = Gate
    template_name = "airline_app/gate_list.html"
    context_object_name = "gates"
    paginate_by = 10
    ordering = ["gate_code"]


class GateCreateView(CreateView):
    """Crear puertas de embargue."""

    model = Gate
    form_class = GateForm
    template_name = "airline_app/gate_form.html"
    success_url = reverse_lazy("gate_list")

    def form_valid(self, form):
        messages.success(self.request, "Puerta de embarque creada exitosamente.")
        return super().form_valid(form)


class GateUpdateView(UpdateView):
    """Actualizar una puerta de embargue."""

    model = Gate
    form_class = GateForm
    template_name = "airline_app/gate_form.html"
    success_url = reverse_lazy("gate_list")

    def form_valid(self, form):
        messages.success(self.request, "Puerta de embarque actualizada exitosamente.")
        return super().form_valid(form)


class GateDeleteView(DeleteView):
    """Borrar una puerta de embargue."""

    model = Gate
    template_name = "airline_app/gate_confirm_delete.html"
    success_url = reverse_lazy("gate_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Puerta de embarque eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)


class GateDetailView(DetailView):
    """Detallar una puerta de embargue."""

    model = Gate
    template_name = "airline_app/gate_detail.html"
    context_object_name = "gate"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flights"] = self.object.flights.filter(
            status__in=["SCHEDULED", "IN_PROGRESS"]
        ).order_by("departure_time")
        return context


# Vistas de personal
class PersonnelListView(ListView):
    """Listar el personal."""

    model = Personnel
    template_name = "airline_app/personnel_list.html"
    context_object_name = "personnel_list"
    paginate_by = 10
    ordering = ["last_name", "first_name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        personnel_type = self.request.GET.get("type")
        if personnel_type in ["PILOT", "COPILOT"]:
            queryset = queryset.filter(personnel_type=personnel_type)
        return queryset


class PersonnelCreateView(CreateView):
    """Crear un miembro del personal."""

    model = Personnel
    form_class = PersonnelForm
    template_name = "airline_app/personnel_form.html"
    success_url = reverse_lazy("personnel_list")

    def form_valid(self, form):
        messages.success(self.request, "Personal creado exitosamente.")
        return super().form_valid(form)


class PersonnelUpdateView(UpdateView):
    """Actualizar miembro del personal."""

    model = Personnel
    form_class = PersonnelForm
    template_name = "airline_app/personnel_form.html"
    success_url = reverse_lazy("personnel_list")

    def form_valid(self, form):
        messages.success(self.request, "Personal actualizado exitosamente.")
        return super().form_valid(form)


class PersonnelDeleteView(DeleteView):
    """Eliminar un miembro del personal."""

    model = Personnel
    template_name = "airline_app/personnel_confirm_delete.html"
    success_url = reverse_lazy("personnel_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Personal eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)


class PersonnelDetailView(DetailView):
    """Mostrar los detalles de un miembro del personal."""

    model = Personnel
    template_name = "airline_app/personnel_detail.html"
    context_object_name = "personnel"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.personnel_type == "PILOT":
            context["flights"] = self.object.flights_as_pilot.filter(
                status__in=["SCHEDULED", "IN_PROGRESS"]
            ).order_by("departure_time")
        else:
            context["flights"] = self.object.flights_as_copilot.filter(
                status__in=["SCHEDULED", "IN_PROGRESS"]
            ).order_by("departure_time")
        return context


# Vistas de aviones
class AircraftListView(ListView):
    """Mostrar la lista de aviones."""

    model = Aircraft
    template_name = "airline_app/aircraft_list.html"
    context_object_name = "aircraft_list"
    paginate_by = 10
    ordering = ["registration_number"]

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status")
        if status in ["OPERATIONAL", "MAINTENANCE", "OUT_OF_SERVICE"]:
            queryset = queryset.filter(status=status)
        return queryset


class AircraftCreateView(CreateView):
    """Crear un nuevo avión."""

    model = Aircraft
    form_class = AircraftForm
    template_name = "airline_app/aircraft_form.html"
    success_url = reverse_lazy("aircraft_list")

    def form_valid(self, form):
        messages.success(self.request, "Aeronave creada exitosamente.")
        return super().form_valid(form)


class AircraftUpdateView(UpdateView):
    """Actualizar un nuevo avión."""

    model = Aircraft
    form_class = AircraftForm
    template_name = "airline_app/aircraft_form.html"
    success_url = reverse_lazy("aircraft_list")

    def form_valid(self, form):
        messages.success(self.request, "Aeronave actualizada exitosamente.")
        return super().form_valid(form)


class AircraftDeleteView(DeleteView):
    """Borrar un avión."""

    model = Aircraft
    template_name = "airline_app/aircraft_confirm_delete.html"
    success_url = reverse_lazy("aircraft_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Aeronave eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)


class AircraftDetailView(DetailView):
    """Detallar un avión."""

    model = Aircraft
    template_name = "airline_app/aircraft_detail.html"
    context_object_name = "aircraft"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flights"] = self.object.flights.filter(
            status__in=["SCHEDULED", "IN_PROGRESS"]
        ).order_by("departure_time")
        return context


# Vistas de Vuelos
class FlightListView(ListView):
    """Mostrar la lista de vuelos."""

    model = Flight
    template_name = "airline_app/flight_list.html"
    context_object_name = "flights"
    paginate_by = 10
    ordering = ["-departure_time"]

    def get_queryset(self):
        queryset = super().get_queryset()
        form = FlightSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data.get("flight_number"):
                queryset = queryset.filter(
                    flight_number__icontains=form.cleaned_data["flight_number"]
                )
            if form.cleaned_data.get("origin"):
                queryset = queryset.filter(
                    origin__icontains=form.cleaned_data["origin"]
                )
            if form.cleaned_data.get("destination"):
                queryset = queryset.filter(
                    destination__icontains=form.cleaned_data["destination"]
                )
            if form.cleaned_data.get("status"):
                queryset = queryset.filter(status=form.cleaned_data["status"])
            if form.cleaned_data.get("date_from"):
                queryset = queryset.filter(
                    departure_time__gte=form.cleaned_data["date_from"]
                )
            if form.cleaned_data.get("date_to"):
                queryset = queryset.filter(
                    departure_time__lte=form.cleaned_data["date_to"]
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = FlightSearchForm(self.request.GET)
        return context


class FlightCreateView(CreateView):
    """Crear un vuelo."""

    model = Flight
    form_class = FlightForm
    template_name = "airline_app/flight_form.html"
    success_url = reverse_lazy("flight_list")

    def form_valid(self, form):
        try:
            self.object = form.save()
            # Validación de copilotos
            self.object.validate_copilots()
            messages.success(self.request, "Vuelo creado exitosamente.")
            return redirect(self.success_url)
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(self.request, error)
            return self.form_invalid(form)


class FlightUpdateView(UpdateView):
    """Actualizar un vuelo."""

    model = Flight
    form_class = FlightForm
    template_name = "airline_app/flight_form.html"
    success_url = reverse_lazy("flight_list")

    def form_valid(self, form):
        try:
            self.object = form.save()
            # Valida los copilotos
            self.object.validate_copilots()
            messages.success(self.request, "Vuelo actualizado exitosamente.")
            return redirect(self.success_url)
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(self.request, error)
            return self.form_invalid(form)


class FlightDeleteView(DeleteView):
    """Borrar un vuelo."""

    model = Flight
    template_name = "airline_app/flight_confirm_delete.html"
    success_url = reverse_lazy("flight_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Vuelo eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)


class FlightDetailView(DetailView):
    """Detallar un vuelo."""

    model = Flight
    template_name = "airline_app/flight_detail.html"
    context_object_name = "flight"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["duration"] = self.object.get_duration()
        context["required_copilots"] = self.object.get_required_copilots()
        context["assigned_copilots"] = self.object.copilots.count()
        return context


def check_availability(request):
    """Checkea la disponibilidad de los recursos en el tiempo dado."""
    if request.method == "POST":
        form = ResourceAvailabilityForm(request.POST)
        if form.is_valid():
            resource_type = form.cleaned_data["resource_type"]
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]

            available_resources = []

            if resource_type == "runway":
                resources = Runway.objects.filter(is_active=True)
                for resource in resources:
                    if resource.is_available(start_time, end_time):
                        available_resources.append(resource)

            elif resource_type == "gate":
                resources = Gate.objects.filter(is_active=True)
                for resource in resources:
                    if resource.is_available(start_time, end_time):
                        available_resources.append(resource)

            elif resource_type == "aircraft":
                resources = Aircraft.objects.filter(status="OPERATIONAL")
                for resource in resources:
                    if resource.is_available(start_time, end_time):
                        available_resources.append(resource)

            elif resource_type == "personnel":
                resources = Personnel.objects.filter(is_active=True)
                for resource in resources:
                    if resource.is_available(start_time, end_time):
                        available_resources.append(resource)

            context = {
                "form": form,
                "available_resources": available_resources,
                "resource_type": resource_type,
                "start_time": start_time,
                "end_time": end_time,
            }
            return render(request, "airline_app/check_availability.html", context)
    else:
        form = ResourceAvailabilityForm()

    return render(request, "airline_app/check_availability.html", {"form": form})
