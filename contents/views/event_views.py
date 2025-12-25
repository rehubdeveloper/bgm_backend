from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from contents.models.event import Event
from contents.serializers.event_serializers import EventSerializer


class EventListView(APIView):
    """
    Public endpoint: List all events (READ-ONLY)
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Events"],
        summary="Get all events",
        responses=EventSerializer(many=True),
    )
    def get(self, request):
        events = Event.objects.all().order_by("-event_date")
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventDetailView(APIView):
    """
    Public endpoint: Retrieve event details (READ-ONLY)
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Events"],
        summary="Retrieve event details",
        responses={200: EventSerializer},
    )
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
