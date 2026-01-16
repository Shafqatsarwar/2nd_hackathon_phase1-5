import requests
import logging


def get_weather_info(location: str) -> str:
    """
    Get current weather information for a location.
    This function tries multiple weather sources to get current weather data.
    """
    # Try to get weather from wttr.in (simple weather service)
    try:
        # Format location for URL
        formatted_location = location.replace(" ", "+").replace(",", "")
        url = f"http://wttr.in/{formatted_location}?format=3"

        response = requests.get(url, timeout=10)
        if response.status_code == 200 and response.text.strip():
            return f"Current weather for {location}: {response.text.strip()}"
    except Exception as e:
        logging.warning(f"Weather API request failed: {e}")

    # If wttr.in fails, try a web search with more specific terms
    try:
        from .web_search import search_web
        search_query = f"current weather {location} today temperature"
        result = search_web(search_query, max_results=3)

        if result and "No results found" not in result:
            return f"Weather information for {location}:\n{result[:500]}..."
    except Exception as e:
        logging.warning(f"Web search for weather failed: {e}")

    return f"Unable to retrieve current weather for {location}. Please try again later or check a weather service directly."


def get_weather_forecast(location: str) -> str:
    """
    Get weather forecast for a location.
    """
    try:
        from .web_search import search_web
        search_query = f"{location} weather forecast next 3 days"
        result = search_web(search_query, max_results=3)

        if result and "No results found" not in result:
            return f"Weather forecast for {location}:\n{result[:500]}..."
        else:
            return f"Could not find a weather forecast for {location}."
    except Exception as e:
        logging.error(f"Error getting weather forecast: {e}")
        return f"Error retrieving weather forecast for {location}: {str(e)}"