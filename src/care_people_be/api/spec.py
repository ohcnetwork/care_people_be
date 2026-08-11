from care.emr.resources.base import EMRResource
from care_people_be.models.care_people import CarePeople
from pydantic import UUID4, Field, model_validator
from care.emr.resources.patient.spec import PatientListSpec, PatientRetrieveSpec
from care.emr.resources.facility.spec import FacilityBaseSpec

class CarePeopleListSpec(EMRResource):
    __model__ = CarePeople
    id:UUID4 | None = None
    patient: dict
    facility: dict

    def perform_extra_serialization(cls, mapping, obj, *args, **kwargs):
        if obj.patient:
            mapping["patient"] = PatientListSpec.serialize(obj.patient).to_json()
        if obj.facility:
            mapping["facility"] = FacilityBaseSpec.serialize(obj.facility).to_json()

class CarePeopleRetrieveSpec(CarePeopleListSpec):
    id:UUID4 | None = None
    patient: dict
    facility: dict

    def perform_extra_serialization(cls, mapping, obj, *args, **kwargs):
        if obj.patient:
            mapping["patient"] = PatientRetrieveSpec.serialize(obj.patient).to_json()
        if obj.facility:
            mapping["facility"] = FacilityBaseSpec.serialize(obj.facility).to_json()

