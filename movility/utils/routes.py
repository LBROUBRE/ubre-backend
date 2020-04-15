# import all dependencies
from django.core import serializers
from datetime import datetime

from movility.models import Solicitudes, Vehiculos, Conductores, ParadasVirtuales
from movility.serializers import *
from movility.utils.VroomRequest import VroomRequest

# def name_to_coordinates(search_string, alldata=False): # TODO do this in Front-end
#     from OSMPythonTools.nominatim import Nominatim
#     nominatim = Nominatim()
#     response = nominatim.query(search_string).toJSON() # json["matches_number"]["info_parameter"]
#     if (alldata): return response
#     else: return str(response[0]["lat"]) + ", " + str(response[0]["lon"])


def generate_vroom_request():
    
    # get all instances of Solicitudes, Vehiculos and Conductores in the DB
    reqs = Solicitudes.objects.all()
    buses = Vehiculos.objects.all()
    # drivers = Conductores.objects.all()
    
    vroom_request = VroomRequest()
    
    # get all "paradas" in all Solicitudes instances;
    for req in reqs.iterator():
        origin = get_best_virtual_stop(req.origen)
        destination = get_best_virtual_stop(req.destino) 
        vroom_request.add_shipment(req.id, origin, destination, req.estado,
                                   req.fechaHoraSalida, req.fechaHoraLlegada, amount=1)
        # TODO?: origen y destino -> [lon, lat]

    # get all buses in Vehiculos instances
    for bus in buses.iterator():
        vroom_request.add_vehicle(bus.matricula)

    return vroom_request


def get_best_virtual_stop(location):
    import numpy as np
    # Right now it picks the closest virtual stop, on future versions the stop will be optimized
    # by the routing algorithm
    v_stops = ParadasVirtuales.objects.all()
    MAXIMUM_DISTANCE_FOR_CHECKING = 0.75  # maximum km
    approved_v_stops = []  # Here we will store all coordinates
    lon1 = int(location.split(",")[0])
    lat1 = int(location.split(",")[1])
    for v_stop in v_stops.iterator():
        lon2 = int(v_stop.coordenadas.split(",")[0])
        lat2 = int(v_stop.coordenadas.split(",")[1])

        if calculate_nodes_distance([lon1, lat1], [lon2, lat2]) < MAXIMUM_DISTANCE_FOR_CHECKING:
            approved_v_stops.append([lon2, lat2])

    best_duration = -1
    import requests as rest
    for approved_v_stop in approved_v_stops:
        destination = "%i, %i" % (approved_v_stop[1], approved_v_stop[0])
        origin = "%i, %i" % (lon1, lat1)
        res = rest.post("http://127.0.0.1:5000/route/v1/foot/%s;%s" % (origin, destination))
        duration = res.json()["routes"][0]["duration"]
        if best_duration == -1:
            best_duration = duration
            best_virtual_stop = destination
        elif best_duration < duration:
            best_duration = duration
            best_virtual_stop = destination

        return best_virtual_stop



def calculate_nodes_distance(n1, n2):
    from math import radians, cos, sin, asin, sqrt
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lng1, lat1, lng2, lat2 = map(radians, [n1[0], n1[1], n2[0], n2[1]]) # n1 = (lon,lat)
    # haversine formula
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r / 1000


def process_vroom_routing(request):
    import requests as rest
    from movility.utils.VroomResponseProcessor import VroomResponseProcessor

    vroom_response_processor = VroomResponseProcessor(request)

    routes = vroom_response_processor.get_routes()
    for route in routes:
        res = rest.post("http://127.0.0.1:8000/movility/routes/", json=route)
        for step in route["paradas"]:
            json = {
                "estado": 'A'
            }
            request_id = step["solicitudes"]
            res = rest.put("http://127.0.0.1:8000/movility/requests/%i" % request_id, json=json)
            


def vroom_call():

    # Generates a Vroom request Object and fills it with th DB data
    request = generate_vroom_request()
    
    # Process the Vroom response  and updates the DB with the data obtained
    process_vroom_routing(request)

    return 0
