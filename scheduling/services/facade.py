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
        
        # Integrando com Microsserviço de Telemedicina
        if appointment.kind == Appointment.Kind.ONLINE:
            try:
                import requests
                import os
                telemedicine_url = os.environ.get("TELEMEDICINE_SERVICE_URL", "http://localhost:8002/generate-link")
                payload = {"doctor": appointment.doctor.name, "patient": appointment.patient.name}
                response = requests.post(telemedicine_url, json=payload, timeout=2)
                if response.status_code == 200:
                    appointment.location = response.json().get("url", appointment.location)
            except Exception as e:
                print(f"Erro na telemedicina: {e}")

        appointment.save()

        # Integrando com Microsserviço de Prontuário (EHR)
        try:
            import requests
            import os
            ehr_url = os.environ.get("EHR_SERVICE_URL", "http://localhost:8003/record")
            ehr_payload = {
                "patient": appointment.patient.name,
                "doctor": appointment.doctor.name,
                "date": str(appointment.scheduled_for),
                "notes": f"Consulta marcada: {appointment.get_kind_display()} - Sintomas relatados: {appointment.symptoms}"
            }
            requests.post(ehr_url, json=ehr_payload, timeout=2)
        except Exception as e:
            print(f"Erro no EHR: {e}")

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
