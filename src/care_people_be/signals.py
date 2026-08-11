from django.db.models.signals import post_save
from django.dispatch import receiver
from care.utils.shortcuts import get_object_or_404
from care.facility.models.facility import Facility
from care.emr.models.patient import Patient
from care_people_be.models.care_people import CarePeople


@receiver(post_save, sender=Patient)
def set_primary_facility(sender, instance, created, **kwargs):
    if not created:
        if instance.extensions and instance.extensions.get("primary_facility"):
            facility = instance.extensions.get("primary_facility")
            facility = get_object_or_404(Facility, id=facility)
            CarePeople.objects.update_or_create(patient=instance, defaults={"facility": facility})





