from django.urls import path

from . import views


urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("agendar/", views.AppointmentCreateView.as_view(), name="appointment_create"),
    path("consultas/<int:pk>/", views.AppointmentDetailView.as_view(), name="appointment_detail"),
    path("consultas/<int:pk>/cancelar/", views.CancelAppointmentView.as_view(), name="appointment_cancel"),
]
