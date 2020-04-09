# import all dependencies
from django.core import serializers
from datetime import datetime
from movility.models import Solicitudes, Vehiculos, Conductores
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
        vroom_request.add_shipment(req.id, req.origen, req.destino, req.estado,
                                   req.fechaHoraSalida, req.fechaHoraLlegada, amount=1)
        # TODO?: origen y destino -> [lon, lat]

    # get all buses in Vehiculos instances
    for bus in buses.iterator():
        vroom_request.add_vehicle(bus.matricula)

    return vroom_request


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
            print(res)


def vroom_call():

    # Generates a Vroom request Object and fills it with th DB data
    request = generate_vroom_request()

    # Process the Vroom response  and updates the DB with the data obtained
    process_vroom_routing(request)

    return 0
