from django.urls import path
from . import views

app_name = 'shortener'

urlpatterns = [
    path('<str:short_code>/', views.redirect_short_url, name='redirect'),
]
