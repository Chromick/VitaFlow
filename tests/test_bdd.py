import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from scheduling.models import Patient, Doctor, Appointment
from datetime import datetime, timedelta
from django.utils import timezone

# Carrega o arquivo de funcionalidade BDD
scenarios("features/agendamento.feature")

@pytest.fixture
def test_data():
    return {}

@given(parsers.parse('que existe um paciente chamado "{nome}"'))
def create_patient(db, nome, test_data):
    patient = Patient.objects.create(
        name=nome,
        cpf="123.456.789-00",
        birth_date="1990-01-01"
    )
    test_data['patient'] = patient

@given(parsers.parse('que existe um médico chamado "{nome}" da especialidade "{especialidade}"'))
def create_doctor(db, nome, especialidade, test_data):
    doctor = Doctor.objects.create(
        name=nome,
        specialty=especialidade,
        crm="12345-SP"
    )
    test_data['doctor'] = doctor

@when(parsers.parse('o paciente solicita um agendamento "{tipo}" para o dia seguinte'))
def schedule_appointment(db, tipo, test_data):
    amanha = timezone.now() + timedelta(days=1)
    
    agendamento = Appointment.objects.create(
        patient=test_data['patient'],
        doctor=test_data['doctor'],
        kind=tipo,
        status=Appointment.Status.SCHEDULED,
        scheduled_for=amanha,
        location="Clínica Principal"
    )
    test_data['appointment'] = agendamento

@then(parsers.parse('um agendamento deve ser criado no banco de dados com status "{status}"'))
def check_appointment_created(db, status, test_data):
    assert test_data['appointment'].id is not None
    assert test_data['appointment'].status == status
