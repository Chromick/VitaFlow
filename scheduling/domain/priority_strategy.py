from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date

from scheduling.models import Appointment, Patient


@dataclass(frozen=True)
class PriorityResult:
    label: str
    score: int
    reason: str


class PriorityStrategy(ABC):
    """Strategy: permite trocar a regra de prioridade sem mexer no fluxo principal."""

    @abstractmethod
    def calculate(self, patient: Patient, appointment_kind: str) -> PriorityResult:
        raise NotImplementedError


class NormalPriorityStrategy(PriorityStrategy):
    def calculate(self, patient: Patient, appointment_kind: str) -> PriorityResult:
        return PriorityResult("Normal", 1, "Atendimento eletivo sem sinal de urgencia.")


class ElderlyPriorityStrategy(PriorityStrategy):
    def calculate(self, patient: Patient, appointment_kind: str) -> PriorityResult:
        return PriorityResult("Alta", 3, "Paciente com 60 anos ou mais.")


class EmergencyPriorityStrategy(PriorityStrategy):
    def calculate(self, patient: Patient, appointment_kind: str) -> PriorityResult:
        return PriorityResult("Maxima", 5, "Consulta emergencial exige atendimento imediato.")


class PriorityStrategySelector:
    def select(self, patient: Patient, appointment_kind: str) -> PriorityStrategy:
        if appointment_kind == Appointment.Kind.EMERGENCY:
            return EmergencyPriorityStrategy()

        if self._age(patient.birth_date) >= 60:
            return ElderlyPriorityStrategy()

        return NormalPriorityStrategy()

    @staticmethod
    def _age(birth_date):
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
