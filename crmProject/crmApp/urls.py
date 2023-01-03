from django.urls import path
from crmApp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("register/", views.RegisterView.as_view()),

    path('clients/<int:pk>/', views.ClientDetail.as_view()),

    path('projects/', views.ProjectList.as_view()),
    path('projects-client/<int:pk>/', views.ProjectClientList.as_view()),
    path('project-edit/<int:pk>/', views.ProjectEdit.as_view()),
    path('project-create/', views.ProjectCreate.as_view()),

    path('goods/', views.GoodList.as_view()),
    path('statuses/', views.StatusList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)