from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, FormView, TemplateView, View

from .forms import AppointmentForm
from .models import Appointment, Doctor
from .services.facade import SchedulingFacade
from .ui.brand import BRAND
from .ui.components import PATTERN_CARDS, appointment_badge, dashboard_cards


class BrandContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brand"] = BRAND
        return context


class DashboardView(BrandContextMixin, TemplateView):
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


class AppointmentCreateView(BrandContextMixin, FormView):
    template_name = "scheduling/appointment_form.html"
    form_class = AppointmentForm

    def form_valid(self, form):
        appointment = SchedulingFacade().schedule(
            patient_data=form.patient_data(),
            appointment_data=form.appointment_data(),
        )
        messages.success(self.request, "Consulta agendada e notificacoes enviadas.")
        return redirect(appointment)


class AppointmentDetailView(BrandContextMixin, DetailView):
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
