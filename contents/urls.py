from django.urls import path
from .views import AboutListCreateView, DevotionalListCreateView, TestimonySubmitView, EventListCreateView, SermonListCreateView

urlpatterns = [
    path('about/', AboutListCreateView.as_view(), name='about-list'),
    path('devotionals/', DevotionalListCreateView.as_view(), name='devotional-list'),
    path('testimonies/submit/', TestimonySubmitView.as_view(), name='testimony-submit'),
    path('events/', EventListCreateView.as_view(), name='event-list'),
    path('sermons/', SermonListCreateView.as_view(), name='sermon-list'),
]
