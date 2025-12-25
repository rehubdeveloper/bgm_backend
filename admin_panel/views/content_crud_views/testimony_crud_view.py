from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from admin_panel.permissions.is_admin_role import IsSuperAdminOrStaff
from contents.models.testimony import Testimony
from contents.serializers.testimony_serializers import TestimonySerializer
from admin_panel.serializers.testimony_admin_serializer import AdminTestimonySerializer
from admin_panel.serializers.testimony_reject_serializer import RejectTestimonySerializer

# ---------------------------------------------------------------------
# LIST & MANAGE TESTIMONIES
# ---------------------------------------------------------------------
@extend_schema(tags=["Admin Panel - Testimonies"], summary="List & manage testimonies")
class AdminTestimonyList(generics.ListAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = Testimony.objects.all().order_by("-created_at")
    serializer_class = AdminTestimonySerializer


# ---------------------------------------------------------------------
# RETRIEVE / UPDATE / DELETE TESTIMONY
# ---------------------------------------------------------------------
@extend_schema(tags=["Admin Panel - Testimonies"], summary="Retrieve / Update / Delete testimony")
class AdminTestimonyRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = Testimony.objects.all()
    serializer_class = AdminTestimonySerializer

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "images": {"type": "array", "items": {"type": "string", "format": "binary"}},
                    "videos": {"type": "array", "items": {"type": "string", "format": "binary"}},
                    "delete_image_ids": {"type": "array", "items": {"type": "integer"}},
                    "delete_video_ids": {"type": "array", "items": {"type": "integer"}},
                },
            }
        },
        responses={200: AdminTestimonySerializer}
    )
    def patch(self, request, *args, **kwargs):
        testimony = self.get_object()

        if testimony.status == "approved":
            return Response({"detail": "Approved testimonies cannot be edited."}, status=403)

        # Update text
        testimony.text = request.data.get("text", testimony.text)
        testimony.save()

        # Delete selected images/videos
        delete_image_ids = request.data.getlist("delete_image_ids") or []
        if delete_image_ids:
            testimony.images.filter(id__in=delete_image_ids).delete()

        delete_video_ids = request.data.getlist("delete_video_ids") or []
        if delete_video_ids:
            testimony.videos.filter(id__in=delete_video_ids).delete()

        # Add new images/videos
        for img_file in request.FILES.getlist("images"):
            testimony.images.create(image=img_file)
        for vid_file in request.FILES.getlist("videos"):
            testimony.videos.create(video=vid_file)

        serializer = AdminTestimonySerializer(testimony)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        testimony = self.get_object()

        # Delete all images/videos
        for img in testimony.images.all():
            img.image.delete(save=False)
            img.delete()
        for vid in testimony.videos.all():
            vid.video.delete(save=False)
            vid.delete()

        testimony.delete()
        return Response(
            {"detail": "Testimony and media deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# ---------------------------------------------------------------------
# APPROVE TESTIMONY
# ---------------------------------------------------------------------
@extend_schema(tags=["Admin Panel - Testimonies"], summary="Approve a testimony")
class ApproveTestimonyView(APIView):
    permission_classes = [IsSuperAdminOrStaff]

    def post(self, request, pk: int):
        try:
            testimony = Testimony.objects.get(pk=pk)
        except Testimony.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        if testimony.status != "pending":
            return Response({"error": f"Testimony is already {testimony.status}"}, status=400)

        testimony.status = "approved"
        testimony.rejection_reason = None
        testimony.save()  # Signal triggers notification

        serializer = AdminTestimonySerializer(testimony)
        return Response(serializer.data, status=200)


# ---------------------------------------------------------------------
# REJECT TESTIMONY
# ---------------------------------------------------------------------
@extend_schema(
    tags=["Admin Panel - Testimonies"],
    summary="Reject a testimony with reason",
    request=RejectTestimonySerializer,
    responses={200: AdminTestimonySerializer}
)
class RejectTestimonyView(APIView):
    permission_classes = [IsSuperAdminOrStaff]

    def post(self, request, pk: int):
        try:
            testimony = Testimony.objects.get(pk=pk)
        except Testimony.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        if testimony.status == "approved":
            return Response({"error": "Cannot reject an approved testimony"}, status=400)

        serializer = RejectTestimonySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reason = serializer.validated_data["rejection_reason"]

        testimony.status = "rejected"
        testimony.rejection_reason = reason
        testimony.save()  # Signal triggers notification

        response_serializer = AdminTestimonySerializer(testimony)
        return Response(response_serializer.data, status=200)
