from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate-report/', views.generate_report, name='generate_report'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('time-analysis/', views.time_analysis_view, name='time_analysis'),
]
