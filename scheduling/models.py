from django.db import models
from django.urls import reverse


class Patient(models.Model):
    name = models.CharField("nome", max_length=120)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    birth_date = models.DateField("data de nascimento")
    phone = models.CharField("telefone", max_length=30, blank=True)
    insurance = models.CharField("convenio", max_length=80, blank=True)
    medical_history = models.TextField("historico medico", blank=True)
    allergies = models.TextField("alergias", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField("nome", max_length=120)
    specialty = models.CharField("especialidade", max_length=90)
    crm = models.CharField("CRM", max_length=30, unique=True)

    class Meta:
        ordering = ["specialty", "name"]

    def __str__(self):
        return f"Dra./Dr. {self.name} - {self.specialty}"


class Appointment(models.Model):
    class Kind(models.TextChoices):
        IN_PERSON = "presencial", "Presencial"
        ONLINE = "online", "Online"
        EMERGENCY = "emergencial", "Emergencial"

    class Status(models.TextChoices):
        SCHEDULED = "agendada", "Agendada"
        CANCELED = "cancelada", "Cancelada"
        FINISHED = "finalizada", "Finalizada"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name="appointments")
    kind = models.CharField("tipo", max_length=20, choices=Kind.choices)
    status = models.CharField("status", max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    scheduled_for = models.DateTimeField("data e horario")
    symptoms = models.TextField("sintomas", blank=True)
    location = models.CharField("local/link", max_length=180)
    priority_label = models.CharField("prioridade", max_length=40)
    priority_score = models.PositiveSmallIntegerField("pontuacao de prioridade", default=1)
    priority_reason = models.CharField("motivo da prioridade", max_length=180, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-priority_score", "scheduled_for"]

    def __str__(self):
        return f"{self.get_kind_display()} - {self.patient} com {self.doctor.name}"

    def get_absolute_url(self):
        return reverse("appointment_detail", kwargs={"pk": self.pk})


class NotificationLog(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="notifications")
    target = models.CharField("destinatario", max_length=80)
    channel = models.CharField("canal", max_length=30)
    message = models.TextField("mensagem")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.channel} para {self.target}"
