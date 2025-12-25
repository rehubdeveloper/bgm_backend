from django.urls import path
from members.views.member_view import MemberRegisterView, MyProfileView, UpdateMyProfileView
from members.views.testimony_views import MemberTestimonySubmitView

from members.views.testimony_views import (
    MemberTestimonySubmitView,
    MyTestimonyListView,
    MyTestimonyDetailView,
)

urlpatterns = [
    path("", MemberRegisterView.as_view(), name="member-create"),
    path("me/", MyProfileView.as_view(), name="member-me"),
    path("me/update/", UpdateMyProfileView.as_view(), name="member-update"),

    path("testimonies/submit/", MemberTestimonySubmitView.as_view()),
    path("testimonies/", MyTestimonyListView.as_view()),
    path("testimonies/<int:pk>/", MyTestimonyDetailView.as_view()),
]