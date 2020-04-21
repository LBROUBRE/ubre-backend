from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import requests
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from .models import *
from .serializers import *

from .utils import routes

"""""""""""""""""""""""""""
        Vehiculos
"""""""""""""""""""""""""""
@api_view(['GET', 'POST'])
def vehiculos_list(request, format=None):
    """
    Lista todos los vehiculos, o crea uno nuevo.
    """
    if request.method == 'GET':
        vehiculos = Vehiculos.objects.all()
        serializer = VehiculosSerializer(vehiculos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VehiculosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def vehiculos_detail(request, pk, format=None):
    """
    Obtiene, actualiza o borra un vehiculo.
    """
    try:
        vehiculo = Vehiculos.objects.get(pk=pk)
    except Vehiculos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VehiculosSerializer(vehiculo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VehiculosSerializer(vehiculo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vehiculo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""""""""""""""""""""""""""
        Solicitudes
"""""""""""""""""""""""""""
@api_view(['GET', 'POST'])
def solicitudes_list(request, format=None):
    """
    Lista todos las Solicitudes, o crea una nueva.
    """
    if request.method == 'GET':
        solicitudes = Solicitudes.objects.all()
        serializer = SolicitudesSerializer(solicitudes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST': #request = { usuario, origen, destino, fechaHoraSalida, fechaHoraLlegada }
        new_data = {
            "origen":request.data["origen"],
            "destino":request.data["destino"],
            "fechaHoraSalida":request.data["fechaHoraSalida"], #TODO date format
            "usuario":request.data["usuario"],
            "fechaHoraLlegada":request.data["fechaHoraLlegada"],
            "precio":5 #TODO
        }
        serializer = SolicitudesSerializer(data=new_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def solicitudes_detail(request, pk, format=None):
    """
    Obtiene, actualiza o borra un usuario.
    """
    try:
        solicitud = Solicitudes.objects.get(pk=pk)
    except Solicitudes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SolicitudesSerializer(solicitud)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SolicitudesSerializer(solicitud, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        solicitud.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def solicitudes_front(request, format=None):
    """
    Carga una nueva solicitud, calcular las rutas y devolver las rutas calculadas
    """
    new_data = {
        "origen": request.data["origen"],
        "destino": request.data["destino"],
        "fechaHoraSalida": request.data["fechaHoraSalida"],  # TODO date format
        "usuario": request.data["usuario"],
        "fechaHoraLlegada": request.data["fechaHoraLlegada"],
        "precio": 5  # TODO
    }
    serializer = SolicitudesSerializer(data=new_data)
    id = None
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        id = serializer.data["id"]
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    rutas = Rutas.objects.all()
    for ruta in rutas.iterator():
        ruta.delete()
    routes.vroom_call()

    steps = Steps.objects.all()

    for step in steps.iterator():
        if step.solicitudes.id == id:
            id_ruta = step.rutas.id
            ruta = Rutas.objects.get(pk=id_ruta)
            serializer = RutasSerializer(ruta)
            return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({}, status=status.HTTP_404_NOT_FOUND)



"""""""""""""""""""""""""""
        Conductores
"""""""""""""""""""""""""""
@api_view(['GET', 'POST'])
def conductores_list(request, format=None):
    """
    Lista todos los Conductores, o crea uno nuevo.
    """
    if request.method == 'GET':
        conductores = Rutas.objects.all()
        serializer = ConductoresSerializer(conductores, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ConductoresSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def conductores_detail(request, pk, format=None):
    """
    Obtiene, actualiza o borra un usuario.
    """
    try:
        conductores = Conductores.objects.get(pk=pk)
    except Conductores.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ConductoresSerializer(conductores)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ConductoresSerializer(conductores, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        conductores.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""""""""""""""""""""""""""
        Tarificación
"""""""""""""""""""""""""""
@api_view(['GET', 'POST'])
def tarificacion_list(request, format=None):
    """
    Lista toda la Tarificación, o crea uno nuevo.
    """
    if request.method == 'GET':
        tarificacion = Tarificacion.objects.all()
        serializer = TarificacionSerializer(tarificacion, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TarificacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def tarificacion_detail(request, pk, format=None):
    """
    Obtiene, actualiza o borra una tarifa.
    """
    try:
        tarificacion = Tarificacion.objects.get(pk=pk)
    except Tarificacion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TarificacionSerializer(tarificacion)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TarificacionSerializer(tarificacion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tarificacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""""""""""""""""""""""""""
        Virtual Stop
"""""""""""""""""""""""""""
@api_view(['GET', 'POST'])
def stops_list(request, format=None):
    """
    Lista todas las paradas virtuales, o crea una nuevo.
    """
    if request.method == 'GET':
        stops = ParadasVirtuales.objects.all()
        serializer = ParadasVirtualesSerializer(stops, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ParadasVirtualesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def stops_detail(request, pk, format=None):
    """
    Obtiene, actualiza o borra una parada virtual.
    """
    try:
        stops = ParadasVirtuales.objects.get(pk=pk)
    except ParadasVirtuales.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ParadasVirtualesSerializer(stops)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ParadasVirtualesSerializer(stops, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        stops.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""""""""""""""""""""""""""
        Rutas
"""""""""""""""""""""""""""
@api_view(['GET', 'POST'])
def rutas_list(request, format=None):
    """
    Lista todas las rutas, o crea uno nuevo.
    """
    if request.method == 'GET':
        rutas = Rutas.objects.all()
        serializer = RutasSerializer(rutas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RutasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def rutas_detail(request, pk, format=None):
    """
    Obtiene, actualiza o borra una ruta.
    """
    try:
        rutas = Rutas.objects.get(pk=pk)
    except Rutas.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RutasSerializer(rutas)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RutasSerializer(rutas, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        rutas.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def test_vroom(request): #TODO remove
    if request.method == 'GET':
        routes.vroom_call()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
