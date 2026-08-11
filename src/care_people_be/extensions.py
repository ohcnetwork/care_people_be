from care.emr.extensions.base import PlugExtension, ExtensionResource
from care.emr.registries.extensions.registry import ExtensionRegistry
from care.utils.shortcuts import get_object_or_404
from care.facility.models.facility import Facility

class PatientPrimaryFacilityExtension(PlugExtension):
    extension_name = "patient_primary_facility_extension"
    description = "Extension to store primary facility for a patient."
    extension_version = "1.0.0"
    resource_type = ExtensionResource.patient

    write_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Patient Details",
        "type": "object",
        "properties": {
            "primary_facility": {
                "type": "string",
                "format": "uuid",
                "title": "Primary Facility",
                "description": "Facility this patient primarily belongs to",
                "x-ui": {
                    "control": "autocomplete",
                    "render_blacklist": ["patient_summary", "appointment_print"],
                    "metadata": {
                        "url": "/api/v1/facility/",
                        "searchParam": "name",
                        "valueField": "id",
                        "labelField": "name",
                    },
                },
            },
        },
        "additionalProperties": False,
    }

    @staticmethod
    def validate_facility(data, resource=None):
        facility = data.get("primary_facility")
        if not facility:
            data.pop("primary_facility", None)
            return data
        facility = get_object_or_404(Facility, external_id=facility)
        data["primary_facility"] = str(facility.id)
        return data

    def serialize_extensions(self, data, resource=None):
        return self.validate_facility(data, resource)

    def deserialize_extensions_retrieve(self, data, resource):
        if data.get("primary_facility"):
            data["primary_facility"] = get_object_or_404(Facility, id=data["primary_facility"]).external_id
        return data

ExtensionRegistry.register(PatientPrimaryFacilityExtension())


