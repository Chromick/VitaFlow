from django.urls import path

from . import views


urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("agendar/", views.AppointmentCreateView.as_view(), name="appointment_create"),
    path("consultas/<int:pk>/", views.AppointmentDetailView.as_view(), name="appointment_detail"),
    path("consultas/<int:pk>/cancelar/", views.CancelAppointmentView.as_view(), name="appointment_cancel"),
    path("medicos/novo/", views.DoctorCreateView.as_view(), name="doctor_create"),
    path("clinica/nova/", views.ClinicCreateView.as_view(), name="clinic_create"),
    path("agenda/", views.AgendaView.as_view(), name="agenda"),
]
