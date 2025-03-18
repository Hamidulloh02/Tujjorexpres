from django.urls import path
from . import views

urlpatterns = [
    path('code/', views.get_tracking_info, name='get_tracking_info'),
]
