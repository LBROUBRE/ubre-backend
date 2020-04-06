# import all dependencies
from django.core import serializers
from datetime import datetime
from movility.models import Solicitudes, Vehiculos, Conductores
from movility.serializers import *
from movility.utils.VroomRequest import VroomRequest
import requests

# def name_to_coordinates(search_string, alldata=False): # TODO do this in Front-end
#     from OSMPythonTools.nominatim import Nominatim
#     nominatim = Nominatim()
#     response = nominatim.query(search_string).toJSON() # json["matches_number"]["info_parameter"]
#     if (alldata): return response
#     else: return str(response[0]["lat"]) + ", " + str(response[0]["lon"])


def generate_vroom_request(): #TODO
    
    # get all instances of Solicitudes, Vehiculos and Conductores in the DB
    reqs = Solicitudes.objects.all()
    buses = Vehiculos.objects.all()
    # drivers = Conductores.objects.all()
    
    vroom_request = VroomRequest()
    
    # get all "paradas" in all Solicitudes instances;
    for req in reqs.iterator():
        vroom_request.add_shipment(req.id, req.origen, req.destino, amount=1)  # TODO?: origen y destino -> [lon, lat]

    # get all buses in Vehiculos instances
    for bus in buses.iterator():
        vroom_request.add_vehicle(bus.matricula)

    return vroom_request


def process_vroom_routing(request):
    response = request.get_response()
    vroom_response_processor = VroomResponseProcessor(request)



def vroom_call():

    # Generates a Vroom request Object and fills it with th DB data
    request = generate_vroom_request()

    # Process the Vroom response  and updates the DB with the data obtained
    process_vroom_routing(request)
