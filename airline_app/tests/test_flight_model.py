import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from airline_app.models import Flight, ResourceConstraint


@pytest.mark.django_db
def test_flight_clean_does_not_query_with_none_times(runway, gate, aircraft, pilot):
    # Should not crash with "Cannot use None as a query value".
    flight = Flight(
        flight_number="AA100",
        origin="Havana",
        destination="Miami",
        departure_time=None,
        arrival_time=None,
        status="SCHEDULED",
        runway=runway,
        gate=gate,
        aircraft=aircraft,
        pilot=pilot,
    )

    # clean() should be safe even if times are missing
    flight.clean()


@pytest.mark.django_db
def test_resource_constraint_personnel_mapping_only_triggers_when_violated(
    runway, gate, gate_2, aircraft, pilot, copilot
):
    # Constraint: If pilot (personnel) is used, then gate must be gate_2
    constraint = ResourceConstraint.objects.create(
        name="Pilot requires Gate 2",
        constraint_type="CO_REQUISITE",
        description="",
        primary_resource_type="personnel",
        primary_resource_id=pilot.id,
        related_resource_type="gate",
        related_resource_id=gate_2.id,
        is_active=True,
    )

    dep = timezone.now() + timezone.timedelta(days=1)
    arr = dep + timezone.timedelta(hours=2)

    # Violating flight (uses gate instead of gate_2)
    violating = Flight(
        flight_number="AA101",
        origin="Havana",
        destination="Miami",
        departure_time=dep,
        arrival_time=arr,
        status="SCHEDULED",
        runway=runway,
        gate=gate,
        aircraft=aircraft,
        pilot=pilot,
    )

    with pytest.raises(ValidationError):
        violating.full_clean()

    # Compliant flight
    ok = Flight(
        flight_number="AA102",
        origin="Havana",
        destination="Miami",
        departure_time=dep,
        arrival_time=arr,
        status="SCHEDULED",
        runway=runway,
        gate=gate_2,
        aircraft=aircraft,
        pilot=pilot,
    )

    ok.full_clean()

    # Silence linter about unused
    assert constraint.is_active
