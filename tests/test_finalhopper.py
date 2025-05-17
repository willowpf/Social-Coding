import pytest
from unittest.mock import patch
from app.finalhopper import geocoding

@patch("app.geo_service.requests.get")
def test_geocoding_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "hits": [{
            "point": {"lat": 40.7128, "lng": -74.0060},
            "name": "New York",
            "state": "NY",
            "country": "USA"
        }]
    }

    status, lat, lng, loc = geocoding("New York", "test-key")
    assert status == 200
    assert lat == 40.7128
    assert lng == -74.0060
    assert "New York" in loc

@patch("app.geo_service.requests.get")
def test_geocoding_no_hits(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"hits": []}

    status, lat, lng, loc = geocoding("Nowhereville", "test-key")
    assert status == 200
    assert lat is None
    assert loc is None

@patch("app.geo_service.requests.get")
def test_geocoding_http_error(mock_get):
    mock_get.return_value.status_code = 500

    status, lat, lng, loc = geocoding("New York", "test-key")
    assert status == 500
    assert lat is None
    assert loc is None
