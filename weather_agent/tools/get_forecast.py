from datetime import datetime, timedelta
from typing import List, Optional
from ..shared import client
from api.meteoblue_client.models import (
    ForecastPackage, 
    TemperatureUnit, 
    WindSpeedUnit, 
    PrecipitationUnit, 
    OutputFormat
)

# Cache for forecast results (2 hour TTL)
# Structure: {(lat, lon, packages_tuple, asl, tz, temp, wind, precip): {'forecast': {...}, 'timestamp': datetime}}
_forecast_cache = {}
CACHE_TTL_HOURS = 2


def get_forecast(
    lat: float,
    lon: float,
    packages: Optional[List[str]] = None,
    temperature_unit: Optional[str] = None,
    windspeed_unit: Optional[str] = None,
    precipitation_unit: Optional[str] = None,
    altitude_meters: Optional[int] = None,
    timezone: Optional[str] = None,
    output_format: str = "json",
    skip_cache: bool = False
) -> dict:
    """Retrieves weather forecast data for specific coordinates with full API capabilities.
    
    Use this tool AFTER you have obtained coordinates from search_location.
    This tool provides comprehensive weather forecast data with customizable packages, units, and formats.
    
    This function implements caching: if the same location and parameters are requested
    within 2 hours, it returns the cached result without calling the API.
    
    Args:
        lat: Latitude of the location (WGS84 decimal degrees). Required.
        lon: Longitude of the location (WGS84 decimal degrees). Required.
        packages: List of forecast packages to include. If None, defaults to ["basic-day"] (7-day daily forecast).
                 Available packages (use the string names):
                 - "basic-1h": Hourly forecast for 7 days
                 - "basic-day": Daily summaries for 7 days (default)
                 - "current": Current weather conditions
                 - "clouds": Cloud coverage data
                 - "sun_moon": Sunrise/sunset and moon phases
                 - "agro": Agricultural data (soil temperature, growing degree days, etc.)
                 - "solar": Solar radiation data
                 - "wind": Detailed wind data
                 - "sea": Marine/sea data
                 - "air": Air quality data
                 - "trend": 14-day trend forecast
                 You can combine multiple packages: ["basic-day", "current", "sun_moon"]
                 Examples:
                 - User asks "hourly forecast" -> use ["basic-1h"]
                 - User asks "current weather" -> use ["current"]
                 - User asks "sunrise and sunset" -> use ["sun_moon"]
                 - User asks "agricultural data" -> use ["agro"]
                 - User asks "solar radiation" -> use ["solar"]
                 - User asks "wind forecast" -> use ["wind"]
                 - User asks "marine forecast" -> use ["sea"]
                 - User asks "air quality" -> use ["air"]
                 - User asks "14 day trend" -> use ["trend"]
        temperature_unit: Temperature unit. Options: "C" (Celsius) or "F" (Fahrenheit).
                         If None, uses API default (usually Celsius).
                         Examples:
                         - User says "temperature in Fahrenheit" -> use "F"
                         - User says "temperature in Celsius" -> use "C"
                         - User says "degrees F" -> use "F"
        windspeed_unit: Wind speed unit. Options: "ms-1" (meters/second), "kmh" (km/h), 
                       "mph" (miles/hour), "kn" (knots).
                       If None, uses API default.
                       Examples:
                       - User says "wind in mph" -> use "mph"
                       - User says "wind in km/h" -> use "kmh"
                       - User says "wind in knots" -> use "kn"
                       - User says "wind in m/s" -> use "ms-1"
        precipitation_unit: Precipitation unit. Options: "mm" (millimeters) or "inch" (inches).
                           If None, uses API default (usually mm).
                           Examples:
                           - User says "rainfall in inches" -> use "inch"
                           - User says "precipitation in mm" -> use "mm"
        altitude_meters: Altitude above sea level in meters. Use when user mentions elevation,
                        mountain locations, or high-altitude areas.
                        Examples:
                        - User says "at 2000 meters" -> use 2000
                        - User says "mountain location at 1500m" -> use 1500
        timezone: Timezone identifier (e.g., "Europe/Zurich", "America/New_York", "Asia/Tokyo").
                 Use when user specifies a timezone or asks for times in a specific timezone.
                 Examples:
                 - User says "in EST timezone" -> use "America/New_York"
                 - User says "in Central European Time" -> use "Europe/Zurich"
                 - User says "times in UTC" -> use "UTC"
        output_format: Output format. Options: "json" (default) or "csv".
                      Use "csv" only if user explicitly requests CSV format.
        skip_cache: If True, bypasses the cache and always fetches fresh data from the API.
                   Use this when the user explicitly requests fresh data (e.g., mentions "CACHE_OVERRIDE").
                   Defaults to False.
        
    Returns:
        A dictionary with the forecast data.
        On success: {'status': 'success', 'forecast': {forecast data with requested packages}}
        On error: {'status': 'error', 'error_message': 'Failed to retrieve forecast'}
        
    Example workflows:
        1. Basic daily forecast:
           User: "What's the weather in London?"
           -> get_forecast(lat=51.5, lon=-0.12)
           
        2. Hourly forecast:
           User: "Give me hourly weather for Paris"
           -> get_forecast(lat=48.85, lon=2.35, packages=["basic-1h"])
           
        3. Current conditions:
           User: "What's the current weather in Tokyo?"
           -> get_forecast(lat=35.68, lon=139.69, packages=["current"])
           
        4. Multiple packages:
           User: "I need daily forecast, current conditions, and sunrise times for Madrid"
           -> get_forecast(lat=40.42, lon=-3.70, packages=["basic-day", "current", "sun_moon"])
           
        5. With units:
           User: "Weather in New York in Fahrenheit and wind in mph"
           -> get_forecast(lat=40.71, lon=-74.01, temperature_unit="F", windspeed_unit="mph")
           
        6. High altitude:
           User: "Weather forecast for a location at 2000 meters elevation"
           -> get_forecast(lat=46.52, lon=7.47, altitude_meters=2000)
           
        7. With timezone:
           User: "Weather in Los Angeles, show times in PST"
           -> get_forecast(lat=34.05, lon=-118.24, timezone="America/Los_Angeles")
           
        8. Agricultural data:
           User: "I need agricultural weather data for farming"
           -> get_forecast(lat=47.56, lon=7.57, packages=["agro"])
           
        9. Solar data:
           User: "What's the solar radiation forecast?"
           -> get_forecast(lat=47.56, lon=7.57, packages=["solar"])
           
        10. Marine forecast:
            User: "I need marine weather data"
            -> get_forecast(lat=47.56, lon=7.57, packages=["sea"])
    """
    global _forecast_cache
    
    # Convert package strings to ForecastPackage enums
    if packages is None:
        packages_enum = [ForecastPackage.BASIC_DAY]
    else:
        packages_enum = []
        # Map common user-friendly names to package values
        package_map = {
            "basic-1h": "basic-1h",
            "basic_1h": "basic-1h",
            "hourly": "basic-1h",
            "basic-day": "basic-day",
            "basic_day": "basic-day",
            "daily": "basic-day",
            "current": "current",
            "clouds": "clouds",
            "cloud": "clouds",
            "sun_moon": "sun_moon",
            "sun-moon": "sun_moon",
            "sun": "sun_moon",
            "moon": "sun_moon",
            "agro": "agro",
            "agricultural": "agro",
            "solar": "solar",
            "wind": "wind",
            "sea": "sea",
            "marine": "sea",
            "air": "air",
            "air_quality": "air",
            "air-quality": "air",
            "trend": "trend",
            "14day": "trend",
            "14-day": "trend"
        }
        
        for pkg in packages:
            pkg_lower = pkg.lower().strip()
            # Try mapping first
            mapped_pkg = package_map.get(pkg_lower, pkg_lower)
            
            # Try direct value match first (most reliable)
            try:
                packages_enum.append(ForecastPackage(mapped_pkg))
            except ValueError:
                # Try enum name match
                try:
                    pkg_upper = mapped_pkg.upper().replace("-", "_")
                    packages_enum.append(ForecastPackage[pkg_upper])
                except (KeyError, ValueError):
                    return {
                        "status": "error",
                        "error_message": f"Invalid package '{pkg}'. Valid packages: basic-1h, basic-day, current, clouds, sun_moon, agro, solar, wind, sea, air, trend"
                    }
    
    # Convert unit strings to enums
    temp_unit_enum = None
    if temperature_unit:
        try:
            temp_unit_enum = TemperatureUnit(temperature_unit.upper())
        except ValueError:
            return {
                "status": "error",
                "error_message": f"Invalid temperature unit '{temperature_unit}'. Use 'C' or 'F'"
            }
    
    wind_unit_enum = None
    if windspeed_unit:
        try:
            wind_unit_enum = WindSpeedUnit(windspeed_unit.lower())
        except ValueError:
            return {
                "status": "error",
                "error_message": f"Invalid windspeed unit '{windspeed_unit}'. Use 'ms-1', 'kmh', 'mph', or 'kn'"
            }
    
    precip_unit_enum = None
    if precipitation_unit:
        try:
            precip_unit_enum = PrecipitationUnit(precipitation_unit.lower())
        except ValueError:
            return {
                "status": "error",
                "error_message": f"Invalid precipitation unit '{precipitation_unit}'. Use 'mm' or 'inch'"
            }
    
    # Convert output format
    try:
        format_enum = OutputFormat(output_format.lower())
    except ValueError:
        return {
            "status": "error",
            "error_message": f"Invalid output format '{output_format}'. Use 'json' or 'csv'"
        }
    
    # Create cache key including all relevant parameters
    cache_key = (
        round(lat, 4),
        round(lon, 4),
        tuple(sorted([p.value for p in packages_enum])),  # Sort for consistency
        altitude_meters,
        timezone,
        temperature_unit,
        windspeed_unit,
        precipitation_unit,
        output_format
    )
    
    # Check cache only if skip_cache is False
    if not skip_cache:
        now = datetime.now()
        if cache_key in _forecast_cache:
            cached_entry = _forecast_cache[cache_key]
            cache_age = now - cached_entry['timestamp']
            
            # If cache is still valid (less than 2 hours old)
            if cache_age < timedelta(hours=CACHE_TTL_HOURS):
                return {"status": "success", "forecast": cached_entry['forecast']}
            else:
                # Cache expired, remove it
                del _forecast_cache[cache_key]
    
    # Cache miss, expired, or skip_cache=True - fetch from API
    now = datetime.now()
    try:
        forecast = client.get_forecast(
            lat=lat,
            lon=lon,
            packages=packages_enum,
            asl=altitude_meters,
            tz=timezone,
            format=format_enum,
            temperature=temp_unit_enum,
            windspeed=wind_unit_enum,
            precipitationamount=precip_unit_enum
        )
        
        # Store in cache (even if skip_cache was True, we still cache the fresh result)
        _forecast_cache[cache_key] = {
            'forecast': forecast,
            'timestamp': now
        }
        
        return {"status": "success", "forecast": forecast}
    except Exception as e:
        return {"status": "error", "error_message": f"Forecast retrieval failed: {str(e)}"}
