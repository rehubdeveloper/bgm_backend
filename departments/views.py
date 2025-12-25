from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema

from .models import Department
from .serializers import DepartmentSerializer


@extend_schema(
    tags=["Departments"],
    summary="List all departments",
    description="Public endpoint to list all church departments.",
)
class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    tags=["Departments"],
    summary="Retrieve department details",
)
class DepartmentDetailView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]
