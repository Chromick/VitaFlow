from dataclasses import dataclass
from datetime import date

from scheduling.models import Patient


@dataclass
class PatientProfileBuilder:
    """Builder: monta uma ficha de paciente com campos obrigatorios e opcionais."""

    name: str
    cpf: str
    birth_date: date
    phone: str = ""
    insurance: str = ""
    medical_history: str = ""
    allergies: str = ""

    def with_contact(self, phone: str):
        self.phone = phone
        return self

    def with_insurance(self, insurance: str):
        self.insurance = insurance
        return self

    def with_clinical_notes(self, medical_history: str, allergies: str):
        self.medical_history = medical_history
        self.allergies = allergies
        return self

    def build(self) -> Patient:
        return Patient(
            name=self.name,
            cpf=self.cpf,
            birth_date=self.birth_date,
            phone=self.phone,
            insurance=self.insurance,
            medical_history=self.medical_history,
            allergies=self.allergies,
        )
