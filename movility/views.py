from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from OSMPythonTools.nominatim import Nominatim
import requests

from .models import Usuarios, Rutas, Solicitudes, Vehiculos
from .serializers import UsuariosSerializer, RutasSerializer, SolicitudesSerializer, VehiculosSerializer

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
    def get(self, request, origin, dest):

        #geometry = "mtx`Gbmet@~@EJA?B@DBDB@B@BABABE@C?GR?lCKZAAaAEyCCcB?IAo@?QASMyHA[Im@Ki@GOGQEMq@sA[m@OQBI?IAICGEEGCG?[s@Yu@wA{Cw@uAa@q@DMBMAMAMJ[HQh@sA`@g@l@oAX}@Pu@Fe@?e@A[Ie@Qa@W]UU]Qg@[_B{@{As@uB}@m@EmAm@}@e@g@a@w@k@_@[a@_@[[[Km@y@aAcBs@uAc@gAsBcG]}@Uc@o@aAkA_BsAuBm@qAi@kA[_Ak@{Ak@iAg@s@g@k@y@s@aBuAcAeAkBgCa@s@Uc@aAoBk@eBg@iBYkAW{AUiBMkBe@}Gw@qFi@yAo@uA{AuC{G_H}DgDo@o@q@w@m@}@iAsBe@kA_@mAmBsG]_Ao@wAgAkByBoD}@wBk@uBs@uCo@cBeA_B{AiAqAm@yAg@qAw@gAaA_AqAoAgBgCcDoAaBiBcCsByBwDmDQOoAoAe@k@aA}Ao@kA_A{BeCqFqBsCoAqAqAaA}AaAcBu@iBg@mBYqBGoBJw@JiB`@eBp@_B~@yBjBgBhAeAj@mA`@s@LaAN}@DgBE{ASeAYWKSGa@QYQ]Ue@a@{@s@kAwAoBqDIQMSKSMWOUMUOUMSSWOSOSQQMMMMMMOMWSOMSMOIUOWMSIQIQGMEMEOCOESCWESCUC]E_@Es@IQCOASCOAcAG{AKkHg@gAIgk@}CSC]IYGYGe@M[M[Oc@UUOMIKGQOMKMMQQQQOOOQYWk@o@WWKMOMMMOMIIIIGGIGGEQMMIMISIQKQG[MUIQESESEQESCWCUCSCUASAQ?QAU?Q@U@S@S@SBSBSDQDe@JSDQFSHQFOFSJQHWNQHOJQNQJOLOLQNMLMLKJQPQRQVQRQVQVg@t@SXKLILIJKJKJKLMLEBKJYTMJMJo@d@iBbAuEnBmBbAiBjAiBxAcB|AcFvFsAjAiAx@_Af@}Al@oBf@_BVyCJaBIkBMgBWkE_AsCw@kBq@aEuBsA}@kBuAmByAs@o@oCsCsCgD{AgBgDsCyCeBoDsBo@a@yAu@eBcBuA{Ai@u@mAuBgAwB{@yBsAeEmAcCe@}@mAoByAgBaByAs@i@mBgAiFyBqBcAmBoA_D}BkBmAqB_A{@Y{@S}@O}BQ_AA}BF}@J_ANyBj@yDlA{Bj@}B`@aAH_CF_CG_AG_AM{Bg@yBs@y@_@w@a@qGeEoBeAuBs@{@SyBY}BE}BJ_Gn@aCNaCBaCGaAG}B]{Bi@yBs@uBaAsBkAoBwAgB_BcBkBqCgDeBkBkBcBoByAuBkAwBaA{Bu@_ASyBa@wBUwBKwB?yBHgFZqBDsBCqBMqBYaDs@}DcBmBcAuHgEaCoAeB}@{By@uAe@eB]_F_AmDe@gDYyDKqC?kEL_DVyEn@mB`@qCr@q@RsAb@gDrAoB|@wGfDgD~AkDrAmDfAwBf@yB^yBXyBRuF^wBX{@NuBj@y@XoB|@iBjAeBtA}A`BuAhBmAlBmDbHiArBg@t@sAhBm@p@aBzAiBpAoBdAw@ZuBp@y@PqB\\qGp@}Cf@eBd@gBl@eBx@sCbBmCrB{D~CsChBeB|@_DnAmBh@cDp@mD^qCJyA?oAEkBGiBQyDy@mB}@w@a@_Am@c@e@Sq@?_ALu@\\a@^Oh@Db@V^r@Nd@~AdEH^XzAVrAL|@Z`DJpAFtAB`CAdEM`DUvC_@xCi@rCg@vBk@nBcAlCq@tAWj@c@r@i@z@g@h@[Vo@b@k@Zo@b@YV]`@[b@Wh@Ul@YbAWhAQl@M\\IVKNMTONUNa@HO?OEMMY[k@o@cAcA}BwBaEyDq@o@]o@Yo@Wu@]sAQ_AS}AcCmRCOCQASCU?QAQCy@AOAOCWCQCSeAsD_AoCy@aBMWk@y@g@o@_@a@c@e@WWFMlAqDBGDMa@q@iBsCWa@g@u@Ua@o@aAk@{@}AcCOUa@o@ACMQBG@IAGAGCGECDODMJm@Fm@@g@DgABu@?MDuAF_CJa@PWF@HAFCFGBIBI?KAKCIEGEEIQMMEWC]AY?]Ba@@e@"

        #TODO backend services
        nominatim = Nominatim()
        origen = nominatim.query(origin).toJSON()
        destino = nominatim.query(dest).toJSON()

        URL = "http://127.0.0.1:5000/route/v1/driving/" + \
              str(origen[0]["lon"]) + "," + str(origen[0]["lat"]) + ";" + \
              str(destino[0]["lon"]) + "," + str(destino[0]["lat"]) + "?" + \
              "overview=full"

        r = requests.get(URL)
        retorno_osrm = r.json()
        geometry = retorno_osrm["routes"][0]["geometry"]

        return Response(
            {
                "polyline":geometry
            }
        )


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