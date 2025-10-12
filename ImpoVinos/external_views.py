# ImpoVinos/external_views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# 🍷 API de Wine Explorer
class WineExplorerSearchView(APIView):
    """
    API que consume datos de Wine Explorer (Sample APIs) y los devuelve como JSON.
    Ejemplo:
      /api/v1/external/wine-explorer/search/?wine=Cabernet
    """
    permission_classes = []  # pública (no requiere token)

    def get(self, request):
        query = request.query_params.get("wine", "")
        if not query:
            return Response(
                {"error": "Debe indicar un vino en el parámetro 'wine'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # API pública de vinos (puedes cambiarla si tienes otra URL oficial)
        url = "https://api.sampleapis.com/wines/reds"

        try:
            response = requests.get(url, timeout=8)
            response.raise_for_status()
        except requests.RequestException:
            return Response(
                {"error": "No se pudo conectar con la API externa de Wine Explorer."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        wines = response.json()

        # Filtrar por nombre o bodega que contengan el texto buscado
        resultados = [
            w for w in wines
            if query.lower() in w.get("wine", "").lower() or query.lower() in w.get("winery", "").lower()
        ]

        # Devolver máximo 5 resultados
        return Response(resultados[:5], status=status.HTTP_200_OK)


# 🌤️ API del clima (Open-Meteo)
class WeatherCurrentView(APIView):
    """
    Endpoint para consultar el clima actual por coordenadas.
    Ejemplo:
      /api/v1/external/weather/current/?lat=-33.45&lon=-70.66
    """
    permission_classes = []  # pública (sin token requerido)

    def get(self, request):
        try:
            lat = float(request.query_params.get('lat', '-33.45'))  # Santiago de Chile
            lon = float(request.query_params.get('lon', '-70.66'))
        except ValueError:
            return Response(
                {"detail": "Parámetros lat/lon inválidos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
        }

        try:
            response = requests.get(url, params=params, timeout=8)
            response.raise_for_status()
        except requests.RequestException:
            return Response(
                {"detail": "Error al conectar con Open-Meteo"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        data = response.json().get("current_weather", {})
        return Response(
            {
                "latitude": lat,
                "longitude": lon,
                "temperature": data.get("temperature"),
                "windspeed": data.get("windspeed"),
                "weathercode": data.get("weathercode"),
                "time": data.get("time"),
            },
            status=status.HTTP_200_OK,
        )
