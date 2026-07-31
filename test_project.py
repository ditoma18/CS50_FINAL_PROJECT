import os
import pytest

from project import (
    calculate_safety_flag,
    get_species_advice,
    trigger_sos,
    read_shore_alerts,
    simulate_gps
)


def test_calculate_safety_flag():
    # Test safe conditions
    assert calculate_safety_flag(3.0, 0.8, 10.0) == "🟢 SAFE"

    # Test caution conditions
    assert calculate_safety_flag(6.0, 0.8, 10.0) == "⚠️ CAUTION"
    assert calculate_safety_flag(3.0, 1.5, 8.0) == "⚠️ CAUTION"

    # Test dangerous conditions
    assert calculate_safety_flag(8.0, 0.5, 10.0) == "🔴 DANGER"
    assert calculate_safety_flag(3.0, 2.0, 10.0) == "🔴 DANGER"
    assert calculate_safety_flag(3.0, 0.5, 2.0) == "🔴 DANGER"



def test_get_species_advice():
    # Test known fish species information
    result = get_species_advice("sardinella")

    assert "Sardinella aurita" in result
    assert "12 cm" in result
    assert "Overfished Threat" in result

    result = get_species_advice("Anchovy")

    assert "Engraulis encrasicolus" in result
    assert "10 cm" in result



def test_trigger_sos():
    # Remove old SOS file before testing
    if os.path.exists("sos_repository.json"):
        os.remove("sos_repository.json")

    message = trigger_sos(
        "TEST_FISHER",
        6.1245,
        1.2294
    )

    assert "TRANSMITTED" in message
    assert "6.1245,1.2294" in message

    alerts = read_shore_alerts()

    assert len(alerts) == 1
    assert alerts[0]["fisher_id"] == "TEST_FISHER"



def test_invalid_coordinates():
    # Test invalid latitude
    with pytest.raises(ValueError):
        trigger_sos("TEST", 100, 1.2)

    # Test invalid longitude
    with pytest.raises(ValueError):
        trigger_sos("TEST", 6.1, 200)



def test_read_shore_alerts_empty():
    # If no SOS file exists, function should return an empty list
    if os.path.exists("sos_repository.json"):
        os.remove("sos_repository.json")

    assert read_shore_alerts() == []



def test_simulate_gps():
    latitude, longitude = simulate_gps()

    # I Check that generated coordinates stay around Lomé port
    assert 6.08 <= latitude <= 6.16
    assert 1.18 <= longitude <= 1.26



def cleanup(module):
    # Delete files created during tests
    if os.path.exists("sos_repository.json"):
        os.remove("sos_repository.json")

    if os.path.exists("User_contribution.json"):
        os.remove("User_contribution.json")