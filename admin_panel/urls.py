from django.urls import path

from admin_panel.views.member_crud_view import AdminMemberList, AdminMemberRUD
from admin_panel.views.department_crud_view import AdminDepartmentListCreate, AdminDepartmentRUD
from admin_panel.views.content_crud_views.devotional_crud_view import AdminDevotionalListCreate, AdminDevotionalRUD
from admin_panel.views.content_crud_views.testimony_crud_view import AdminTestimonyList, AdminTestimonyRUD, ApproveTestimonyView, RejectTestimonyView, AdminTestimonyCreate
from admin_panel.views.content_crud_views.sermon_crud_view import AdminSermonListCreate, AdminSermonRUD

from admin_panel.views.content_crud_views.about_crud_view import AdminAboutListCreate, AdminAboutRUD
from admin_panel.views.content_crud_views.event_crud_view import AdminEventListCreate, AdminEventRUD


urlpatterns = [


    #Members
    path("members/", AdminMemberList.as_view(), name="admin-member-list"),
    path("members/<int:pk>/", AdminMemberRUD.as_view(), name="admin-member-rud"),

    path("departments/", AdminDepartmentListCreate.as_view(), name="admin-dept-list"),
    path("departments/<int:pk>/", AdminDepartmentRUD.as_view(), name="admin-dept-rud"),

    # Devotionals
    path("devotionals/", AdminDevotionalListCreate.as_view(), name="admin-devotional-list"),
    path("devotionals/<int:pk>/", AdminDevotionalRUD.as_view(), name="admin-devotional-rud"),

    # Testimonies
    path("testimonies/", AdminTestimonyList.as_view(), name="admin-testimony-list"),
    path("testimonies/create/", AdminTestimonyCreate.as_view(), name="admin-testimony-create"),
    path("testimonies/<int:pk>/", AdminTestimonyRUD.as_view(), name="admin-testimony-rud"),
    path("testimonies/<int:pk>/approve/", ApproveTestimonyView.as_view(), name="admin-testimony-approve"),
    path("testimonies/<int:pk>/reject/", RejectTestimonyView.as_view(), name="admin-testimony-reject"),


    #Sermons
    path("sermons/", AdminSermonListCreate.as_view(), name="admin-sermon-list"),
    path("sermons/<int:pk>/", AdminSermonRUD.as_view(), name="admin-sermon-rud"),

    # About
    path("about/", AdminAboutListCreate.as_view(), name="admin-about-list"),
    path("about/<int:pk>/", AdminAboutRUD.as_view(), name="admin-about-rud"),

    # Events
    path("events/", AdminEventListCreate.as_view(), name="admin-event-list"),
    path("events/<int:pk>/", AdminEventRUD.as_view(), name="admin-event-rud"),
]


# Sermons


