# ADK Snippets for Weather Agent

This document contains guidelines and code snippets extracted from the ADK repositories for building a weather agent that uses Meteoblue as a tool.

## Core Concepts

### What is a Tool in ADK?

Tools are programming functions with structured input and output that can be called by an ADK Agent to perform actions. They extend agent capabilities by allowing them to:
- Query databases
- Make API requests (e.g., getting weather data)
- Search the web
- Execute code snippets
- Retrieve information from documents

### How Agents Use Tools

1. **Reasoning**: The agent's LLM analyzes its system instruction, conversation history, and user request.
2. **Selection**: Based on the analysis, the LLM decides which tool to execute.
3. **Invocation**: The LLM generates the required arguments and triggers execution.
4. **Observation**: The agent receives the output from the tool.
5. **Finalization**: The agent incorporates the tool's output into its response.

## Building Function Tools

## ADK Project Structure

### Directory Layout

ADK expects agents to be organized in a specific directory structure for compatibility with `adk web` and other ADK tools.

**Correct Structure:**
```
your_project/
├── weather_agent/           # Agent package directory
│   ├── __init__.py         # Package init (imports agent module)
│   └── agent.py            # Defines root_agent
├── api/                    # Your API clients and utilities
├── pyproject.toml          # Project configuration
└── .env                    # Environment variables
```

**Key Requirements:**
1. **Agent Directory**: Each agent must be in its own directory (e.g., `weather_agent/`)
2. **`__init__.py`**: Must import the agent module
3. **`agent.py`**: Must define a variable named `root_agent` (not any other name)
4. **Location**: Agent directories should be at the project root level

### File Templates

#### `__init__.py`
```python
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from . import agent
```

#### `agent.py`
```python
# Copyright 2025 Google LLC
# ... (license header)

from google.adk import Agent

# Define your tool functions here
def my_tool(param: str) -> dict:
    """Tool docstring."""
    return {"status": "success", "result": "..."}

# IMPORTANT: Must be named 'root_agent'
# NOTE: Do NOT pass api_key - ADK handles credentials automatically
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='my_agent_name',
    description="Agent description",
    instruction="Agent instructions...",
    tools=[my_tool],
    # api_key is NOT needed - ADK reads GOOGLE_API_KEY from .env automatically
)
```

### Running with ADK Web

From your project root directory:
```bash
# ADK will auto-detect agents in the current directory
adk web

# Or specify a specific agent directory
adk web weather_agent
```

**Note**: When using `uv` for dependency management:
```bash
uv run adk web
```

### Credentials Configuration

**IMPORTANT**: ADK handles Google API credentials automatically. Do NOT pass `api_key` as a parameter to the `Agent` constructor.

**How ADK handles credentials:**
- ADK automatically reads credentials from environment variables
- For Google Gemini models, set `GOOGLE_API_KEY` in your `.env` file
- ADK uses `InMemoryCredentialService` (experimental) when running with `adk web`
- Passing `api_key` to `Agent()` will cause a Pydantic validation error: `Extra inputs are not permitted`

**Correct setup:**
1. Create a `.env` file in your project root:
```
GOOGLE_API_KEY=your_google_api_key_here
METEOBLUE_API_KEY=your_meteoblue_api_key_here
```

2. Load environment variables in your agent code (for your own API clients):
```python
from dotenv import load_dotenv
import os

load_dotenv()
# Use for your own API clients (e.g., Meteoblue)
client = MeteoblueClient(api_key=os.getenv("METEOBLUE_API_KEY"))
```

3. Do NOT pass api_key to Agent:
```python
# ✅ Correct
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='my_agent',
    # ADK reads GOOGLE_API_KEY from environment automatically
)

# ❌ Wrong - will cause validation error
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='my_agent',
    api_key=os.getenv("GOOGLE_API_KEY"),  # Don't do this!
)
```

### Common Mistakes to Avoid

❌ **Wrong**: Standalone file `weather_agent.py` at root level
```
your_project/
└── weather_agent.py  # Won't work with adk web
```

❌ **Wrong**: Agent variable not named `root_agent`
```python
# In agent.py
my_agent = Agent(...)  # Wrong variable name
```

❌ **Wrong**: Passing `api_key` parameter to Agent constructor
```python
# This will cause a Pydantic validation error!
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='my_agent',
    api_key=os.getenv("GOOGLE_API_KEY"),  # ❌ NOT ALLOWED
    # ... other params
)
```

✅ **Correct**: Agent in directory with proper structure
```
your_project/
└── weather_agent/
    ├── __init__.py
    └── agent.py  # Contains root_agent
```

