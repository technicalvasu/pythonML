from django.urls import path
from . import views
from .views import PredictionAPI

urlpatterns=[
    path('predict',PredictionAPI.as_view(),name='predict')
]