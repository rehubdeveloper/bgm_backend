from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from contents.models.about import About
from contents.serializers.about_serializers import AboutSerializer


class AboutListView(APIView):
    """
    Public endpoint: Only GET. Anyone can view About sections.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["About"],
        summary="Get all About sections",
        description="Returns a list of all About sections (About Church and About Pastor).",
        responses=AboutSerializer(many=True),
    )
    def get(self, request):
        items = About.objects.all()
        serializer = AboutSerializer(items, many=True)
        return Response(serializer.data)


class AboutDetailView(APIView):
    """
    Public endpoint: Only GET for single About section.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["About"],
        summary="Retrieve About section",
        responses={200: AboutSerializer},
    )
    def get(self, request, pk):
        about = get_object_or_404(About, pk=pk)
        serializer = AboutSerializer(about)
        return Response(serializer.data)
