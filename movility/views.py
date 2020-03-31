from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import requests

from .models import Usuarios, Rutas, Solicitudes, Vehiculos
from .serializers import UsuariosSerializer, RutasSerializer, SolicitudesSerializer, VehiculosSerializer

from .utils import routes

"""""""""""""""""""""""""""
        Usuarios
"""""""""""""""""""""""""""
@api_view(['GET', 'POST'])
def usuarios_list(request, format=None):
    """
    Lista todos los usuarios, o crea un nuevo usuario.
    """
    if request.method == 'GET':
        usuarios = Usuarios.objects.all()
        serializer = UsuariosSerializer(usuarios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UsuariosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def usuarios_detail(request, pk, format=None):
    """
    Obtiene, actualiza o borra un usuario.
    """
    try:
        user = Usuarios.objects.get(pk=pk)
    except Usuarios.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsuariosSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UsuariosSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method=='GET':
        user=Usuarios.objects.get(id=id)
        serializer = UsuariosSerializer(user)
        return Response(serializer.data)


"""""""""""""""""""""""""""
        Rutas
"""""""""""""""""""""""""""
class RouteResponseView(APIView):
    def get(self, request, user_dni, origin, dest, departure_date, arrival_date):

        #TODO check if exists user dni

        # Names to coordinates
        origin_coords = routes.name_to_coordinates(origin, alldata=False)
        dest_coords = routes.name_to_coordinates(dest, alldata=False)

        # Create petition in bbdd
        petition_data {
            #TODO id de la solicitud?¿? autogenerada en la bbdd en teoria
            "origen":origin_coords,
            "destino":dest_coords,
            "fechaHoraSalida":departure_date, #TODO date formate
            "fechaHoraLlegada":arrival_date,
            "estado": #TODO ¿?¿?
            "idUsuario":user_dni
        }



"""""""""""""""""""""""""""
        Vehiculos
"""""""""""""""""""""""""""
@api_view(['GET', 'POST'])
def vehiculos_list(request, format=None):
    """
    Lista todos los usuarios, o crea un nuevo usuario.
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
    Obtiene, actualiza o borra un usuario.
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

    if request.method=='GET':
        vehiculo=Vehiculos.objects.get(id=id)
        serializer = VehiculosSerializer(vehiculo)
        return Response(serializer.data)


"""""""""""""""""""""""""""
        Solicitudes
"""""""""""""""""""""""""""
@api_view(['GET', 'POST'])
def solicitudes_list(request, format=None):
    """
    Lista todos los usuarios, o crea un nuevo usuario.
    """
    if request.method == 'GET':
        solicitudes = Solicitudes.objects.all()
        serializer = SolicitudesSerializer(solicitudes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SolicitudesSerializer(data=request.data)
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

    if request.method=='GET':
        solicitud=Solicitudes.objects.get(id=id)
        serializer = SolicitudesSerializer(solicitud)
        return Response(serializer.data)