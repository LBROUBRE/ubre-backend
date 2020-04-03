
def name_to_coordinates(search_string, alldata=False):
    from OSMPythonTools.nominatim import Nominatim
    nominatim = Nominatim()
    response = nominatim.query(search_string).toJSON() # json["matches_number"]["info_parameter"]
    if (alldata): return response
    else: return str(response[0]["lat"]) + ", " + str(response[0]["lon"])

def generate_route_from_dbrequests(): #TODO

    # import all dependencies
    from django.core import serializers
    from datetime import datetime
    from movility.models import Solicitudes, Vehiculos, Conductores
    from movility.serializers import ConductoresSerializer, RutasSerializer, SolicitudesSerializer, VehiculosSerializer
    
    # get all instances of Solicitudes, Vehiculos and Conductores in the DB
    requests = Solicitudes.objects.all()
    buses = Vehiculos.objects.all()
    drivers = Conductores.objects.all()

    # define 2 functions to update the "state" in db instances and to create a new instance
    def update_db_value(serializerType, instance, key, value):
        new_data = serializerType(instance).data
        new_data[key]=value
        update_serializer = serializerType(instance, data=new_data)
        if update_serializer.is_valid():
            update_serializer.save()
    
    def create_db_instance(serializerType, data):
        serializer = serializerType(data=data)
        if serializer.is_valid():
            serializer.save()
    
    # get all "paradas" in all Solicitudes instances; update their states to "en_curso"
    route_stops = []
    for req in requests.iterator():
        update_db_value(SolicitudesSerializer, req, "state", "en_curso")
        route_stops.append(req.paradas)

    # get the first free bus in Vehiculos instances; update its state to "driving"
    for bus in buses.iterator():
        if (bus.state == "free"):
            update_db_value(VehiculosSerializer, bus, "state", "driving")
            route_bus = bus

    # get the first free driver in Conductores instances; update his state to "driving"
    for drv in drivers.iterator(): 
        if (drv.free == True):
            update_db_value(ConductoresSerializer, drv, "state", "driving")
            route_driver = drv

    # create a new route with all these parameters
    new_route = {
        "origen":1,
        "destino":1,
        "fecha":datetime.now(),
        "vehiculo":route_bus.matricula,
        "paradas":route_stops,
        "conductor":route_driver.dni
    }

    # put the new route in DB
    create_db_instance(RutasSerializer, new_route)

    # return the new route data (json)
    return new_route