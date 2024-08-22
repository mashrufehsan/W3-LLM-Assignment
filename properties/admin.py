from django.contrib import admin
from .models import PropertySummary


class PropertySummaryAdmin(admin.ModelAdmin):
    list_display = ('property_title', 'summary',
                    'created_date', 'updated_date')
    readonly_fields = ['created_date', 'updated_date']

    def property_title(self, obj):
        return obj.property_info.title
    property_title.short_description = 'Property Title'


admin.site.register(PropertySummary, PropertySummaryAdmin)
