Meteoblue has two APIs available in the free tier:

## Forecast API

The Forecast API provides access to instant weather data.

**Base URL**: `https://my.meteoblue.com/packages/[package-name]-[aggregation]`

**Required Parameters**:
- `apikey`: Your API Key (e.g., `nKUzq34iAcFWJw20`).
- `lat`: Latitude of the location (WGS84).
- `lon`: Longitude of the location (WGS84).

**Optional Parameters**:
- `asl`: Altitude above sea level in meters.
- `tz`: Timezone (e.g., `Europe/Zurich`).
- `format`: Output format (`json` or `csv`).
- `temperature`: Temperature unit (`C` or `F`).
- `windspeed`: Wind speed unit (`ms-1`, `kmh`, `mph`, `kn`).
- `precipitationamount`: Precipitation unit (`mm`, `inch`).

**Available Packages (Free Tier)**:
- `basic-1h`: 7-day forecast, hourly data.
- `basic-day`: 7-day forecast, daily summaries.
- `current`: Current data.
- `clouds`: Cloud coverage.
- `sun_moon`: Sunrise and sunset/moon phases.
- `agro`: Agricultural data.
- `solar`: Solar radiation data.
- `wind`: Wind data.
- `sea`: Marine data.
- `air`: Air quality data.
- `trend`: 14-day trend.

**Example Request**:
```bash
curl "https://my.meteoblue.com/packages/basic-1h_basic-day?lat=47.56&lon=7.57&apikey=nKUzq34iAcFWJw20&format=json"
```

## Image API

The Image API generates ready-to-use weather and climate diagrams.

**Base URL**: `https://my.meteoblue.com/visimage/[image-type]`

**Required Parameters**:
- `apikey`: Your API Key.
- `lat`: Latitude.
- `lon`: Longitude.

**Image Types (Free Tier - Climate)**:
- `meteogram_climate`: Standard climate diagram.
- `meteogram_currentOnClimate`: Comparison of current weather with climate.
- `meteogram_climateYear`: Annual course of temperature and precipitation.
- `climate_model/temp_precip`: Climate models for temperature and precipitation.
- `meteogram_climate_wind_rose`: Climate wind rose.

**Example Request**:
```bash
curl "https://my.meteoblue.com/visimage/meteogram_climate?lat=47.56&lon=7.57&apikey=nKUzq34iAcFWJw20" > meteogram_climate.png
```

**Limits and Conditions**:
- **Credits**: 10 million credits per year (renewable).
- **Rate Limit**: 500 calls per minute.
- **Usage**: Non-commercial use only.

## Location Search API

To resolve city names to coordinates (geocoding), you can use the Location Search API.

**Base URL**: `https://www.meteoblue.com/en/server/search/query3`

**Parameters**:
- `query`: City or place name.
- `apikey`: Your API Key.

**Example Request**:
```bash
curl "https://www.meteoblue.com/en/server/search/query3?query=Basel&apikey=nKUzq34iAcFWJw20"
```

**Response (JSON)**:
Returns a list of results with `name`, `lat`, `lon`, `country`, etc. You can take the first result to get the most likely coordinates.

Complete documentation can be found at https://docs.meteoblue.com/en/weather-apis/introduction/overview