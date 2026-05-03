"""
Unit tests for the Google Workspace integration module.
"""

import pytest
from google_workspace import add_election_reminder_to_calendar, find_polling_location_via_maps

def test_add_election_reminder_to_calendar():
    """Test that the calendar tool correctly returns a success message."""
    result = add_election_reminder_to_calendar("Oct 21, 2026", "City Hall")
    assert "Successfully added" in result
    assert "Oct 21, 2026" in result
    assert "City Hall" in result

def test_find_polling_location_via_maps():
    """Test that the maps tool correctly returns a simulated location."""
    result = find_polling_location_via_maps("456 Elm St")
    assert "City Hall" in result
    assert "1.2 miles" in result
    assert "456 Elm St" in result
