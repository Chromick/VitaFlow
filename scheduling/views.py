from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, View

from .forms import AppointmentForm, ClinicForm, DoctorForm
from .models import Appointment, Clinic, Doctor
from .services.facade import SchedulingFacade
from .ui.brand import BRAND
from .ui.components import PATTERN_CARDS, appointment_badge, dashboard_cards


class BrandContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brand"] = BRAND
        return context


class DashboardView(LoginRequiredMixin, BrandContextMixin, TemplateView):
    template_name = "scheduling/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointments = Appointment.objects.select_related("patient", "doctor").prefetch_related("notifications")[:8]
        context.update(
            {
                "stats": dashboard_cards(),
                "patterns": PATTERN_CARDS,
                "appointments": appointments,
                "doctors_count": Doctor.objects.count(),
            }
        )
        return context


class AppointmentCreateView(LoginRequiredMixin, BrandContextMixin, FormView):
    template_name = "scheduling/appointment_form.html"
    form_class = AppointmentForm

    def form_valid(self, form):
        appointment = SchedulingFacade().schedule(
            patient_data=form.patient_data(),
            appointment_data=form.appointment_data(),
        )
        messages.success(self.request, "Consulta agendada e notificacoes enviadas.")
        return redirect(appointment)


class AppointmentDetailView(LoginRequiredMixin, BrandContextMixin, DetailView):
    model = Appointment
    template_name = "scheduling/appointment_detail.html"
    context_object_name = "appointment"

    def get_queryset(self):
        return Appointment.objects.select_related("patient", "doctor").prefetch_related("notifications")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["badge"] = appointment_badge(self.object)
        return context


class CancelAppointmentView(View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        SchedulingFacade().cancel(appointment)
        messages.info(request, "Consulta cancelada e envolvidos notificados.")
        return redirect(appointment)


class DoctorCreateView(LoginRequiredMixin, BrandContextMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "scheduling/doctor_form.html"
    success_url = reverse_lazy("doctor_create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Médico {self.object.name} cadastrado com sucesso!")
        return response


class ClinicCreateView(LoginRequiredMixin, BrandContextMixin, CreateView):
    model = Clinic
    form_class = ClinicForm
    template_name = "scheduling/clinic_form.html"
    success_url = reverse_lazy("clinic_create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clinics"] = Clinic.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Clínica {self.object.name} cadastrada com sucesso!")
        return response


class AgendaView(LoginRequiredMixin, BrandContextMixin, ListView):
    model = Appointment
    template_name = "scheduling/agenda.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return (
            Appointment.objects
            .filter(status=Appointment.Status.SCHEDULED)
            .select_related("patient", "doctor")
            .order_by("scheduled_for")
        )
