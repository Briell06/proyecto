from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),
    # URLs para pistas
    path("pistas/", views.RunwayListView.as_view(), name="runway_list"),
    path("pistas/crear/", views.RunwayCreateView.as_view(), name="runway_create"),
    path("pistas/<int:pk>/", views.RunwayDetailView.as_view(), name="runway_detail"),
    path(
        "pistas/<int:pk>/editar/",
        views.RunwayUpdateView.as_view(),
        name="runway_update",
    ),
    path(
        "pistas/<int:pk>/eliminar/",
        views.RunwayDeleteView.as_view(),
        name="runway_delete",
    ),
    # URLs para puertas de embargue
    path("puertas/", views.GateListView.as_view(), name="gate_list"),
    path("puertas/crear/", views.GateCreateView.as_view(), name="gate_create"),
    path("puertas/<int:pk>/", views.GateDetailView.as_view(), name="gate_detail"),
    path(
        "puertas/<int:pk>/editar/", views.GateUpdateView.as_view(), name="gate_update"
    ),
    path(
        "puertas/<int:pk>/eliminar/", views.GateDeleteView.as_view(), name="gate_delete"
    ),
    # URLs para el personal
    path("personal/", views.PersonnelListView.as_view(), name="personnel_list"),
    path(
        "personal/crear/", views.PersonnelCreateView.as_view(), name="personnel_create"
    ),
    path(
        "personal/<int:pk>/",
        views.PersonnelDetailView.as_view(),
        name="personnel_detail",
    ),
    path(
        "personal/<int:pk>/editar/",
        views.PersonnelUpdateView.as_view(),
        name="personnel_update",
    ),
    path(
        "personal/<int:pk>/eliminar/",
        views.PersonnelDeleteView.as_view(),
        name="personnel_delete",
    ),
    # URLs para los aviones
    path("aeronaves/", views.AircraftListView.as_view(), name="aircraft_list"),
    path(
        "aeronaves/crear/", views.AircraftCreateView.as_view(), name="aircraft_create"
    ),
    path(
        "aeronaves/<int:pk>/",
        views.AircraftDetailView.as_view(),
        name="aircraft_detail",
    ),
    path(
        "aeronaves/<int:pk>/editar/",
        views.AircraftUpdateView.as_view(),
        name="aircraft_update",
    ),
    path(
        "aeronaves/<int:pk>/eliminar/",
        views.AircraftDeleteView.as_view(),
        name="aircraft_delete",
    ),
    # URLs para los vuelos
    path("vuelos/", views.FlightListView.as_view(), name="flight_list"),
    path("vuelos/crear/", views.FlightCreateView.as_view(), name="flight_create"),
    path("vuelos/<int:pk>/", views.FlightDetailView.as_view(), name="flight_detail"),
    path(
        "vuelos/<int:pk>/editar/",
        views.FlightUpdateView.as_view(),
        name="flight_update",
    ),
    path(
        "vuelos/<int:pk>/eliminar/",
        views.FlightDeleteView.as_view(),
        name="flight_delete",
    ),
    # URLs de utilidad
    path("disponibilidad/", views.check_availability, name="check_availability"),
    path("buscar-horario/", views.find_slot, name="find_slot"),
    # URLs para restricciones de recursos
    path(
        "restricciones/", views.ConstraintListView.as_view(), name="constraint_list"
    ),
    path(
        "restricciones/crear/",
        views.ConstraintCreateView.as_view(),
        name="constraint_create",
    ),
    path(
        "restricciones/<int:pk>/",
        views.ConstraintDetailView.as_view(),
        name="constraint_detail",
    ),
    path(
        "restricciones/<int:pk>/editar/",
        views.ConstraintUpdateView.as_view(),
        name="constraint_update",
    ),
    path(
        "restricciones/<int:pk>/eliminar/",
        views.ConstraintDeleteView.as_view(),
        name="constraint_delete",
    ),
]
