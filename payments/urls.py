from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create/<int:booking_id>/', views.payment_create, name='create'),
    path('callback/<str:transaction_id>/', views.payment_callback, name='callback'),
    path('history/', views.payment_history, name='history'),
    path('refund-request/<int:payment_id>/', views.refund_request, name='refund_request'),
]
