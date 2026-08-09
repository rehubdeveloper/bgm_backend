from django.urls import path
from django.http import JsonResponse

def ping(request):
    return JsonResponse({'ok': True, 'app': 'accounts'})

urlpatterns = [
    path('ping/', ping),
]
