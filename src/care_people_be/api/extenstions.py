from care.emr.extensions.base import PlugExtension, ExtensionResource
from care.emr.registries.extensions.registry import ExtensionRegistry
from care.utils.shortcuts import get_object_or_404
from care.facility.models.facility import Facility

class PatientPrimaryFacilityExtension(PlugExtension):
    name = "primary_facility"
    description = "Extension to store primary facility for a patient."
    version = "1.0.0"
    resource_type = ExtensionResource.patient

    write_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Patient Primary Facility",
        "type": "string",
        "format": "uuid",
    }

    @staticmethod
    def validate_facility(data,resource):
        facility=data.get("primary_facility")
        facility = get_object_or_404(Facility, external_id=facility)
        data["primary_facility"] = facility.id
        return data

    def serialize_extensions(self, data,resource):
            return self.validate_facility(data, resource)

ExtensionRegistry.register_extension(PatientPrimaryFacilityExtension)


