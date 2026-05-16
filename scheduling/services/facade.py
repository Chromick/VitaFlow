from django.db import transaction

from scheduling.domain.appointment_factory import AppointmentFactory
from scheduling.domain.observers import AppointmentSubject, DoctorNotifier, PatientNotifier, ReceptionNotifier
from scheduling.domain.patient_builder import PatientProfileBuilder
from scheduling.domain.priority_strategy import PriorityStrategySelector
from scheduling.models import Appointment, Patient


class SchedulingFacade:
    """Facade: expoe um caso de uso simples para a view."""

    def __init__(self):
        self.priority_selector = PriorityStrategySelector()
        self.subject = AppointmentSubject()
        self.subject.attach(PatientNotifier())
        self.subject.attach(DoctorNotifier())
        self.subject.attach(ReceptionNotifier())

    @transaction.atomic
    def schedule(self, *, patient_data, appointment_data):
        patient = self._get_or_create_patient(patient_data)
        appointment = AppointmentFactory.create(patient=patient, **appointment_data)

        strategy = self.priority_selector.select(patient, appointment.kind)
        priority = strategy.calculate(patient, appointment.kind)
        appointment.priority_label = priority.label
        appointment.priority_score = priority.score
        appointment.priority_reason = priority.reason
        appointment.save()

        self.subject.notify(appointment, "Agendamento confirmado")
        return appointment

    @transaction.atomic
    def cancel(self, appointment: Appointment):
        appointment.status = Appointment.Status.CANCELED
        appointment.save(update_fields=["status"])
        self.subject.notify(appointment, "Agendamento cancelado")
        return appointment

    def _get_or_create_patient(self, patient_data):
        patient = Patient.objects.filter(cpf=patient_data["cpf"]).first()
        if patient:
            for field, value in patient_data.items():
                setattr(patient, field, value)
            patient.save()
            return patient

        builder = (
            PatientProfileBuilder(
                name=patient_data["name"],
                cpf=patient_data["cpf"],
                birth_date=patient_data["birth_date"],
            )
            .with_contact(patient_data.get("phone", ""))
            .with_insurance(patient_data.get("insurance", ""))
            .with_clinical_notes(
                patient_data.get("medical_history", ""),
                patient_data.get("allergies", ""),
            )
        )
        patient = builder.build()
        patient.save()
        return patient
