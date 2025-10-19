from django.contrib import admin
from django.utils.html import format_html
from .models import Runway, Gate, Personnel, Aircraft, Flight, ResourceConstraint


@admin.register(Runway)
class RunwayAdmin(admin.ModelAdmin):
    """Admin interface for Runway model."""
    list_display = ['runway_code', 'name', 'length_meters', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['runway_code', 'name']
    ordering = ['runway_code']


@admin.register(Gate)
class GateAdmin(admin.ModelAdmin):
    """Admin interface for Gate model."""
    list_display = ['gate_code', 'name', 'terminal', 'is_active', 'created_at']
    list_filter = ['terminal', 'is_active', 'created_at']
    search_fields = ['gate_code', 'name', 'terminal']
    ordering = ['gate_code']


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    """Admin interface for Personnel model."""
    list_display = ['employee_id', 'get_full_name', 'personnel_type', 'license_number', 'years_of_experience', 'is_active']
    list_filter = ['personnel_type', 'is_active', 'created_at']
    search_fields = ['first_name', 'last_name', 'employee_id', 'license_number']
    ordering = ['last_name', 'first_name']
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'employee_id')
        }),
        ('Professional Details', {
            'fields': ('personnel_type', 'license_number', 'years_of_experience')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    """Admin interface for Aircraft model."""
    list_display = ['registration_number', 'manufacturer', 'model', 'capacity', 'status', 'last_maintenance_date']
    list_filter = ['status', 'manufacturer', 'created_at']
    search_fields = ['registration_number', 'model', 'manufacturer']
    ordering = ['registration_number']
    fieldsets = (
        ('Aircraft Identification', {
            'fields': ('registration_number', 'manufacturer', 'model', 'year_manufactured')
        }),
        ('Specifications', {
            'fields': ('capacity',)
        }),
        ('Status & Maintenance', {
            'fields': ('status', 'last_maintenance_date')
        }),
    )


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    """Admin interface for Flight model."""
    list_display = ['flight_number', 'origin', 'destination', 'departure_time', 'arrival_time', 'status', 'get_duration_display']
    list_filter = ['status', 'departure_time', 'origin', 'destination']
    search_fields = ['flight_number', 'origin', 'destination']
    ordering = ['-departure_time']
    filter_horizontal = ['copilots']
    
    fieldsets = (
        ('Flight Information', {
            'fields': ('flight_number', 'origin', 'destination', 'status')
        }),
        ('Schedule', {
            'fields': ('departure_time', 'arrival_time')
        }),
        ('Resource Assignment', {
            'fields': ('runway', 'gate', 'aircraft')
        }),
        ('Crew Assignment', {
            'fields': ('pilot', 'copilots')
        }),
    )
    
    def get_duration_display(self, obj):
        """Display flight duration in a readable format."""
        duration = obj.get_duration()
        hours = int(duration)
        minutes = int((duration - hours) * 60)
        return f"{hours}h {minutes}m"
    get_duration_display.short_description = 'Duration'
    
    def save_model(self, request, obj, form, change):
        """Override to handle validation properly."""
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            self.message_user(request, f"Error saving flight: {str(e)}", level='error')
            raise
    
    def save_related(self, request, form, formsets, change):
        """Override to validate copilots after they are saved."""
        super().save_related(request, form, formsets, change)
        try:
            form.instance.validate_copilots()
        except Exception as e:
            self.message_user(request, f"Warning: {str(e)}", level='warning')


@admin.register(ResourceConstraint)
class ResourceConstraintAdmin(admin.ModelAdmin):
    """Admin interface for ResourceConstraint model."""
    list_display = ['name', 'constraint_type', 'is_active', 'created_at']
    list_filter = ['constraint_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
