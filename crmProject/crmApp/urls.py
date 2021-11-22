from django.urls import path
from crmApp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('clients/', views.ClientList.as_view()),
    path('clients/<int:pk>/', views.ClientDetail.as_view()),

    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),

    path('goods/', views.GoodList.as_view()),
    path('goods/<int:pk>/', views.GoodDetail.as_view()),

    path('statuses/', views.StatusList.as_view()),
    path('statuses/<int:pk>/', views.StatusDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)