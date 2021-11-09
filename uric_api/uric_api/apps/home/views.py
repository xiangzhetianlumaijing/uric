from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import DatabaseError

# Create your views here.


class TestAPIView(APIView):
    def get(self, request):
        raise DatabaseError("xxxxx")
        return Response({"message": "hello"},)

