import pytest
from django.utils import timezone

from airline_app.models import Aircraft, Gate, Personnel, Runway


@pytest.fixture()
def runway(db):
    return Runway.objects.create(name="Runway 1", runway_code="RW-01", length_meters=3000, is_active=True)


@pytest.fixture()
def gate(db):
    return Gate.objects.create(name="Gate 1", gate_code="G-01", terminal="T1", is_active=True)


@pytest.fixture()
def gate_2(db):
    return Gate.objects.create(name="Gate 2", gate_code="G-02", terminal="T1", is_active=True)


@pytest.fixture()
def aircraft(db):
    return Aircraft.objects.create(
        registration_number="N12345",
        model="737-800",
        manufacturer="Boeing",
        capacity=180,
        year_manufactured=2020,
        status="OPERATIONAL",
        last_maintenance_date=timezone.now(),
    )


@pytest.fixture()
def pilot(db):
    return Personnel.objects.create(
        first_name="Juan",
        last_name="Pérez",
        employee_id="PIL-001",
        personnel_type="PILOT",
        license_number="LIC-001",
        years_of_experience=10,
        is_active=True,
    )


@pytest.fixture()
def copilot(db):
    return Personnel.objects.create(
        first_name="Ana",
        last_name="Gómez",
        employee_id="COP-001",
        personnel_type="COPILOT",
        license_number="LIC-002",
        years_of_experience=6,
        is_active=True,
    )
