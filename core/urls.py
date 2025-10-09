from django.urls import path
from .views import can_spend, classify_text

urlpatterns = [
    path("api/can_spend/", can_spend, name="can_spend"),
    path("api/classify_text/", classify_text, name="classify_text"),
]
