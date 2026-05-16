from dataclasses import dataclass

from scheduling.models import Appointment


@dataclass(frozen=True)
class AppointmentDefaults:
    location: str
    default_symptom_note: str


class AppointmentFactory:
    """Factory Method: encapsula a criacao dos tipos de consulta."""

    _defaults = {
        Appointment.Kind.IN_PERSON: AppointmentDefaults(
            location="Unidade VitaFlow - Sala de triagem",
            default_symptom_note="Consulta presencial agendada pela recepcao digital.",
        ),
        Appointment.Kind.ONLINE: AppointmentDefaults(
            location="Sala virtual VitaFlow Meet",
            default_symptom_note="Consulta online com link enviado ao paciente.",
        ),
        Appointment.Kind.EMERGENCY: AppointmentDefaults(
            location="Pronto atendimento VitaFlow - prioridade imediata",
            default_symptom_note="Atendimento emergencial registrado no sistema.",
        ),
    }

    @classmethod
    def create(cls, *, kind, patient, doctor, scheduled_for, symptoms="") -> Appointment:
        defaults = cls._defaults[kind]
        return Appointment(
            kind=kind,
            patient=patient,
            doctor=doctor,
            scheduled_for=scheduled_for,
            symptoms=symptoms or defaults.default_symptom_note,
            location=defaults.location,
        )
