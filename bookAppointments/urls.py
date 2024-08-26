from django.urls import path
from .views import book_appointment, fetch_appointments, delete_appointment, edit_appointment

urlpatterns = [
    path('book-appointment/', book_appointment, name='book_appointment'),
    path('fetch-appointments/<str:email>/', fetch_appointments, name='fetch_appointments'),
    path('delete-appointment/', delete_appointment, name='delete_appointment'),
    path('edit_appointment/', edit_appointment, name='edit_appointment'),
    

]

