from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema, OpenApiExample

from contents.models.testimony import Testimony
from contents.serializers.testimony_serializers import TestimonySerializer
from django.shortcuts import get_object_or_404



class MemberTestimonySubmitView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        tags=["Members"],
        summary="Submit a testimony",
        description="Submit testimony with multiple images/videos.",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "images": {"type": "array", "items": {"type": "string", "format": "binary"}},
                    "videos": {"type": "array", "items": {"type": "string", "format": "binary"}},
                },
                "required": ["text"]
            }
        },
        responses={201: {"type": "object", "properties": {"message": {"type": "string"}}}}
    )
    def post(self, request):
        serializer = TestimonySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        testimony = serializer.save(member=request.user, status="pending")

        # Save images
        for img_file in request.FILES.getlist("images"):
            testimony.images.create(image=img_file)

        # Save videos
        for vid_file in request.FILES.getlist("videos"):
            testimony.videos.create(video=vid_file)

        return Response({"message": "Testimony submitted and awaiting approval"}, status=201)


class MyTestimonyListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Members"],
        summary="List my testimonies",
        responses={200: TestimonySerializer(many=True)},
    )
    def get(self, request):
        testimonies = Testimony.objects.filter(member=request.user).order_by("-created_at")
        serializer = TestimonySerializer(testimonies, many=True)
        return Response(serializer.data)



class MyTestimonyDetailView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, request, pk):
        return get_object_or_404(Testimony, pk=pk, member=request.user)

    @extend_schema(
        tags=["Members"],
        summary="Retrieve my testimony",
        responses={200: TestimonySerializer},
    )
    def get(self, request, pk):
        testimony = self.get_object(request, pk)
        serializer = TestimonySerializer(testimony)
        return Response(serializer.data)

    @extend_schema(
    tags=["Members"],
    summary="Update rejected/pending testimony",
    request=TestimonySerializer,
    responses={200: TestimonySerializer},
    )
    def patch(self, request, pk):
        testimony = self.get_object(request, pk)

        if testimony.status == "approved":
            return Response(
                {"detail": "Approved testimonies cannot be edited."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TestimonySerializer(
            testimony,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save(status="pending")  # 🔁 re-submit
            return Response(
                {"message": "Testimony updated and resubmitted for approval."}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        tags=["Members"],
        summary="Delete my testimony (not approved)",
    )
    def delete(self, request, pk):
        testimony = self.get_object(request, pk)

        if testimony.status == "approved":
            return Response(
                {"detail": "Approved testimonies cannot be deleted."},
                status=status.HTTP_403_FORBIDDEN
            )

        # delete files
        if testimony.image:
            testimony.image.delete(save=False)
        if testimony.video:
            testimony.video.delete(save=False)

        testimony.delete()
        return Response(
            {"message": "Testimony deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
