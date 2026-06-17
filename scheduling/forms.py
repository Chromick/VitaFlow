from django import forms
from django.utils import timezone

from .models import Appointment, Doctor


class AppointmentForm(forms.Form):
    name = forms.CharField(label="Nome completo", max_length=120)
    cpf = forms.CharField(label="CPF", max_length=14)
    birth_date = forms.DateField(
        label="Data de nascimento",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    phone = forms.CharField(label="Telefone", max_length=30, required=False)
    insurance = forms.CharField(label="Convenio", max_length=80, required=False)
    medical_history = forms.CharField(
        label="Historico medico",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )
    allergies = forms.CharField(
        label="Alergias",
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
    )
    doctor = forms.ModelChoiceField(label="Medico", queryset=Doctor.objects.none())
    kind = forms.ChoiceField(label="Tipo de consulta", choices=Appointment.Kind.choices)
    scheduled_for = forms.DateTimeField(
        label="Data e horario",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    symptoms = forms.CharField(
        label="Sintomas ou observacoes",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["doctor"].queryset = Doctor.objects.all()
        self._apply_design_system()

    def clean_scheduled_for(self):
        scheduled_for = self.cleaned_data["scheduled_for"]
        if timezone.is_naive(scheduled_for):
            scheduled_for = timezone.make_aware(scheduled_for)
        if scheduled_for < timezone.now():
            raise forms.ValidationError("Escolha uma data futura para o agendamento.")
        return scheduled_for

    def patient_data(self):
        fields = ["name", "cpf", "birth_date", "phone", "insurance", "medical_history", "allergies"]
        return {field: self.cleaned_data[field] for field in fields}

    def appointment_data(self):
        fields = ["doctor", "kind", "scheduled_for", "symptoms"]
        return {field: self.cleaned_data[field] for field in fields}

    def _apply_design_system(self):
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
