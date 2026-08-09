from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from members.models import Member
from departments.models import Department
from contents.models import DailyDevotional, Testimony, Event, Sermon

class DashboardView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @extend_schema(tags=['Admin Panel'], summary='Dashboard stats')
    def get(self, request):
        data = {
            'members_count': Member.objects.count(),
            'departments_count': Department.objects.count(),
            'devotionals_count': DailyDevotional.objects.count(),
            'pending_testimonies': Testimony.objects.filter(status='pending').count(),
            'events_count': Event.objects.count(),
            'sermons_count': Sermon.objects.count(),
        }
        return Response(data, status=status.HTTP_200_OK)
