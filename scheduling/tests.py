from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from scheduling.models import Appointment, Doctor, NotificationLog, Patient
from scheduling.services.facade import SchedulingFacade


class SchedulingPatternsTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            name="Ana Ribeiro",
            specialty="Cardiologia",
            crm="CRM-SP 48291",
        )

    def test_facade_integrates_patterns_when_scheduling_emergency(self):
        appointment = SchedulingFacade().schedule(
            patient_data={
                "name": "Lucas Almeida",
                "cpf": "987.654.321-00",
                "birth_date": timezone.datetime(1995, 3, 22).date(),
                "phone": "(11) 97777-2020",
                "insurance": "",
                "medical_history": "",
                "allergies": "",
            },
            appointment_data={
                "doctor": self.doctor,
                "kind": Appointment.Kind.EMERGENCY,
                "scheduled_for": timezone.now() + timedelta(hours=3),
                "symptoms": "Dor intensa no peito.",
            },
        )

        self.assertEqual(appointment.priority_label, "Maxima")
        self.assertEqual(appointment.location, "Pronto atendimento VitaFlow - prioridade imediata")
        self.assertEqual(NotificationLog.objects.filter(appointment=appointment).count(), 3)

    def test_builder_updates_existing_patient_through_facade(self):
        Patient.objects.create(
            name="Marina Costa",
            cpf="123.456.789-10",
            birth_date=timezone.datetime(1958, 7, 12).date(),
        )

        appointment = SchedulingFacade().schedule(
            patient_data={
                "name": "Marina Costa",
                "cpf": "123.456.789-10",
                "birth_date": timezone.datetime(1958, 7, 12).date(),
                "phone": "(11) 98888-1010",
                "insurance": "SaudePlus",
                "medical_history": "Hipertensao controlada.",
                "allergies": "Dipirona.",
            },
            appointment_data={
                "doctor": self.doctor,
                "kind": Appointment.Kind.IN_PERSON,
                "scheduled_for": timezone.now() + timedelta(days=2),
                "symptoms": "Retorno.",
            },
        )

        appointment.patient.refresh_from_db()
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(appointment.patient.insurance, "SaudePlus")
        self.assertEqual(appointment.priority_label, "Alta")
