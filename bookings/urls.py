from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:scooter_id>/', views.booking_create, name='create'),
    path('detail/<int:booking_id>/', views.booking_detail, name='detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.booking_cancel, name='cancel'),
]
