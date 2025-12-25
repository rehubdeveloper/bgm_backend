from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema
from contents.models.testimony import Testimony
from contents.serializers.testimony_serializers import TestimonySerializer


class ApprovedTestimonyListView(APIView):
    """
    Public endpoint: List ONLY approved testimonies
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Testimonies"],
        summary="List approved testimonies",
        description="Returns only testimonies approved by the admin.",
        responses=TestimonySerializer(many=True),
    )
    def get(self, request):
        testimonies = (
            Testimony.objects
            .filter(status="approved")
            .order_by("-created_at")
        )
        serializer = TestimonySerializer(testimonies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApprovedTestimonyDetailView(APIView):
    """
    Public endpoint: Retrieve ONE approved testimony
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Testimonies"],
        summary="Retrieve approved testimony details",
        responses={200: TestimonySerializer},
    )
    def get(self, request, pk):
        testimony = get_object_or_404(
            Testimony,
            pk=pk,
            status="approved"
        )
        serializer = TestimonySerializer(testimony)
        return Response(serializer.data, status=status.HTTP_200_OK)
