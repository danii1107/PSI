from rest_framework.views import APIView
from rest_framework.response import Response 

class myclassView(APIView):
    def get(self, request):
        return Response({"message": "Got some data!"})