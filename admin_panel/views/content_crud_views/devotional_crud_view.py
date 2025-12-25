from rest_framework import generics
from contents.models.devotional import DailyDevotional
from contents.serializers.devotional_serializers import DailyDevotionalSerializer
from admin_panel.permissions.is_admin_role import IsSuperAdminOrStaff
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Admin Panel - Devotionals"], summary="Devotional list/create")
class AdminDevotionalListCreate(generics.ListCreateAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = DailyDevotional.objects.all().order_by("-created_at")
    serializer_class = DailyDevotionalSerializer

@extend_schema(tags=["Admin Panel - Devotionals"], summary="Devotional RUD")
class AdminDevotionalRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdminOrStaff]
    queryset = DailyDevotional.objects.all()
    serializer_class = DailyDevotionalSerializer
