from django.urls import path
from .views import DepartmentListCreateView, DepartmentRUDView

urlpatterns = [
    path('', DepartmentListCreateView.as_view(), name='department-list'),
    path('<int:pk>/', DepartmentRUDView.as_view(), name='department-rud'),
]
