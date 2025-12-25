from django.urls import path
from messaging.views.send_message_view import SendMessageView
from messaging.views.list_logs_view import MessageLogListView
from messaging.views.resend_view import ResendMessageView

urlpatterns = [
    path("send/", SendMessageView.as_view(), name="messaging-send"),
    path("logs/", MessageLogListView.as_view(), name="messaging-logs"),
    path("resend/<int:log_id>/", ResendMessageView.as_view(), name="messaging-resend"),
]
