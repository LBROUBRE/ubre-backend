# import all dependencies
from django.core import serializers
from datetime import datetime

from movility.models import Solicitudes, Vehiculos, Conductores, ParadasVirtuales
from movility.serializers import *
from movility.utils.VroomRequest import VroomRequest

from movility.utils.output import createNewOutput, getLastOutputData, setLastOutputData  # OUTPUT

# def name_to_coordinates(search_string, alldata=False): # TODO do this in Front-end
#     from OSMPythonTools.nominatim import Nominatim
#     nominatim = Nominatim()
#     response = nominatim.query(search_string).toJSON() # json["matches_number"]["info_parameter"]
#     if (alldata): return response
#     else: return str(response[0]["lat"]) + ", " + str(response[0]["lon"])


def generate_vroom_request():

    createNewOutput()  # OUTPUT
    output_data = getLastOutputData()  # OUTPUT
    
    # get all instances of Solicitudes, Vehiculos and Conductores in the DB
    reqs = Solicitudes.objects.all()
    buses = Vehiculos.objects.all()
    # drivers = Conductores.objects.all()
    
    vroom_request = VroomRequest()
    
    # get all "paradas" in all Solicitudes instances;
    for req in reqs.iterator():
        origin_vs_id, origin= get_best_virtual_stop(req.origen)
        destination_vs_id, destination = get_best_virtual_stop(req.destino)
        vroom_request.add_shipment(req.id, origin_vs_id, origin, destination_vs_id, destination, req.estado,
                                   req.fechaHoraSalida, req.fechaHoraLlegada, amount=1)
        output_data["solicitudes"].append({  # OUTPUT
            "id":req.id,
            "estado":"A",  # will change to "R" in VroomResponseProcessor, if it is necessary
            "origen_deseado":req.origen,
            "destino_deseado":req.destino,
            "origen_real":origin,
            "destino_real":destination,
            "hora_salida_deseada":datetime.fromtimestamp(req.fechaHoraSalida.timestamp()).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "hora_llegada_deseada":datetime.fromtimestamp(req.fechaHoraLlegada.timestamp()).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "hora_salida_real":None,
            "hora_llegada_real":None
        })

    # get all buses in Vehiculos instances
    for bus in buses.iterator():
        vroom_request.add_vehicle(bus.matricula)
    
    setLastOutputData(output_data)  # OUTPUT

    return vroom_request


def get_best_virtual_stop(location):
    import numpy as np
    # Right now it picks the closest virtual stop, on future versions the stop will be optimized
    # by the routing algorithm
    v_stops = ParadasVirtuales.objects.all()
    MAXIMUM_DISTANCE_FOR_CHECKING = 0.75  # maximum km
    approved_v_stops = []  # Here we will store all coordinates
    lon1 = float(location.split(",")[0])
    lat1 = float(location.split(",")[1])
    for v_stop in v_stops.iterator():
        lon2 = float(v_stop.coordenadas.split(",")[0])
        lat2 = float(v_stop.coordenadas.split(",")[1])

        if calculate_nodes_distance([lon1, lat1], [lon2, lat2]) < MAXIMUM_DISTANCE_FOR_CHECKING:
            approved_v_stops.append(v_stop)

    best_duration = -1
    best_virtual_stop = None
    import requests as rest
    for approved_v_stop in approved_v_stops:
        destination = "%s,%s" % (approved_v_stop.coordenadas.split(",")[0], approved_v_stop.coordenadas.split(",")[1])
        origin = "%s,%s" % (lon1, lat1)
        res = rest.post("http://127.0.0.1:5000/route/v1/foot/%s;%s" % (origin, destination))
        duration = res.json()["routes"][0]["duration"]
        if (best_duration < duration) or (best_duration == -1):
            best_duration = duration
            best_virtual_stop = approved_v_stop

    if best_virtual_stop is None:
        # Crear vparada
        json = {
            "coordenadas": "%f,%f"%(lon1,lat1)
        }
        res = rest.post("http://127.0.0.1:8000/movility/stops/", json=json)
        best_virtual_stop = res.json()
    
    if (isinstance(best_virtual_stop,dict)):
        return best_virtual_stop["id"], best_virtual_stop["coordenadas"]
    else:
        return best_virtual_stop.id, best_virtual_stop.coordenadas


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
    return c * r


def process_vroom_routing(request):
    import requests as rest
    from movility.utils.VroomResponseProcessor import VroomResponseProcessor

    vroom_response_processor = VroomResponseProcessor(request)

    routes = vroom_response_processor.get_routes()

    output_data = getLastOutputData()  # OUTPUT
    
    for route in routes:
        rest.post("http://127.0.0.1:8000/movility/routes/", json=route)

        solicitudes_atendidas = []  # OUTPUT
        
        for step in route["steps"]:
            json = {
                "estado": 'A'
            }
            request_id = step["solicitudes"]
            rest.put("http://127.0.0.1:8000/movility/requests/%i" % request_id, json=json)
            
            if request_id not in solicitudes_atendidas:  # OUTPUT
                solicitudes_atendidas.append(request_id)
        
        response_routes = rest.get("http://127.0.0.1:8000/movility/routes/").json()  # OUTPUT - get max route_id in DB
        route_id = 0  # OUTPUT
        for route in response_routes:  # OUTPUT
            route_id = route["id"] if route["id"] > route_id else route_id
        output_data["rutas"].append({  # OUTPUT
            "id":route_id,
            "solicitudes_atendidas":solicitudes_atendidas,
            "tramos":[]
        })

    for route_index, route in enumerate(request.response["routes"]):
        for step_index in range(1,(len(route["steps"]))):
            output_data["rutas"][route_index]["tramos"].append({
                "origen":route["steps"][step_index-1]["location"],
                "destino":route["steps"][step_index]["location"],
                "pasajeros":route["steps"][step_index]["load"]
            })

    setLastOutputData(output_data)  # OUTPUT
            


def vroom_call():

    # Generates a Vroom request Object and fills it with th DB data
    request = generate_vroom_request()
    
    # Process the Vroom response  and updates the DB with the data obtained
    process_vroom_routing(request)

    return 0
