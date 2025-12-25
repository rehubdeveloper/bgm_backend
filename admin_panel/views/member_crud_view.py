from rest_framework import generics
from members.models.member import Member
from members.serializers.member_serializer import MemberSerializer
from admin_panel.permissions.is_admin_role import IsSuperAdminOrStaff
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Admin Panel - Members"], summary="Member CRUD (Admin)")
class AdminMemberList(generics.ListAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = Member.objects.all().order_by("-created_at")
    serializer_class = MemberSerializer

@extend_schema(tags=["Admin Panel - Members"], summary="Member RUD (Admin)")
class AdminMemberRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