✅ **Correct**: Let ADK handle credentials automatically
```python
# ADK automatically reads credentials from environment variables
# No need to pass api_key to Agent constructor
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='my_agent',
    # api_key parameter is NOT needed - ADK handles it automatically
    # ... other params
)
```

## Building Function Tools


### Basic Agent Structure

```python
from google.adk import Agent

# IMPORTANT: Do NOT pass api_key parameter
# ADK automatically reads GOOGLE_API_KEY from environment variables
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='weather_agent',
    description="An agent that provides weather forecasts using Meteoblue API.",
    instruction="""You are a weather assistant that helps users get weather forecasts.
    
    When a user asks for weather information:
    1. Use search_location to find the city coordinates
    2. Use get_forecast to retrieve the weather data
    3. Present the information in a user-friendly format
    """,
    tools=[search_location, get_forecast, get_image],
    # api_key is NOT needed - ADK handles it automatically
)
```

### Function Tool Best Practices

#### 1. Clear Function Names
Use descriptive, verb-noun based names:
- ✅ `get_weather`, `search_location`, `fetch_forecast`
- ❌ `run`, `process`, `do_stuff`

#### 2. Well-Defined Parameters

**Required Parameters** (no default value):
```python
def get_weather(city: str, unit: str) -> dict:
    """
    Retrieves the weather for a city in the specified unit.
    
    Args:
        city (str): The city name.
        unit (str): The temperature unit, either 'Celsius' or 'Fahrenheit'.
    """
    # ... function logic ...
    return {"status": "success", "report": f"Weather for {city} is sunny."}
```

**Optional Parameters** (with default value):
```python
def search_flights(destination: str, departure_date: str, flexible_days: int = 0) -> dict:
    """
    Searches for flights.
    
    Args:
        destination (str): The destination city.
        departure_date (str): The desired departure date.
        flexible_days (int, optional): Number of flexible days for the search. Defaults to 0.
    """
    # ... function logic ...
    return {"status": "success", "flights": [...]}
```

#### 3. Return Type: Always Use Dictionaries

The preferred return type is a **dictionary** with a `status` key:

```python
def lookup_order_status(order_id: str) -> dict:
    """Fetches the current status of a customer's order using its ID.
    
    Returns:
        A dictionary indicating the outcome.
        On success, status is 'success' and includes an 'order' dictionary.
        On failure, status is 'error' and includes an 'error_message'.
        Example success: {'status': 'success', 'order': {'state': 'shipped', 'tracking_number': '1Z9...'}}
        Example error: {'status': 'error', 'error_message': 'Order ID not found.'}
    """
    if status_details := fetch_status_from_backend(order_id):
        return {
            "status": "success",
            "order": {
                "state": status_details.state,
                "tracking_number": status_details.tracking,
            },
        }
    else:
        return {"status": "error", "error_message": f"Order ID {order_id} not found."}
```

#### 4. Comprehensive Docstrings

The docstring is **critical** - it's the primary source of information for the LLM:

```python
def get_weather_forecast(city: str, days: int) -> dict:
    """Retrieves a multi-day weather forecast for a specified city.
    
    Use this tool when a user asks for weather predictions for multiple days.
    Do not use it for current weather conditions (use get_current_weather instead).
    
    Args:
        city: The name of the city to get the forecast for.
        days: The number of days to forecast (1-14).
        
    Returns:
        A dictionary with status and forecast data.
        On success: {'status': 'success', 'forecast': [{'date': '2025-11-30', 'temp_max': 25, ...}]}
        On error: {'status': 'error', 'error_message': 'City not found'}
    """
    # ... implementation ...
```

### Using ToolContext

For advanced scenarios, use `ToolContext` to access session state and control agent flow:

```python
from google.adk.tools.tool_context import ToolContext

def save_user_preference(theme: str, tool_context: ToolContext) -> dict:
    """Updates a user-specific preference.
    
    Args:
        theme: The theme preference ('light' or 'dark').
    """
    # Write to user-specific state
    tool_context.state['user:preferences:theme'] = theme
    
    return {
        "status": "success",
        "message": f"Theme preference updated to {theme}"
    }
```

**State Prefixes:**
- `app:*` - Shared across all users
- `user:*` - Specific to the current user across all sessions
- (No prefix) - Specific to the current session
- `temp:*` - Temporary, not persisted (for passing data within a single run)

### Sequential Tool Usage

When tools need to be called in sequence, describe the workflow in the agent's instruction:

