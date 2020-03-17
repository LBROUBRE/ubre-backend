from rest_framework.views import APIView
from rest_framework.response import Response

class RouteResponseView(APIView):
    def get(self, request, origin, dest):
        lat = origin
        #TODO
        lon = dest
        return Response(
            {
                lat:lon
            }
        )