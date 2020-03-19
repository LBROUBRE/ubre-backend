from rest_framework.views import APIView
from rest_framework.response import Response
from OSMPythonTools.nominatim import Nominatim
import requests


class RouteResponseView(APIView):
    def get(self, request, origin, dest):

        #TODO backend services
        nominatim = Nominatim()
        origen = nominatim.query(origin).toJSON()
        destino = nominatim.query(dest).toJSON()

        URL = "http://127.0.0.1:5000/route/v1/driving/" + \
              origen["lat"] + "," + origen["lon"] + ";" + \
              destino["lat"] + "," + destino["lon"]

        r = requests.get(URL)
        retorno_osrm = r.json()
        geometry = retorno_osrm["routes"]["0"]["geometry"]

        return Response(
            {
                "polyline":geometry
            }
        )