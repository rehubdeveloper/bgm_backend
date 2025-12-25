from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample
from contents.models.devotional import DailyDevotional
from contents.serializers.devotional_serializers import DailyDevotionalSerializer
from django.shortcuts import get_object_or_404


class DevotionalListCreateView(APIView):

    @extend_schema(
        tags=["Devotionals"],
        summary="Get all daily devotionals",
        responses=DailyDevotionalSerializer(many=True),
    )
    def get(self, request):
        devotionals = DailyDevotional.objects.all().order_by("-created_at")
        serializer = DailyDevotionalSerializer(devotionals, many=True)
        return Response(serializer.data)

    
class DevotionalDetailView(APIView):
    @extend_schema(
        tags=["Devotionals"],
        summary="Retrieve devotional details",
        responses={200: DailyDevotionalSerializer},
    )
    def get(self, request, pk):
        devotional = get_object_or_404(DailyDevotional, pk=pk)
        serializer = DailyDevotionalSerializer(devotional)
        return Response(serializer.data)


