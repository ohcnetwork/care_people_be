from django.conf import settings
from django.shortcuts import HttpResponse
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from care_people_be.api.viewsets import CarePeopleViewSet


def healthy(request):
    return HttpResponse("OK")


router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register(r"", CarePeopleViewSet, basename="care_people_be")

urlpatterns = [
    path("health", healthy),
] + router.urls
