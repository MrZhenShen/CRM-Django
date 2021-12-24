from django.urls import path
from crmApp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),

    path('clients/', views.ClientList.as_view()),
    path('clients/<int:pk>/', views.ClientDetail.as_view()),

    path('projects/', views.ProjectList.as_view()),
    path('client-projects/<int:pk>/', views.ClientProjectList.as_view()),

    path('goods/', views.GoodList.as_view()),
    path('goods/<int:pk>/', views.GoodDetail.as_view()),

    path('statuses/', views.StatusList.as_view()),
    path('statuses/<int:pk>/', views.StatusDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)