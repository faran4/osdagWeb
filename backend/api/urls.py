from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', HelloWorld.as_view(), name='hello'),
    path('bolt-diameters/', BoltDiameterAPIView.as_view(), name='bolt-diameters-api'),
    path('materials/', MaterialAPIView.as_view(), name='materials-api'),
    path('beams/', BeamAPIView.as_view(), name='beam-list'),
    path("submit-design/", SubmitDesignDataAPIView.as_view(), name="submit-design"),
]

