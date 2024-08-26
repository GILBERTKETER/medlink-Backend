from django.urls import path
from .views import set_reminder, get_reminders
urlpatterns = [
    path('set-timeline/', set_reminder, name="set_reminder"),
    path('get-timeline/<str:email>/', get_reminders, name="get_reminder")
]
