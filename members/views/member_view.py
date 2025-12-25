from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from members.serializers.member_serializer import MemberSerializer


@extend_schema(
    tags=["Members"],
    summary="Register as a member",
    request=MemberSerializer,
    responses={201: MemberSerializer},
)
class MemberRegisterView(APIView):
    """
    Public registration endpoint
    """

    def post(self, request):
        serializer = MemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["Members"],
    summary="Get my profile",
    responses={200: MemberSerializer},
)
class MyProfileView(APIView):
    """
    Authenticated members can view their own profile
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MemberSerializer(request.user)
        return Response(serializer.data)


@extend_schema(
    tags=["Members"],
    summary="Update my profile",
    request=MemberSerializer,
    responses={200: MemberSerializer},
)
class UpdateMyProfileView(APIView):
    """
    Authenticated members can update their own profile
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = MemberSerializer(
            request.user,
            data=request.data,
            partial=False
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        serializer = MemberSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
