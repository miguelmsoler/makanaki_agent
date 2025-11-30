import requests
from typing import List, Optional, Union, Dict, Any
from .models import ForecastPackage, ImageType, TemperatureUnit, WindSpeedUnit, PrecipitationUnit, OutputFormat

class MeteoblueClient:
    """
    Client for interacting with the Meteoblue API.
    """
    FORECAST_BASE_URL = "https://my.meteoblue.com/packages"
    IMAGE_BASE_URL = "https://my.meteoblue.com/visimage"
    SEARCH_BASE_URL = "https://www.meteoblue.com/en/server/search/query3"

    def __init__(self, api_key: str):
        """
        Initialize the client with an API key.
        
        Args:
            api_key: The Meteoblue API key.
        """
        self.api_key = api_key

    def get_forecast(
        self,
        lat: float,
        lon: float,
        packages: List[ForecastPackage],
        asl: Optional[int] = None,
        tz: Optional[str] = None,
        format: OutputFormat = OutputFormat.JSON,
        temperature: Optional[TemperatureUnit] = None,
        windspeed: Optional[WindSpeedUnit] = None,
        precipitationamount: Optional[PrecipitationUnit] = None,
    ) -> Dict[str, Any]:
        """
        Fetch weather forecast data.
        
        Args:
            lat: Latitude (WGS84).
            lon: Longitude (WGS84).
            packages: List of forecast packages to include.
            asl: Altitude above sea level in meters.
            tz: Timezone (e.g., 'Europe/Zurich').
            format: Output format (JSON or CSV).
            temperature: Temperature unit.
            windspeed: Wind speed unit.
            precipitationamount: Precipitation unit.
            
        Returns:
            Dictionary containing the forecast data.
        """
        package_str = "_".join([p.value for p in packages])
        url = f"{self.FORECAST_BASE_URL}/{package_str}"
        
        params = {
            "apikey": self.api_key,
            "lat": lat,
            "lon": lon,
            "format": format.value
        }
        
        if asl is not None:
            params["asl"] = asl
        if tz is not None:
            params["tz"] = tz
        if temperature is not None:
            params["temperature"] = temperature.value
        if windspeed is not None:
            params["windspeed"] = windspeed.value
        if precipitationamount is not None:
            params["precipitationamount"] = precipitationamount.value
            
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if format == OutputFormat.JSON:
            return response.json()
        return response.text  # Return raw text for CSV

    def get_image(
        self,
        image_type: ImageType,
        lat: float,
        lon: float,
        output_file: Optional[str] = None
    ) -> bytes:
        """
        Fetch a weather/climate image.
        
        Args:
            image_type: Type of image to generate.
            lat: Latitude.
            lon: Longitude.
            output_file: Optional path to save the image to.
            
        Returns:
            Raw image bytes.
        """
        url = f"{self.IMAGE_BASE_URL}/{image_type.value}"
        
        params = {
            "apikey": self.api_key,
            "lat": lat,
            "lon": lon
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if output_file:
            with open(output_file, "wb") as f:
                f.write(response.content)
                
        return response.content

    def search_location(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for a location by name.
        
        Args:
            query: Name of the city or place.
            
        Returns:
            List of matching locations with coordinates.
        """
        params = {
            "apikey": self.api_key,
            "query": query
        }
        
        response = requests.get(self.SEARCH_BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("results", [])
