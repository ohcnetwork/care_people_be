from django.db import models

from care.utils.models.base import BaseModel
from care.emr.models.patient import Patient
from care.facility.models.facility import Facility

class CarePeople(BaseModel):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
    )
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
    )
