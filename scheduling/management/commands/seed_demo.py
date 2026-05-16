from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from scheduling.models import Appointment, Doctor
from scheduling.services.facade import SchedulingFacade


class Command(BaseCommand):
    help = "Cria dados de demonstracao para a VitaFlow Clinic."

    def handle(self, *args, **options):
        doctors = [
            ("Ana Ribeiro", "Cardiologia", "CRM-SP 48291"),
            ("Caio Mendes", "Clinica Geral", "CRM-SP 77412"),
            ("Helena Duarte", "Neurologia", "CRM-SP 91280"),
        ]
        for name, specialty, crm in doctors:
            Doctor.objects.get_or_create(crm=crm, defaults={"name": name, "specialty": specialty})

        if Appointment.objects.exists():
            self.stdout.write(self.style.WARNING("Dados de exemplo ja existem."))
            return

        doctor = Doctor.objects.first()
        SchedulingFacade().schedule(
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
                "doctor": doctor,
                "kind": Appointment.Kind.IN_PERSON,
                "scheduled_for": timezone.now() + timedelta(days=2),
                "symptoms": "Retorno de cardiologia.",
            },
        )
        SchedulingFacade().schedule(
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
                "doctor": doctor,
                "kind": Appointment.Kind.EMERGENCY,
                "scheduled_for": timezone.now() + timedelta(hours=3),
                "symptoms": "Dor intensa no peito.",
            },
        )
        self.stdout.write(self.style.SUCCESS("Dados de exemplo criados."))
