from google.adk.tools.tool_context import ToolContext
import google.genai.types as types
from ..shared import client
from api.meteoblue_client.models import ImageType

async def get_climate_image(lat: float, lon: float, city_name: str = "location", tool_context: ToolContext = None) -> dict:
    """Generates a 14-day meteogram image for specific coordinates and displays it in the chat.
    
    Use this tool to provide a visual representation of the 14-day weather forecast.
    The image shows temperature, precipitation, and other weather patterns over time.
    Call this AFTER getting coordinates from search_location.
    
    Args:
        lat: Latitude of the location.
        lon: Longitude of the location.
        city_name: Name of the city for the filename (optional, defaults to "location").
        tool_context: Tool context for saving artifacts (provided automatically by ADK).
        
    Returns:
        A dictionary with the status and artifact information.
        On success: {'status': 'success', 'message': 'Meteogram saved', 'filename': 'meteogram_basel.png'}
        On error: {'status': 'error', 'error_message': 'Failed to generate image'}
        
    Note:
        Images are saved as artifacts and automatically displayed in the chat interface.
    """
    try:
        # Sanitize city name for filename
        safe_name = "".join(c for c in city_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_').lower()
        filename = f"meteogram_{safe_name}.png"
        
        # Get image bytes from API (don't save to file)
        image_bytes = client.get_image(
            image_type=ImageType.METEOGRAM_14_DAY,
            lat=lat,
            lon=lon
        )
        
        # If tool_context is not provided, fall back to saving to /tmp
        if tool_context is None:
            # Fallback for backwards compatibility
            image_path = f"/tmp/{filename}"
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            return {
                "status": "success",
                "image_path": image_path,
                "message": f"Meteogram saved to {image_path}"
            }
        
        # Create artifact Part with image data
        image_artifact = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/png"
        )
        
        # Save as artifact (will display in chat) - AWAIT the async call
        version = await tool_context.save_artifact(filename, image_artifact)
        
        return {
            "status": "success",
            "message": f"14-day meteogram saved",
            "filename": filename,
            "version": version
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Image generation failed: {str(e)}"}
