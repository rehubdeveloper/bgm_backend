from rest_framework import generics, permissions
from .models import Member
from .serializers import MemberSerializer

class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all().order_by('-created_at')
    serializer_class = MemberSerializer
    permission_classes = [permissions.AllowAny]

class MemberRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.AllowAny]
