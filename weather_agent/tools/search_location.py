from ..shared import client

def search_location(query: str) -> dict:
    """Searches for a location by name to get its coordinates.
    
    Use this tool when you need to find the latitude and longitude
    of a city or place before getting weather data. This is always
    the first step when a user asks about weather for a specific location.
    
    Args:
        query: The name of the city or place to search for (e.g., "Basel", "New York", "Tokyo").
        
    Returns:
        A dictionary with the search results.
        On success: {'status': 'success', 'results': [{'name': 'Basel, Switzerland', 'lat': 47.56, 'lon': 7.57, 'country': 'Switzerland', ...}]}
        On error: {'status': 'error', 'error_message': 'No results found for query'}
        
    Example:
        If user asks "What's the weather in Paris?", first call search_location("Paris")
        to get coordinates, then use those coordinates with get_forecast.
    """
    try:
        results = client.search_location(query)
        if not results:
            return {
                "status": "error",
                "error_message": f"No locations found for '{query}'. Please try a different city name."
            }
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "error_message": f"Search failed: {str(e)}"}
