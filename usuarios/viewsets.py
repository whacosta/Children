from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Nino
from rest_framework.views import APIView
from .serializers import *
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
class NinoViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated,]
    queryset = Nino.objects.all()
    serializer_class = NinoSerializer

class NinoAuth(APIView):
    def get(self, request, format=None):
        if not 'code' in request.query_params:
            raise ValidationError({"msg":"no se envió el parametro code"})
        code = request.query_params['code']
        nino = Nino.objects.filter(cod_apadr=code)
        if not nino.exists():
            raise ValidationError({"msg":{"El niño no existe"}})

        serializer = NinoSerializer(nino.first())
        return Response(serializer.data)