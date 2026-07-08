import os
import json
import pytest
from project import calculate_safety_flag, get_species_advice, trigger_sos, read_shore_alerts


def test_calculate_safety_flag():
    # Test safe profile conditions
    assert calculate_safety_flag(3.0, 0.8, 10.0) == "🟢 SAFE"
    # Test winds threshold crossing limits
    assert calculate_safety_flag(6.0, 0.5, 9.0) == "⚠️ CAUTION"
    # Test wave height limits crossing threshold
    assert calculate_safety_flag(2.0, 1.4, 8.0) == "⚠️ CAUTION"
    # Test critical dangers triggered directly
    assert calculate_safety_flag(8.5, 0.5, 10.0) == "🔴 DANGER"
    assert calculate_safety_flag(2.0, 2.2, 10.0) == "🔴 DANGER"
    assert calculate_safety_flag(2.0, 0.5, 2.0) == "🔴 DANGER"


def test_get_species_advice():
    assert "Sardinella aurita" in get_species_advice("sardinella")
    assert "Engraulis encrasicolus" in get_species_advice("  Anchovy ")
    assert "❌" in get_species_advice("Tilapia")


def test_trigger_sos_and_repository():
    # Clean file state before testing tracking pipelines
    if os.path.exists("sos_repository.json"):
        os.remove("sos_repository.json")

    # Fire valid tracking transaction parameters
    msg = trigger_sos("TEST_CRAFT_77", 6.1245, 1.2294)
    assert "TEST_CRAFT_77" in msg
    assert "https://www.google.com/maps?q=6.1245,1.2294" in msg

    # Validate file input output reading structures work seamlessly
    alerts = read_shore_alerts()
    assert len(alerts) == 1
    assert alerts[0]["fisher_id"] == "TEST_CRAFT_77"

    # Test coordinate boundaries value exception catching
    with pytest.raises(ValueError):
        trigger_sos("BAD_GPS", 150.0, 2.0)


def teardown_module(module):
    """Cleanup temporary test lifecycle repository footprints automatically."""
    if os.path.exists("sos_repository.json"):
        os.remove("sos_repository.json")