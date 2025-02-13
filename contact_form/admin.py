from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'email', 'message')
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fieldsets = (
        ('Контактная информация', {
            'fields': ('name', 'email')
        }),
        ('Сообщение', {
            'fields': ('message',)
        }),
        ('Статус', {
            'fields': ('is_processed',)
        })
    )

    def mark_as_processed(self, request, queryset):
        queryset.update(is_processed=True)
    mark_as_processed.short_description = "Отметить как обработанные"

    actions = [mark_as_processed]