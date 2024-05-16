from django.urls import path
from . import views

urlpatterns = [
    path('', views.poll_list),
    path('<int:pk>/', views.poll_detail),
    path('<int:pk>/agree/', views.agree),
    path('<int:pk>/disagree/', views.disagree),
    path('create/', views.poll_create),
]