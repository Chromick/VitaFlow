import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from scheduling.models import Patient, Doctor, Appointment
from scheduling.services.facade import SchedulingFacade
from datetime import date, timedelta
from django.utils import timezone

# Carrega o arquivo de funcionalidade BDD
scenarios("features/agendamento.feature")

@pytest.fixture
def test_data():
    return {}

@given(parsers.parse('que existe um paciente chamado "{nome}" com "{idade}" anos'))
def create_patient_with_age(db, nome, idade, test_data):
    birth_year = date.today().year - int(idade)
    patient = Patient.objects.create(
        name=nome,
        cpf=f"123.456.{idade}-00",
        birth_date=f"{birth_year}-01-01"
    )
    test_data['patient'] = patient

@given(parsers.parse('que existe um médico chamado "{nome}" da especialidade "{especialidade}"'))
def create_doctor(db, nome, especialidade, test_data):
    doctor = Doctor.objects.create(
        name=nome,
        specialty=especialidade,
        crm=f"12345-{nome[:2]}"
    )
    test_data['doctor'] = doctor

@when(parsers.parse('o paciente solicita um agendamento "{tipo}" para o dia seguinte'))
def schedule_appointment_tomorrow(db, tipo, test_data):
    amanha = timezone.now() + timedelta(days=1)
    
    # Usa a Facade para simular o fluxo real que passa pelo domínio (PriorityStrategy, Factory)
    facade = SchedulingFacade()
    agendamento = facade.schedule_appointment(
        patient=test_data['patient'],
        doctor=test_data['doctor'],
        kind=tipo,
        scheduled_for=amanha
    )
    test_data['appointment'] = agendamento

@when(parsers.parse('o paciente solicita um agendamento "{tipo}" para hoje'))
def schedule_appointment_today(db, tipo, test_data):
    hoje = timezone.now()
    
    facade = SchedulingFacade()
    agendamento = facade.schedule_appointment(
        patient=test_data['patient'],
        doctor=test_data['doctor'],
        kind=tipo,
        scheduled_for=hoje
    )
    test_data['appointment'] = agendamento

@then(parsers.parse('um agendamento deve ser criado no banco de dados com status "{status}"'))
def check_appointment_created(db, status, test_data):
    assert test_data['appointment'].id is not None
    assert test_data['appointment'].status == status

@then(parsers.parse('a prioridade definida deve ser "{prioridade}"'))
def check_appointment_priority(db, prioridade, test_data):
    assert test_data['appointment'].priority_label == prioridade
