from rest_framework import generics
from .models import About, DailyDevotional, Testimony, Event, Sermon
from .serializers import AboutSerializer, DailyDevotionalSerializer, TestimonySerializer, EventSerializer, SermonSerializer

class AboutListCreateView(generics.ListCreateAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

class DevotionalListCreateView(generics.ListCreateAPIView):
    queryset = DailyDevotional.objects.all().order_by('-created_at')
    serializer_class = DailyDevotionalSerializer

class TestimonySubmitView(generics.CreateAPIView):
    queryset = Testimony.objects.all()
    serializer_class = TestimonySerializer

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-event_date')
    serializer_class = EventSerializer

class SermonListCreateView(generics.ListCreateAPIView):
    queryset = Sermon.objects.all().order_by('-created_at')
    serializer_class = SermonSerializer
