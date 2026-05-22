from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume_list, name='resume_list'),
    path('create/', views.resume_create, name='resume_create'),
    path('<int:pk>/', views.resume_detail, name='resume_detail'),
    path('<int:pk>/edit/', views.resume_update, name='resume_update'),
    path('<int:pk>/delete/', views.resume_delete, name='resume_delete'),
]
