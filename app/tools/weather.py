from agno.tools import tool


@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a specific location.
    For this demo, it always returns a sunny forecast for Madrid.
    """
    if "madrid" in city.lower():
        return "Está soleado en Madrid."
    return f"No tengo información del tiempo para {city}."