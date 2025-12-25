from rest_framework import generics
from departments.models import Department
from departments.serializers import DepartmentSerializer  # ensure serializer exists at departments.serializers
from admin_panel.permissions.is_admin_role import IsSuperAdminOrStaff
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Admin Panel - Department"], summary="Department CRUD (Admin)")
class AdminDepartmentListCreate(generics.ListCreateAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

@extend_schema(tags=["Admin Panel - Department"], summary="Department RUD (Admin)")
class AdminDepartmentRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
