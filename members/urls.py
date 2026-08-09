from django.urls import path
from .views import MemberListCreateView, MemberRUDView

urlpatterns = [
    path('', MemberListCreateView.as_view(), name='members-list'),
    path('<int:pk>/', MemberRUDView.as_view(), name='members-rud'),
]
