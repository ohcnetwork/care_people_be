from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from care_people_be.api.spec import CarePeopleListSpec, CarePeopleRetrieveSpec
from care_people_be.models.care_people import CarePeople
from care.emr.models.patient import Patient
from care.security.authorization import AuthorizationController
from care.emr.api.viewsets.base import (
    EMRBaseViewSet,
    EMRListMixin,
    EMRRetrieveMixin,
)

class CarePeopleFilters(filters.FilterSet):
    patient_id = filters.UUIDFilter(field_name="patient__external_id")
    facility_id = filters.UUIDFilter(field_name="facility__external_id")

class CarePeopleViewSet(
    EMRBaseViewSet,
    EMRListMixin,
    EMRRetrieveMixin,
):
    database_model = CarePeople
    pydantic_read_model = CarePeopleListSpec
    pydantic_retrieve_model = CarePeopleRetrieveSpec
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = CarePeopleFilters
    ordering_fields = ["created_date", "modified_date"]


    def get_queryset(self):
        allowed_patients = AuthorizationController.call(
            "get_filtered_patients", Patient.objects.all(), self.request.user
        )
        return (
            super()
            .get_queryset()
            .filter(patient__in=allowed_patients)
            .select_related("patient", "facility")
        )


