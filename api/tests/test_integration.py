import pytest
import os
from dotenv import load_dotenv
from api.meteoblue_client.client import MeteoblueClient
from api.meteoblue_client.models import ForecastPackage, ImageType

# Load .env file to get the real API key
load_dotenv()

@pytest.mark.integration
def test_full_flow_integration():
    api_key = os.getenv("METEOBLUE_API_KEY")
    if not api_key:
        pytest.skip("METEOBLUE_API_KEY not found in environment")

    client = MeteoblueClient(api_key=api_key)

    # 1. Search for a city
    print("\nSearching for 'Basel'...")
    results = client.search_location("Basel")
    assert len(results) > 0
    
    city = results[0]
    lat = city["lat"]
    lon = city["lon"]
    print(f"Found {city['name']} at {lat}, {lon}")

    # 2. Get Forecast
    print("Fetching forecast...")
    forecast = client.get_forecast(
        lat=lat,
        lon=lon,
        packages=[ForecastPackage.BASIC_DAY]
    )
    assert "data_day" in forecast
    print("Forecast fetched successfully.")

    # 3. Get Image
    print("Fetching image...")
    image_data = client.get_image(
        image_type=ImageType.METEOGRAM_14_DAY,
        lat=lat,
        lon=lon,
        output_file="/tmp/integration_test_image.png"
    )
    assert len(image_data) > 0
    assert os.path.exists("/tmp/integration_test_image.png")
    print("Image fetched and saved to /tmp/integration_test_image.png")
