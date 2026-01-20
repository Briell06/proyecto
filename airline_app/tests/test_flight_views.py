import pytest
from django.urls import reverse
from django.utils import timezone

from airline_app.models import Flight


@pytest.mark.django_db
def test_flight_create_view_creates_flight(client, runway, gate, aircraft, pilot, copilot):
    url = reverse("flight_create")
    dep = timezone.now() + timezone.timedelta(days=1)
    arr = dep + timezone.timedelta(hours=2)

    payload = {
        "flight_number": "AA200",
        "origin": "Havana",
        "destination": "Miami",
        "departure_time": dep.strftime("%Y-%m-%dT%H:%M"),
        "arrival_time": arr.strftime("%Y-%m-%dT%H:%M"),
        "status": "SCHEDULED",
        "runway": runway.id,
        "gate": gate.id,
        "aircraft": aircraft.id,
        "pilot": pilot.id,
        "copilots": [copilot.id],
    }

    resp = client.post(url, data=payload)
    assert resp.status_code in (200, 302)
    assert Flight.objects.filter(flight_number="AA200").exists()


@pytest.mark.django_db
def test_flight_update_view_does_not_500_on_validationerror(client, runway, gate, aircraft, pilot, copilot):
    dep = timezone.now() + timezone.timedelta(days=1)
    arr = dep + timezone.timedelta(hours=2)

    flight = Flight.objects.create(
        flight_number="AA201",
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
    flight.copilots.add(copilot)

    url = reverse("flight_update", kwargs={"pk": flight.pk})

    # Make it invalid: arrival_time before departure_time
    payload = {
        "flight_number": "AA201",
        "origin": "Havana",
        "destination": "Miami",
        "departure_time": dep.strftime("%Y-%m-%dT%H:%M"),
        "arrival_time": (dep - timezone.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M"),
        "status": "SCHEDULED",
        "runway": runway.id,
        "gate": gate.id,
        "aircraft": aircraft.id,
        "pilot": pilot.id,
        "copilots": [copilot.id],
    }

    resp = client.post(url, data=payload)
    # Important: should not crash with 500
    assert resp.status_code != 500
