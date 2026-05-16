from abc import ABC, abstractmethod

from scheduling.models import NotificationLog


class AppointmentObserver(ABC):
    """Observer: interessados reagem quando a consulta muda de estado."""

    @abstractmethod
    def update(self, appointment, event: str):
        raise NotImplementedError


class PatientNotifier(AppointmentObserver):
    def update(self, appointment, event: str):
        NotificationLog.objects.create(
            appointment=appointment,
            target=appointment.patient.name,
            channel="SMS",
            message=f"{event}: sua consulta {appointment.get_kind_display()} foi atualizada.",
        )


class DoctorNotifier(AppointmentObserver):
    def update(self, appointment, event: str):
        NotificationLog.objects.create(
            appointment=appointment,
            target=appointment.doctor.name,
            channel="E-mail",
            message=f"{event}: agenda atualizada para {appointment.patient.name}.",
        )


class ReceptionNotifier(AppointmentObserver):
    def update(self, appointment, event: str):
        NotificationLog.objects.create(
            appointment=appointment,
            target="Recepcao VitaFlow",
            channel="Painel interno",
            message=f"{event}: {appointment.priority_label} - {appointment.patient.name}.",
        )


class AppointmentSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: AppointmentObserver):
        self._observers.append(observer)

    def notify(self, appointment, event: str):
        for observer in self._observers:
            observer.update(appointment, event)
