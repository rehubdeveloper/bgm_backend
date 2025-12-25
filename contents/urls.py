from django.urls import path

from contents.views.about_views import AboutListView, AboutDetailView
from contents.views.devotional_views import DevotionalListCreateView, DevotionalDetailView
from contents.views.event_views import EventListView,EventDetailView, EventDetailView
from contents.views.sermon_views import SermonListCreateView, SermonDetailView
from contents.views.testimony_views import ApprovedTestimonyListView, ApprovedTestimonyDetailView



urlpatterns = [
    # Events
    path("events/", EventListView.as_view(), name="event-list-create"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event-delete"),

    # Sermons
    path("sermons/", SermonListCreateView.as_view(), name="sermon-list-create"),
    path("sermons/<int:pk>/", SermonDetailView.as_view(), name="sermon-delete"),

    # TESTIMONIES
    path("testimonies/", ApprovedTestimonyListView.as_view(), name="testimony-submit"),
    path("testimonies/<int:pk>/", ApprovedTestimonyDetailView.as_view(), name="testimony-delete"),

    #About
    path("about/", AboutListView.as_view(), name="about-list-create"),
    path("about/<int:pk>/", AboutDetailView.as_view(), name="about-delete"),

    # Devotionals
    path("devotionals/", DevotionalListCreateView.as_view(), name="devotional-list-create"),
    path("devotionals/<int:pk>/", DevotionalDetailView.as_view(), name="devotional-delete"),
    
]
