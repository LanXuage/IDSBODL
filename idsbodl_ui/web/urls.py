from django.urls import path
from . import views


urlpatterns = [
  path('', views.index),
  path('nidsdatas', views.nidsdatas),
  # path('chapter/<int:chapter_id>', views.chapter),
]
