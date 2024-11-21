from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import handler403

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forbidden/', views.custom_permission_denied_view, name='forbidden'),
    path('dashboard/managers/', views.managers_dashboard, name='managers_dashboard'),
    path('dashboard/workers/', views.workers_dashboard, name='workers_dashboard'),
    path('dashboard/approvers/', views.approvers_dashboard, name='approvers_dashboard'),
    path('dashboard/create_task/', views.create_task, name='create_task'),
]

handler403 = views.custom_permission_denied_view