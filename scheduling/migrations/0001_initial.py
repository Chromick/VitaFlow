from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="nome")),
                ("specialty", models.CharField(max_length=90, verbose_name="especialidade")),
                ("crm", models.CharField(max_length=30, unique=True, verbose_name="CRM")),
            ],
            options={"ordering": ["specialty", "name"]},
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="nome")),
                ("cpf", models.CharField(max_length=14, unique=True, verbose_name="CPF")),
                ("birth_date", models.DateField(verbose_name="data de nascimento")),
                ("phone", models.CharField(blank=True, max_length=30, verbose_name="telefone")),
                ("insurance", models.CharField(blank=True, max_length=80, verbose_name="convenio")),
                ("medical_history", models.TextField(blank=True, verbose_name="historico medico")),
                ("allergies", models.TextField(blank=True, verbose_name="alergias")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Appointment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("kind", models.CharField(choices=[("presencial", "Presencial"), ("online", "Online"), ("emergencial", "Emergencial")], max_length=20, verbose_name="tipo")),
                ("status", models.CharField(choices=[("agendada", "Agendada"), ("cancelada", "Cancelada"), ("finalizada", "Finalizada")], default="agendada", max_length=20, verbose_name="status")),
                ("scheduled_for", models.DateTimeField(verbose_name="data e horario")),
                ("symptoms", models.TextField(blank=True, verbose_name="sintomas")),
                ("location", models.CharField(max_length=180, verbose_name="local/link")),
                ("priority_label", models.CharField(max_length=40, verbose_name="prioridade")),
                ("priority_score", models.PositiveSmallIntegerField(default=1, verbose_name="pontuacao de prioridade")),
                ("priority_reason", models.CharField(blank=True, max_length=180, verbose_name="motivo da prioridade")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("doctor", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="appointments", to="scheduling.doctor")),
                ("patient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="appointments", to="scheduling.patient")),
            ],
            options={"ordering": ["-priority_score", "scheduled_for"]},
        ),
        migrations.CreateModel(
            name="NotificationLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("target", models.CharField(max_length=80, verbose_name="destinatario")),
                ("channel", models.CharField(max_length=30, verbose_name="canal")),
                ("message", models.TextField(verbose_name="mensagem")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("appointment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to="scheduling.appointment")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