```python
instruction="""You are a weather sentiment analyzer.

When a user asks about weather and sentiment:
1. First, call get_weather(city) to retrieve the weather data
2. Wait for the weather result
3. Then, call analyze_sentiment(weather_description) with the weather data
4. Present both the weather and sentiment analysis to the user

If get_weather returns an error, inform the user and do not call analyze_sentiment.
"""
```

## Weather Agent Example Pattern

Based on the ADK patterns, here's the complete structure for a Meteoblue weather agent.

**File: `weather_agent/agent.py`**

```python
# Copyright 2025 Google LLC
# ... (license header)

import os
from google.adk import Agent
from api.meteoblue_client import MeteoblueClient
from api.meteoblue_client.models import ForecastPackage, ImageType
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Meteoblue client
client = MeteoblueClient(api_key=os.getenv("METEOBLUE_API_KEY"))

def search_location(query: str) -> dict:
    """Searches for a location by name to get its coordinates.
    
    Use this tool when you need to find the latitude and longitude
    of a city or place before getting weather data.
    
    Args:
        query: The name of the city or place to search for.
        
    Returns:
        On success: {'status': 'success', 'results': [{'name': 'Basel', 'lat': 47.56, 'lon': 7.57, ...}]}
        On error: {'status': 'error', 'error_message': 'No results found'}
    """
    try:
        results = client.search_location(query)
        if not results:
            return {"status": "error", "error_message": f"No locations found for '{query}'"}
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def get_forecast(lat: float, lon: float, days: int = 7) -> dict:
    """Retrieves weather forecast data for specific coordinates.
    
    Use this tool after you have obtained coordinates from search_location.
    Provides detailed forecast including temperature, precipitation, wind, etc.
    
    Args:
        lat: Latitude of the location (WGS84).
        lon: Longitude of the location (WGS84).
        days: Number of forecast days (1-7). Defaults to 7.
        
    Returns:
        On success: {'status': 'success', 'forecast': {...}}
        On error: {'status': 'error', 'error_message': '...'}
    """
    try:
        forecast = client.get_forecast(
            lat=lat,
            lon=lon,
            packages=[ForecastPackage.BASIC_DAY]
        )
        return {"status": "success", "forecast": forecast}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def get_climate_image(lat: float, lon: float, city_name: str = "location") -> dict:
    """Generates a climate diagram image for specific coordinates.
    
    Use this tool to provide a visual representation of climate data.
    The image is saved to /tmp/ directory.
    
    Args:
        lat: Latitude of the location.
        lon: Longitude of the location.
        city_name: Name of the city for the filename (optional).
        
    Returns:
        On success: {'status': 'success', 'image_path': '/tmp/climate_image.png'}
        On error: {'status': 'error', 'error_message': '...'}
    """
    try:
        safe_name = "".join(c for c in city_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_').lower()
        image_path = f"/tmp/climate_{safe_name}.png"
        
        client.get_image(
            image_type=ImageType.METEOGRAM_CLIMATE,
            lat=lat,
            lon=lon,
            output_file=image_path
        )
        return {"status": "success", "image_path": image_path}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

# IMPORTANT: Must be named 'root_agent' for ADK to detect it
# NOTE: Do NOT pass api_key parameter - ADK handles credentials automatically
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='meteoblue_weather_agent',
    description="A weather assistant that provides forecasts using Meteoblue API.",
    instruction="""You are a helpful weather assistant powered by Meteoblue.

When a user asks for weather information:
1. Use search_location to find the city and get its coordinates
2. Extract the latitude and longitude from the first result
3. Use get_forecast with those coordinates to get weather data
4. Optionally, use get_climate_image to provide a visual diagram
5. Present the weather information in a clear, user-friendly format

If search_location returns no results, ask the user to provide a different city name.
If get_forecast fails, inform the user and suggest trying again.

Always mention that the data comes from Meteoblue.
""",
    tools=[search_location, get_forecast, get_climate_image],
    # api_key is NOT needed - ADK reads GOOGLE_API_KEY from .env automatically
)
```

**File: `weather_agent/__init__.py`**

```python
# Copyright 2025 Google LLC
# ... (license header)

from . import agent
```

## Troubleshooting Common Errors

### Pydantic Validation Error: "Extra inputs are not permitted"

**Error message:**
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for LlmAgent
api_key
  Extra inputs are not permitted [type=extra_forbidden, input_value='...', input_type=str]
```

**Cause:** Passing `api_key` parameter to the `Agent()` constructor.

**Solution:** Remove the `api_key` parameter. ADK handles credentials automatically.

```python
# ❌ Wrong - causes validation error
root_agent = Agent(
    model='gemini-2.0-flash-001',
    api_key=os.getenv("GOOGLE_API_KEY"),  # Remove this line!
    # ... other params
)

