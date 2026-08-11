from care.emr.models.patient import Patient
from care.facility.models.facility import Facility
from care.utils.shortcuts import get_object_or_404

from django.db.models.signals import post_save
from django.dispatch import receiver

from care_people_be.extensions import PatientPrimaryFacilityExtension
from care_people_be.models.care_people import CarePeople


@receiver(post_save, sender=Patient)
def set_primary_facility(sender, instance, created, **kwargs):
    """Mirror the patient's primary_facility extension into CarePeople.

    Runs on create as well as update: the field is most often set at
    registration, and skipping creation left the table permanently empty.
    """
    namespace = PatientPrimaryFacilityExtension.extension_name
    facility = (instance.extensions or {}).get(namespace, {}).get(
        "primary_facility"
    )

    if not facility:
        CarePeople.objects.filter(patient=instance).delete()
        return

    facility = get_object_or_404(Facility, id=facility)

    CarePeople.objects.update_or_create(
        patient=instance, defaults={"facility": facility}
    )
