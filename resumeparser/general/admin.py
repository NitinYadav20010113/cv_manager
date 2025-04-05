from django.contrib import admin
from django.contrib.auth.models import User
from .tblmodels import process_information,file_model,upload_progress

# Register your models here.


admin.site.register(process_information)
admin.site.register(file_model)
# admin.site.register(upload_progress)


# Inline admin for file_model
class FileModelInline(admin.TabularInline):  # You can also use StackedInline
    model = file_model
    extra = 0  # No extra empty forms

# Main admin for upload_progress
@admin.register(upload_progress)
class UploadProgressAdmin(admin.ModelAdmin):
    inlines = [FileModelInline]