# ✅ Correct - ADK handles credentials automatically
root_agent = Agent(
    model='gemini-2.0-flash-001',
    # ADK reads GOOGLE_API_KEY from .env automatically
    # ... other params
)
```

**How ADK handles credentials:**
- ADK automatically reads `GOOGLE_API_KEY` from your `.env` file
- When running `adk web`, ADK uses `InMemoryCredentialService` (experimental)
- No need to manually pass credentials to the Agent constructor

## Key Takeaways

1. **Follow ADK structure**: Use proper directory layout with `__init__.py` and `agent.py` defining `root_agent`
2. **Do NOT pass `api_key` to Agent**: ADK handles Google API credentials automatically via environment variables. Passing `api_key` will cause a Pydantic validation error.
3. **Keep tools focused**: Each tool should do one thing well
4. **Use descriptive names**: Both function names and parameter names should be clear
5. **Return dictionaries with status**: Always include a `status` key in your return value
6. **Write comprehensive docstrings**: The LLM relies heavily on these
7. **Describe sequential workflows**: Tell the agent the order to call tools in the instruction
8. **Handle errors gracefully**: Return error dictionaries with clear messages
9. **Use type hints**: Essential for ADK to generate the correct schema
10. **Environment variables**: Set `GOOGLE_API_KEY` in `.env` file - ADK will read it automatically


## References

- ADK Python Samples: `/refs/adk-python/contributing/samples/`
- ADK Documentation: `/refs/adk-docs/docs/`
- Function Tools Guide: `/refs/adk-docs/docs/tools-custom/function-tools.md`
- Tools Overview: `/refs/adk-docs/docs/tools-custom/index.md`

## Using Agents as Tools (Sub-Agents)

ADK allows you to use an Agent as a tool for another Agent. This is useful for decomposing complex tasks into specialized sub-agents.

### The `AgentTool` Wrapper

To use an agent as a tool, wrap it with `AgentTool` from `google.adk.tools`.

```python
from google.adk.tools import AgentTool
from .sub_agents.my_sub_agent import my_sub_agent

# ...

root_agent = Agent(
    # ...
    tools=[
        AgentTool(my_sub_agent),
        # other tools...
    ]
)
```

### Sub-Agent Implementation

A sub-agent is just a regular ADK Agent. It can have its own tools and instructions.

```python
# weather_agent/sub_agents/location_agent.py
from google.adk import Agent
from ..tools import search_location

location_agent = Agent(
    model='gemini-2.0-flash-001',
    name='location_finder',
    description="Finds coordinates for cities.",
    instruction="You are a location finder. Your job is to find the coordinates of a city...",
    tools=[search_location]
)
```

## Using Artifacts for Images and Files

Artifacts allow agents to save and display binary data (images, PDFs, etc.) in the chat interface.

### Saving Images as Artifacts

To display an image in the chat, save it as an artifact using `tool_context.save_artifact()`:

```python
from google.adk.tools.tool_context import ToolContext
import google.genai.types as types

def my_image_tool(lat: float, lon: float, tool_context: ToolContext) -> dict:
    """Tool that generates and displays an image."""
    # Get image bytes from API or generate them
    image_bytes = get_image_from_somewhere(lat, lon)
    
    # Create artifact Part with image data
    image_artifact = types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/png"
    )
    
    # Save as artifact (will display in chat)
    filename = f"image_{lat}_{lon}.png"
    version = tool_context.save_artifact(filename, image_artifact)
    
    return {
        "status": "success",
        "message": f"Image saved as {filename}",
        "version": version
    }
```

### Key Points

- **ToolContext Parameter**: Tools must accept `tool_context: ToolContext` to access artifact service
- **MIME Type**: Always specify correct MIME type (`image/png`, `image/jpeg`, `application/pdf`, etc.)
- **Automatic Display**: Saved artifacts automatically appear in the chat interface
- **Versioning**: Each save creates a new version, returned by `save_artifact()`

### Loading Artifacts

```python
async def load_previous_image(tool_context: ToolContext) -> dict:
    """Load a previously saved artifact."""
    filename = "my_image.png"
    
    # Load latest version
    artifact = await tool_context.load_artifact(filename)
    
    if artifact and artifact.inline_data:
        image_bytes = artifact.inline_data.data
        mime_type = artifact.inline_data.mime_type
        return {"status": "success", "size": len(image_bytes)}
    
    return {"status": "error", "message": "Artifact not found"}
```
