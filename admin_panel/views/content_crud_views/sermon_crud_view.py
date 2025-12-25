from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema

from contents.models.sermon import Sermon, SermonAudio
from contents.serializers.sermon_serializers import SermonSerializer
from admin_panel.permissions.is_admin_role import IsSuperAdminOrStaff


@extend_schema(
    tags=["Admin Panel - Sermons"],
    summary="Sermon list/create",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "preacher": {"type": "string"},
                "description": {"type": "string"},
                "audios": {
                    "type": "array",
                    "items": {"type": "string", "format": "binary"},
                    "description": "Upload one or more audio files",
                },
            },
            "required": ["title", "audios"],
        }
    },
    responses={201: SermonSerializer},
)
class AdminSermonListCreate(generics.ListCreateAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = Sermon.objects.all().order_by("-created_at")
    serializer_class = SermonSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        # Create sermon instance
        sermon = Sermon.objects.create(
            title=request.data.get("title"),
            preacher=request.data.get("preacher"),
            description=request.data.get("description")
        )

        # Attach audio files
        for audio_file in request.FILES.getlist("audios"):
            SermonAudio.objects.create(sermon=sermon, audio=audio_file)

        serializer = SermonSerializer(sermon)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Admin Panel - Sermons"], summary="Sermon retrieve/update/delete")
class AdminSermonRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = Sermon.objects.all()
    serializer_class = SermonSerializer
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "preacher": {"type": "string"},
                    "description": {"type": "string"},
                    "audios": {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                        "description": "Upload one or more audio files",
                    },
                    "delete_audio_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "IDs of existing audio files to delete",
                    },
                },
            }
        },
        responses={200: SermonSerializer},
    )
    def patch(self, request, *args, **kwargs):
        """
        Partially update a sermon and manage its audio files.
        """
        sermon = self.get_object()

        # Update basic fields
        sermon.title = request.data.get("title", sermon.title)
        sermon.preacher = request.data.get("preacher", sermon.preacher)
        sermon.description = request.data.get("description", sermon.description)
        sermon.save()

        # Delete selected audios (also remove files from storage)
        delete_audio_ids = request.data.getlist("delete_audio_ids") or []
        if delete_audio_ids:
            audios_to_delete = SermonAudio.objects.filter(id__in=delete_audio_ids, sermon=sermon)
            for audio in audios_to_delete:
                if audio.audio:
                    audio.audio.delete(save=False)
                audio.delete()

        # Add new audios
        for audio_file in request.FILES.getlist("audios"):
            SermonAudio.objects.create(sermon=sermon, audio=audio_file)

        serializer = SermonSerializer(sermon)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a sermon and all its associated audio files.
        """
        sermon = self.get_object()
        for audio in sermon.audios.all():
            if audio.audio:
                audio.audio.delete(save=False)
            audio.delete()

        sermon.delete()
        return Response(
            {"detail": "Sermon and all audios deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
