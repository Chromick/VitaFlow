import pytest
from datetime import date, timedelta
from django.utils import timezone
from scheduling.models import Patient, Appointment
from scheduling.domain.priority_strategy import (
    PriorityStrategySelector,
    NormalPriorityStrategy,
    ElderlyPriorityStrategy,
    EmergencyPriorityStrategy
)

@pytest.mark.django_db
class TestPriorityStrategy:

    @pytest.fixture
    def selector(self):
        return PriorityStrategySelector()

    def test_emergency_priority(self, selector):
        """Testa se consultas emergenciais recebem prioridade máxima, independente da idade."""
        # Não precisamos nem salvar no banco para o domínio calcular a idade se passarmos apenas o objeto
        patient = Patient(name="Carlos", birth_date=date.today() - timedelta(days=365 * 30))  # 30 anos
        
        strategy = selector.select(patient, Appointment.Kind.EMERGENCY)
        
        assert isinstance(strategy, EmergencyPriorityStrategy)
        
        result = strategy.calculate(patient, Appointment.Kind.EMERGENCY)
        assert result.label == "Maxima"
        assert result.score == 5

    def test_elderly_priority(self, selector):
        """Testa se pacientes com 60 anos ou mais recebem prioridade Alta."""
        # 65 anos
        patient = Patient(name="Dona Maria", birth_date=date.today() - timedelta(days=365 * 65))
        
        strategy = selector.select(patient, Appointment.Kind.IN_PERSON)
        
        assert isinstance(strategy, ElderlyPriorityStrategy)
        
        result = strategy.calculate(patient, Appointment.Kind.IN_PERSON)
        assert result.label == "Alta"
        assert result.score == 3

    def test_normal_priority(self, selector):
        """Testa se pacientes normais (< 60 anos) e não emergenciais recebem prioridade Normal."""
        patient = Patient(name="Joãozinho", birth_date=date.today() - timedelta(days=365 * 25))
        
        strategy = selector.select(patient, Appointment.Kind.ONLINE)
        
        assert isinstance(strategy, NormalPriorityStrategy)
        
        result = strategy.calculate(patient, Appointment.Kind.ONLINE)
        assert result.label == "Normal"
        assert result.score == 1
