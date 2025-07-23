from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),

]
