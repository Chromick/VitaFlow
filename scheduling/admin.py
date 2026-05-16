from django.contrib import admin

from .models import Appointment, Doctor, NotificationLog, Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "cpf", "phone", "insurance")
    search_fields = ("name", "cpf")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialty", "crm")
    search_fields = ("name", "specialty", "crm")


class NotificationInline(admin.TabularInline):
    model = NotificationLog
    extra = 0
    readonly_fields = ("target", "channel", "message", "created_at")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "kind", "status", "scheduled_for", "priority_label")
    list_filter = ("kind", "status", "priority_label")
    search_fields = ("patient__name", "doctor__name")
    inlines = [NotificationInline]


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ("target", "channel", "appointment", "created_at")
    search_fields = ("target", "message")
