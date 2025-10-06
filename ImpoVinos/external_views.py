# ImpoVinos/external_views.py
import os
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


RAPIDAPI_HOST = os.environ.get(
    "RAPIDAPI_HOST",
    "wine-explorer-api-ratings-insights-and-search.p.rapidapi.com",  # host por defecto de esta API
)
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")

BASE_URL = f"https://{RAPIDAPI_HOST}"
SEARCH_PATH = "/search"  # del snippet: /search?wine_name=...

class WineExplorerSearchView(APIView):
    """
    GET /api/v1/external/wine-explorer/search/?q=syrah
    Traduce 'q' -> 'wine_name' para el proveedor.
    Requiere RAPIDAPI_KEY (y opcionalmente RAPIDAPI_HOST) en variables de entorno.
    """

    def get(self, request):
        if not RAPIDAPI_KEY:
            return Response(
                {"detail": "Falta RAPIDAPI_KEY en variables de entorno (.env)."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        q = (request.query_params.get("q") or request.query_params.get("wine_name") or "").strip()
        if not q:
            return Response({"detail": "Falta parámetro 'q'."}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST,
            "Accept": "application/json",
        }
        params = {"wine_name": q}  # este endpoint usa 'wine_name'

        try:
            r = requests.get(BASE_URL + SEARCH_PATH, headers=headers, params=params, timeout=12)
            r.raise_for_status()
            # Intentar parsear JSON; si no, devolver texto
            try:
                data = r.json()
            except ValueError:
                data = {"raw": r.text}
            return Response(data, status=r.status_code)
        except requests.exceptions.HTTPError:
            return Response(
                {"detail": "Error HTTP del proveedor", "status": r.status_code, "body": r.text[:1000]},
                status=r.status_code,
            )
        except requests.exceptions.RequestException as e:
            return Response({"detail": f"Error de red externo: {e}"}, status=status.HTTP_502_BAD_GATEWAY)