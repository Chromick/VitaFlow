from dataclasses import dataclass

from scheduling.models import Appointment


@dataclass(frozen=True)
class StatCard:
    label: str
    value: str
    tone: str = "neutral"


@dataclass(frozen=True)
class PatternCard:
    name: str
    category: str
    role: str
    file_hint: str


PATTERN_CARDS = [
    PatternCard("Builder", "Criacional", "Monta a ficha completa do paciente.", "domain/patient_builder.py"),
    PatternCard("Factory Method", "Criacional", "Cria consultas presenciais, online e emergenciais.", "domain/appointment_factory.py"),
    PatternCard("Strategy", "Comportamental", "Troca a regra de prioridade sem alterar a view.", "domain/priority_strategy.py"),
    PatternCard("Observer", "Comportamental", "Dispara notificacoes para paciente, medico e recepcao.", "domain/observers.py"),
    PatternCard("Facade", "Estrutural", "Orquestra o caso de uso de agendamento.", "services/facade.py"),
]


def dashboard_cards():
    total = Appointment.objects.count()
    emergency = Appointment.objects.filter(kind=Appointment.Kind.EMERGENCY).count()
    scheduled = Appointment.objects.filter(status=Appointment.Status.SCHEDULED).count()
    return [
        StatCard("Consultas", str(total)),
        StatCard("Agendadas", str(scheduled), "success"),
        StatCard("Emergencias", str(emergency), "danger"),
    ]


def appointment_badge(appointment):
    tones = {
        "Normal": "neutral",
        "Alta": "warning",
        "Maxima": "danger",
    }
    return {
        "label": appointment.priority_label,
        "tone": tones.get(appointment.priority_label, "neutral"),
    }
