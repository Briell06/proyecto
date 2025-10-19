from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),
    # Runway URLs
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
    # Gate URLs
    path("puertas/", views.GateListView.as_view(), name="gate_list"),
    path("puertas/crear/", views.GateCreateView.as_view(), name="gate_create"),
    path("puertas/<int:pk>/", views.GateDetailView.as_view(), name="gate_detail"),
    path(
        "puertas/<int:pk>/editar/", views.GateUpdateView.as_view(), name="gate_update"
    ),
    path(
        "puertas/<int:pk>/eliminar/", views.GateDeleteView.as_view(), name="gate_delete"
    ),
    # Personnel URLs
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
    # Aircraft URLs
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
    # Flight URLs
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
    # Utility URLs
    path("disponibilidad/", views.check_availability, name="check_availability"),
]
