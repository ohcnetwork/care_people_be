from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404
from care_people_be.api.spec import CarePeopleListSpec, CarePeopleRetrieveSpec
from care_people_be.models.care_people import CarePeople
from care.emr.models.patient import Patient
from care.facility.models.facility import Facility
from care.security.authorization import AuthorizationController
from care.emr.api.viewsets.base import (
    EMRBaseViewSet,
    EMRListMixin,
    EMRTagMixin,
    EMRRetrieveMixin,
)
from rest_framework.exceptions import PermissionDenied, ValidationError
from care.emr.resources.tag.config_spec import TagResource
from care.emr.tagging.filters import SingleFacilityTagFilter
class CarePeopleFilters(filters.FilterSet):
    facility = filters.CharFilter(field_name="facility__external_id")
    patient = filters.CharFilter(field_name="patient__external_id")

    class Meta:
        model = CarePeople
        fields = ["facility", "patient"]

class CarePeopleViewSet(
    EMRBaseViewSet,
    EMRListMixin,
    EMRRetrieveMixin,
    EMRTagMixin,
):
    database_model = CarePeople
    pydantic_read_model = CarePeopleListSpec
    pydantic_retrieve_model = CarePeopleRetrieveSpec
    filter_backends = [filters.DjangoFilterBackend,OrderingFilter,SingleFacilityTagFilter]
    filterset_class = CarePeopleFilters
    ordering_fields = ["created_date", "modified_date"]
    resource_type = TagResource.patient



    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("patient", "facility")
        )
        if self.action in ["list"] and "facility" in self.request.GET and self.request.GET["facility"]:
            facility = get_object_or_404(
                Facility, external_id=self.request.GET["facility"]
            )
            qs = qs.filter(facility=facility)
        return qs


