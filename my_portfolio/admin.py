from django.contrib import admin
from .models import Projects

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'link', 'description')
    search_fields = ('name', 'description')  # Allow search by name or description
    list_filter = ('price',)  # Filter projects by price

admin.site.register(Projects, ProjectAdmin)
