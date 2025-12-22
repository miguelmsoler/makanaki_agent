# Makanaki - Weather Agent powered by Meteoblue API

An educational demo built with Google ADK that demonstrates agent capabilities using the Meteoblue API for weather data.

## 🌟 Features

- **Conversational agent** with Google ADK and Gemini 2.0 Flash
- **Specialized sub-agent** for location search
- **14-day forecasts** with visual meteograms
- **Standardized format** with tables and emojis
- **Integrated images** in chat using artifacts
- **Smart caching** to optimize API calls

## 🚀 Quick Start

### Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) for dependency management
- Meteoblue API key ([get one here](https://www.meteoblue.com/en/weather-api))
- Google AI API key ([get one here](https://ai.google.dev/))

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd makanaki

# Install dependencies
uv sync

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Environment Variables

Create a `.env` file in the project root:

```env
METEOBLUE_API_KEY=your_meteoblue_api_key
GOOGLE_API_KEY=your_google_api_key
```

### Run the Agent

```bash
# Start the ADK web interface
uv run adk web

# Open in browser
# http://127.0.0.1:8000
```

### Run Tests

```bash
# All tests
uv run pytest

# Unit tests only (skip integration)
uv run pytest -m "not integration"

# Specific tests
uv run pytest api/tests/test_meteoblue_client.py
```

## 📁 Project Structure

```
makanaki/
├── weather_agent/              # Main ADK agent
│   ├── agent.py               # root_agent definition
│   ├── shared.py              # Shared Meteoblue client
│   ├── tools/                 # Agent tools
│   │   ├── search_location.py
│   │   ├── get_forecast.py
│   │   └── get_climate_image.py
│   └── sub_agents/            # Specialized sub-agents
│       └── location_agent.py  # Location search
├── api/                       # Meteoblue API client
│   ├── meteoblue_client/      # Client implementation
│   │   ├── client.py
│   │   └── models.py          # Enums and models
│   └── tests/                 # Test suite
│       ├── test_meteoblue_client.py
│       └── test_integration.py
├── refs/                      # Reference documentation
│   ├── adk-docs/             # ADK documentation
│   └── adk-python/           # ADK Python source code
├── ADK_SNIPPETS.md           # ADK snippets guide
├── AGENTS.md                 # Agent rules
└── pyproject.toml            # Project configuration
```

## 🛠️ API Client Usage

```python
from api.meteoblue_client import MeteoblueClient
from api.meteoblue_client.models import ForecastPackage, ImageType

client = MeteoblueClient(api_key="YOUR_API_KEY")

# Search for a city
results = client.search_location("Buenos Aires")
lat, lon = results[0]["lat"], results[0]["lon"]

# Get 7-day forecast
forecast = client.get_forecast(
    lat=lat, 
    lon=lon, 
    packages=[ForecastPackage.BASIC_DAY]
)

# Download 14-day meteogram
client.get_image(
    image_type=ImageType.METEOGRAM_14_DAY,
    lat=lat,
    lon=lon,
    output_file="meteogram.png"
)
```

## 🤖 Agent Architecture

### Main Agent (`root_agent`)

- **Model**: Gemini 2.0 Flash
- **Tools**:
  - `location_agent` (sub-agent): Location search
  - `get_forecast`: Get weather forecasts
  - `get_climate_image`: Generate visual meteograms

### Location Sub-Agent

Specialized in finding city coordinates:
- Handles context like country, region, province
- Intelligently filters multiple results
- Only searches for cities (not regions or countries)

### Output Format

The agent presents 7-day forecasts in table format:

| Date | Weather | Temperature (°C) | Precipitation (mm) |
|------|---------|------------------|-------------------|
| ... | ☀️ | ... | ... |

With creative adaptation for other forecast types (hourly, current, etc.)

## 📦 Available Forecast Packages

- `basic-1h`: Hourly forecast for 7 days
- `basic-day`: Daily summaries for 7 days (default)
- `current`: Current weather conditions
- `clouds`: Cloud coverage data
- `sun_moon`: Sunrise/sunset and moon phases
- `agro`: Agricultural data
- `solar`: Solar radiation data
- `wind`: Detailed wind data
- `sea`: Marine data
- `air`: Air quality data
- `trend`: 14-day trend forecast

## 🖼️ Image Types

- `meteogram_14day`: 14-day meteogram (default)
- `meteogram_climate`: Climate diagram
- `meteogram_currentOnClimate`: Current on climate
- `meteogram_climateYear`: Annual climate
- `meteogram_climate_wind_rose`: Climate wind rose

## 🧪 Testing

The project includes:
- **Unit tests**: API mocks
- **Integration tests**: Real API calls
- **Coverage**: Client, tools, and agent

## 📚 Documentation

- `ADK_SNIPPETS.md`: Complete ADK guide with examples
- `api/meteoblue.md`: Meteoblue API documentation
- `refs/adk-docs/`: Official ADK documentation
- `AGENTS.md`: Rules for agents working on this project

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Meteoblue](https://www.meteoblue.com/) for their excellent weather API
- [Google ADK](https://github.com/google/adk) for the agent framework
- [uv](https://github.com/astral-sh/uv) for dependency management
