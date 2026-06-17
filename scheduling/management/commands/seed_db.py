from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from scheduling.models import Appointment, Clinic, Doctor, Patient
from scheduling.services.facade import SchedulingFacade


class Command(BaseCommand):
    help = "Cria usuario de teste, clinica, medicos, pacientes e consultas de demonstracao."

    def handle(self, *args, **options):
        # ---------- Usuario de teste ----------
        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@vitaflow.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            user.set_password("admin123")
            user.save()
            self.stdout.write(self.style.SUCCESS("Usuario admin criado (senha: admin123)."))
        else:
            self.stdout.write(self.style.WARNING("Usuario admin ja existe."))

        # ---------- Clinica ----------
        clinic, _ = Clinic.objects.get_or_create(
            cnpj="12.345.678/0001-99",
            defaults={
                "name": "VitaFlow Clinic - Unidade Centro",
                "phone": "(11) 3333-4444",
                "address": "Av. Paulista, 1000 - Bela Vista, São Paulo - SP",
            },
        )
        self.stdout.write(self.style.SUCCESS(f"Clinica: {clinic.name}"))

        # ---------- Medicos ----------
        doctors_data = [
            ("Ana Ribeiro", "Cardiologia", "CRM-SP 48291"),
            ("Caio Mendes", "Clínica Geral", "CRM-SP 77412"),
            ("Helena Duarte", "Neurologia", "CRM-SP 91280"),
            ("Roberto Silva", "Ortopedia", "CRM-SP 55301"),
            ("Juliana Ferreira", "Pediatria", "CRM-SP 63820"),
        ]
        doctors = []
        for name, specialty, crm in doctors_data:
            doc, _ = Doctor.objects.get_or_create(crm=crm, defaults={"name": name, "specialty": specialty})
            doctors.append(doc)
        self.stdout.write(self.style.SUCCESS(f"{len(doctors)} medicos cadastrados."))

        # ---------- Pacientes e Consultas ----------
        if Appointment.objects.exists():
            self.stdout.write(self.style.WARNING("Consultas de exemplo ja existem. Pulando criacao."))
            return

        now = timezone.now()

        appointments_data = [
            {
                "patient": {
                    "name": "Marina Costa",
                    "cpf": "123.456.789-10",
                    "birth_date": timezone.datetime(1958, 7, 12).date(),
                    "phone": "(11) 98888-1010",
                    "insurance": "SaúdePlus",
                    "medical_history": "Hipertensão controlada há 10 anos.",
                    "allergies": "Dipirona",
                },
                "appointment": {
                    "doctor": doctors[0],
                    "kind": Appointment.Kind.IN_PERSON,
                    "scheduled_for": now + timedelta(days=2, hours=9),
                    "symptoms": "Retorno de cardiologia — checkup anual.",
                },
            },
            {
                "patient": {
                    "name": "Lucas Almeida",
                    "cpf": "987.654.321-00",
                    "birth_date": timezone.datetime(1995, 3, 22).date(),
                    "phone": "(11) 97777-2020",
                    "insurance": "",
                    "medical_history": "",
                    "allergies": "",
                },
                "appointment": {
                    "doctor": doctors[0],
                    "kind": Appointment.Kind.EMERGENCY,
                    "scheduled_for": now + timedelta(hours=3),
                    "symptoms": "Dor intensa no peito e falta de ar.",
                },
            },
            {
                "patient": {
                    "name": "Fernanda Oliveira",
                    "cpf": "456.123.789-55",
                    "birth_date": timezone.datetime(1987, 11, 5).date(),
                    "phone": "(11) 96666-3030",
                    "insurance": "Unimed",
                    "medical_history": "Enxaquecas frequentes desde 2019.",
                    "allergies": "Nenhuma conhecida",
                },
                "appointment": {
                    "doctor": doctors[2],
                    "kind": Appointment.Kind.ONLINE,
                    "scheduled_for": now + timedelta(days=1, hours=14),
                    "symptoms": "Consulta de acompanhamento — cefaleia crônica.",
                },
            },
            {
                "patient": {
                    "name": "Carlos Eduardo Santos",
                    "cpf": "321.654.987-11",
                    "birth_date": timezone.datetime(2015, 6, 18).date(),
                    "phone": "(11) 95555-4040",
                    "insurance": "Amil",
                    "medical_history": "Vacinação em dia.",
                    "allergies": "Amendoim",
                },
                "appointment": {
                    "doctor": doctors[4],
                    "kind": Appointment.Kind.IN_PERSON,
                    "scheduled_for": now + timedelta(days=3, hours=10),
                    "symptoms": "Consulta pediátrica de rotina.",
                },
            },
            {
                "patient": {
                    "name": "Patrícia Nunes",
                    "cpf": "789.012.345-66",
                    "birth_date": timezone.datetime(1972, 9, 30).date(),
                    "phone": "(11) 94444-5050",
                    "insurance": "Bradesco Saúde",
                    "medical_history": "Fratura de fêmur em 2022, reabilitação concluída.",
                    "allergies": "",
                },
                "appointment": {
                    "doctor": doctors[3],
                    "kind": Appointment.Kind.IN_PERSON,
                    "scheduled_for": now + timedelta(days=4, hours=11),
                    "symptoms": "Retorno ortopédico — avaliação pós-reabilitação.",
                },
            },
        ]

        for data in appointments_data:
            SchedulingFacade().schedule(
                patient_data=data["patient"],
                appointment_data=data["appointment"],
            )

        self.stdout.write(self.style.SUCCESS(f"{len(appointments_data)} consultas de exemplo criadas com sucesso!"))
        self.stdout.write(self.style.SUCCESS("Seed completo. Use admin/admin123 para acessar o sistema."))
