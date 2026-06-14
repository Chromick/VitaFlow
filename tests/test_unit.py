import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
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

    def test_create_appointment_missing_doctor_raises_error(self):
        """Testa se tentar criar um agendamento sem o médico obrigatório levanta erro do banco."""
        patient = Patient.objects.create(name="José", cpf="222.222.222-22", birth_date="1985-05-10")
        amanha = timezone.now() + timedelta(days=1)
        
        with pytest.raises(IntegrityError):
            Appointment.objects.create(
                patient=patient,
                # Sem doctor (nulo não é permitido)
                kind=Appointment.Kind.IN_PERSON,
                scheduled_for=amanha,
                location="Clínica Central"
            )
