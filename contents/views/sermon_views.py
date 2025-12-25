from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes, OpenApiParameter

from contents.models.sermon import Sermon
from contents.serializers.sermon_serializers import SermonSerializer

from rest_framework.permissions import IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404

class SermonListCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        tags=["Sermons"],
        summary="Get all sermons",
        responses=SermonSerializer(many=True),
    )
    def get(self, request):
        sermons = Sermon.objects.all().order_by("-created_at")
        serializer = SermonSerializer(sermons, many=True)
        return Response(serializer.data)

    


class SermonDetailView(APIView):

    @extend_schema(
        tags=["Sermons"],
        summary="Retrieve sermon details",
        responses={200: SermonSerializer},
    )
    def get(self, request, pk):
        sermon = get_object_or_404(Sermon, pk=pk)
        serializer = SermonSerializer(sermon)
        return Response(serializer.data)

