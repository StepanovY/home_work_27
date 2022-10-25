from django.urls import path

from ads.views.ad_views import *

urlpatterns = [
    path('', AdListView.as_view()),
    path('<int:pk>/', AdDetailView.as_view()),
    path('create/', AdCreateView.as_view()),
    path('<int:pk>/update/', AdUpdateView.as_view()),
    path('<int:pk>/delete/', AdDeleteView.as_view()),
    path('<int:pk>/image/', AdImageView.as_view()),
]
