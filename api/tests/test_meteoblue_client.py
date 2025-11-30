import pytest
from unittest.mock import Mock, patch
from api.meteoblue_client.client import MeteoblueClient
from api.meteoblue_client.models import ForecastPackage, ImageType, OutputFormat

@pytest.fixture
def client():
    return MeteoblueClient(api_key="TEST_KEY")

def test_init(client):
    assert client.api_key == "TEST_KEY"

@patch("requests.get")
def test_get_forecast(mock_get, client):
    mock_response = Mock()
    mock_response.json.return_value = {"data_1h": {}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = client.get_forecast(
        lat=47.56,
        lon=7.57,
        packages=[ForecastPackage.BASIC_1H, ForecastPackage.BASIC_DAY]
    )

    assert result == {"data_1h": {}}
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert args[0] == "https://my.meteoblue.com/packages/basic-1h_basic-day"
    assert kwargs["params"]["lat"] == 47.56
    assert kwargs["params"]["lon"] == 7.57
    assert kwargs["params"]["apikey"] == "TEST_KEY"
    assert kwargs["params"]["format"] == "json"

@patch("requests.get")
def test_get_image(mock_get, client):
    mock_response = Mock()
    mock_response.content = b"fake_image_data"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = client.get_image(
        image_type=ImageType.METEOGRAM_CLIMATE,
        lat=47.56,
        lon=7.57
    )

    assert result == b"fake_image_data"
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert args[0] == "https://my.meteoblue.com/visimage/meteogram_climate"
    assert kwargs["params"]["lat"] == 47.56
    assert kwargs["params"]["lon"] == 7.57
    assert kwargs["params"]["apikey"] == "TEST_KEY"

@patch("requests.get")
def test_search_location(mock_get, client):
    mock_response = Mock()
    mock_response.json.return_value = {"results": [{"name": "Basel"}]}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = client.search_location(query="Basel")

    assert result == [{"name": "Basel"}]
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert args[0] == "https://www.meteoblue.com/en/server/search/query3"
    assert kwargs["params"]["query"] == "Basel"
    assert kwargs["params"]["apikey"] == "TEST_KEY"
