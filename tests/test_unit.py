import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from scheduling.models import Patient, Doctor, Appointment

@pytest.mark.django_db
class TestAppointmentBusinessRules:
    
    def test_create_appointment_success(self):
        """Testa se é possível criar um agendamento válido no banco"""
        patient = Patient.objects.create(name="Maria", cpf="111.111.111-11", birth_date="1980-05-10")
        doctor = Doctor.objects.create(name="Dr. João", specialty="Dermatologia", crm="54321-RJ")
        amanha = timezone.now() + timedelta(days=1)
        
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            kind=Appointment.Kind.IN_PERSON,
            scheduled_for=amanha,
            location="Clínica Central"
        )
        
        assert appointment.id is not None
        assert appointment.status == Appointment.Status.SCHEDULED
