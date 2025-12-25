from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from contents.models.event import Event
from contents.serializers.event_serializers import EventSerializer
from admin_panel.permissions.is_admin_role import IsSuperAdminOrStaff


# ---------------------------------------------------------------------
# LIST & CREATE EVENTS
# ---------------------------------------------------------------------
@extend_schema(
    tags=["Admin Panel - Events"],
    summary="List & create events",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "event_date": {"type": "string", "format": "date"},
                "images": {
                    "type": "array",
                    "items": {"type": "string", "format": "binary"},
                },
                "videos": {
                    "type": "array",
                    "items": {"type": "string", "format": "binary"},
                },
            },
            "required": ["title", "event_date"],
        }
    },
    responses={201: EventSerializer},
)
class AdminEventListCreate(generics.ListCreateAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = Event.objects.all().order_by("-event_date")
    serializer_class = EventSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        event = Event.objects.create(
            title=request.data.get("title"),
            description=request.data.get("description"),
            event_date=request.data.get("event_date"),
        )

        for img in request.FILES.getlist("images"):
            event.images.create(image=img)

        for vid in request.FILES.getlist("videos"):
            event.videos.create(video=vid)

        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------------------------------------------------------------
# RETRIEVE / UPDATE / DELETE EVENT
# ---------------------------------------------------------------------
@extend_schema(
    tags=["Admin Panel - Events"],
    summary="Retrieve / update / delete event",
)
class AdminEventRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "event_date": {"type": "string", "format": "date"},
                    "images": {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    },
                    "videos": {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    },
                    "delete_image_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                    },
                    "delete_video_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                    },
                },
            }
        },
        responses={200: EventSerializer},
    )
    def patch(self, request, *args, **kwargs):
        event = self.get_object()

        # --------------------
        # Update core fields
        # --------------------
        event.title = request.data.get("title", event.title)
        event.description = request.data.get("description", event.description)
        event.event_date = request.data.get("event_date", event.event_date)
        event.save()

        # --------------------
        # Delete selected images
        # --------------------
        delete_image_ids = request.data.getlist("delete_image_ids") or []
        if delete_image_ids:
            images = event.images.filter(id__in=delete_image_ids)
            for img in images:
                img.image.delete(save=False)
                img.delete()

        # --------------------
        # Delete selected videos
        # --------------------
        delete_video_ids = request.data.getlist("delete_video_ids") or []
        if delete_video_ids:
            videos = event.videos.filter(id__in=delete_video_ids)
            for vid in videos:
                vid.video.delete(save=False)
                vid.delete()

        # --------------------
        # Add new images
        # --------------------
        for img in request.FILES.getlist("images"):
            event.images.create(image=img)

        # --------------------
        # Add new videos
        # --------------------
        for vid in request.FILES.getlist("videos"):
            event.videos.create(video=vid)

        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()

        for img in event.images.all():
            img.image.delete(save=False)
            img.delete()

        for vid in event.videos.all():
            vid.video.delete(save=False)
            vid.delete()

        event.delete()
        return Response(
            {"detail": "Event and media deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
