from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from contents.models.about import About
from contents.serializers.about_serializers import AboutSerializer
from admin_panel.permissions.is_admin_role import IsSuperAdminOrStaff


# ---------------------------------------------------------------------
# LIST & CREATE ABOUT
# ---------------------------------------------------------------------
@extend_schema(
    tags=["Admin Panel - About"],
    summary="List & create about content",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["church", "pastor"]},
                "title": {"type": "string"},
                "content": {"type": "string"},
                "images": {
                    "type": "array",
                    "items": {"type": "string", "format": "binary"},
                },
            },
            "required": ["type", "title", "content"],
        }
    },
    responses={201: AboutSerializer},
)
class AdminAboutListCreate(generics.ListCreateAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = About.objects.all().order_by("-id")
    serializer_class = AboutSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        about = About.objects.create(
            type=request.data.get("type"),
            title=request.data.get("title"),
            content=request.data.get("content"),
        )

        for img in request.FILES.getlist("images"):
            about.images.create(image=img)

        serializer = AboutSerializer(about)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------------------------------------------------------------
# RETRIEVE / UPDATE / DELETE ABOUT
# ---------------------------------------------------------------------
@extend_schema(
    tags=["Admin Panel - About"],
    summary="Retrieve / update / delete about content",
)
class AdminAboutRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["church", "pastor"]},
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                    "images": {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    },
                    "delete_image_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "IDs of images to delete",
                    },
                },
            }
        },
        responses={200: AboutSerializer},
    )
    def patch(self, request, *args, **kwargs):
        about = self.get_object()

        # --------------------
        # Update core fields
        # --------------------
        about.type = request.data.get("type", about.type)
        about.title = request.data.get("title", about.title)
        about.content = request.data.get("content", about.content)
        about.save()

        # --------------------
        # Delete selected images
        # --------------------
        delete_image_ids = request.data.getlist("delete_image_ids") or []
        if delete_image_ids:
            images = about.images.filter(id__in=delete_image_ids)
            for img in images:
                img.image.delete(save=False)
                img.delete()

        # --------------------
        # Add new images
        # --------------------
        for img in request.FILES.getlist("images"):
            about.images.create(image=img)

        serializer = AboutSerializer(about)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        about = self.get_object()

        for img in about.images.all():
            img.image.delete(save=False)
            img.delete()

        about.delete()
        return Response(
            {"detail": "About content and images deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
