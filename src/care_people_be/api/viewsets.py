from uuid import UUID

from django_filters import rest_framework as filters
from rest_framework.filters import TagFilter, OrderingFilter
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
from care.emr.tagging.base import SingleFacilityTagManager


class CarePeopleTagFilter(TagFilter):
    def filter_queryset(self, request, queryset, view):
        tags = request.query_params.get("tags", "").strip()
        tags_behavior = request.query_params.get("tags_behavior", "any")
        if not tags:
            return queryset
        tag_uuids = []
        for tag in tags.split(","):
            try:
                tag_uuids.append(UUID(tag))
            except ValueError:
                continue
        manager = SingleFacilityTagManager()
        tag_ids = []
        for tag_uuid in tag_uuids:
            tag_obj = manager.get_tag_from_external_id(tag_uuid)
            if tag_obj:
                tag_ids.append(tag_obj.id)
        if not tag_ids:
            return queryset.none()
        if tags_behavior == "all":
            return queryset.filter(patient__tags__contains=tag_ids)
        return queryset.filter(patient__tags__overlap=tag_ids)


class CarePeopleFilters(filters.FilterSet):
    facility = filters.CharFilter(field_name="facility__external_id")
    patient = filters.CharFilter(field_name="patient__external_id")


    class Meta:
        model = CarePeople
        fields = ["facility", "patient"]

class CarePeopleViewSet(
    EMRBaseViewSet,
    EMRListMixin,
    EMRRetrieveMixin):
    database_model = CarePeople
    pydantic_read_model = CarePeopleListSpec
    pydantic_retrieve_model = CarePeopleRetrieveSpec
    filter_backends = [filters.DjangoFilterBackend, CarePeopleTagFilter, OrderingFilter]
    filterset_class = CarePeopleFilters
    ordering_fields = ["created_date", "modified_date"]


    def authorize_retrieve(self, model_instance):
        patient = model_instance.patient
        if not AuthorizationController.call(
            "can_view_patient_obj", self.request.user, patient
        ):
            raise PermissionDenied("You do not have permission to view this patient")  # Add this line to handle unauthorized access

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


