import pytest
from django.utils import timezone
from datetime import timedelta
from scheduling.models import Patient, Doctor, Appointment
from scheduling.domain.appointment_factory import AppointmentFactory

@pytest.mark.django_db
class TestAppointmentFactory:
    
    @pytest.fixture
    def mock_data(self):
        patient = Patient.objects.create(name="Teste", cpf="000.000.000-00", birth_date="1990-01-01")
        doctor = Doctor.objects.create(name="Dr. Teste", specialty="Geral", crm="1111-SP")
        amanha = timezone.now() + timedelta(days=1)
        return {"patient": patient, "doctor": doctor, "scheduled_for": amanha}

    def test_create_in_person_appointment(self, mock_data):
        """Testa a criação de um agendamento presencial usando a Factory."""
        appointment = AppointmentFactory.create(
            kind=Appointment.Kind.IN_PERSON,
            patient=mock_data["patient"],
            doctor=mock_data["doctor"],
            scheduled_for=mock_data["scheduled_for"]
        )
        
        assert appointment.kind == Appointment.Kind.IN_PERSON
        assert appointment.location == "Unidade VitaFlow - Sala de triagem"
        assert appointment.symptoms == "Consulta presencial agendada pela recepcao digital."
        assert appointment.id is None  # A factory não deve salvar no banco, apenas criar a entidade

    def test_create_online_appointment(self, mock_data):
        """Testa a criação de um agendamento online usando a Factory."""
        appointment = AppointmentFactory.create(
            kind=Appointment.Kind.ONLINE,
            patient=mock_data["patient"],
            doctor=mock_data["doctor"],
            scheduled_for=mock_data["scheduled_for"]
        )
        
        assert appointment.kind == Appointment.Kind.ONLINE
        assert appointment.location == "Sala virtual VitaFlow Meet"
        
    def test_create_emergency_appointment_with_custom_symptoms(self, mock_data):
        """Testa a criação emergencial passando sintomas personalizados."""
        sintomas_urgentes = "Paciente relatando dor forte no peito."
        appointment = AppointmentFactory.create(
            kind=Appointment.Kind.EMERGENCY,
            patient=mock_data["patient"],
            doctor=mock_data["doctor"],
            scheduled_for=mock_data["scheduled_for"],
            symptoms=sintomas_urgentes
        )
        
        assert appointment.kind == Appointment.Kind.EMERGENCY
        assert appointment.location == "Pronto atendimento VitaFlow - prioridade imediata"
        assert appointment.symptoms == sintomas_urgentes
