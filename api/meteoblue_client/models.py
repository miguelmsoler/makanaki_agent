from enum import Enum

class ForecastPackage(str, Enum):
    BASIC_1H = "basic-1h"
    BASIC_DAY = "basic-day"
    CURRENT = "current"
    CLOUDS = "clouds"
    SUN_MOON = "sun_moon"
    AGRO = "agro"
    SOLAR = "solar"
    WIND = "wind"
    SEA = "sea"
    AIR = "air"
    TREND = "trend"

class ImageType(str, Enum):
    METEOGRAM_CLIMATE = "meteogram_climate"
    METEOGRAM_14_DAY = "meteogram_14day"
    METEOGRAM_CURRENT_ON_CLIMATE = "meteogram_currentOnClimate"
    METEOGRAM_CLIMATE_YEAR = "meteogram_climateYear"
    CLIMATE_MODEL_TEMP_PRECIP = "climate_model/temp_precip"
    METEOGRAM_CLIMATE_WIND_ROSE = "meteogram_climate_wind_rose"

class TemperatureUnit(str, Enum):
    CELSIUS = "C"
    FAHRENHEIT = "F"

class WindSpeedUnit(str, Enum):
    MS = "ms-1"
    KMH = "kmh"
    MPH = "mph"
    KN = "kn"

class PrecipitationUnit(str, Enum):
    MILLIMETER = "mm"
    INCH = "inch"

class OutputFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
