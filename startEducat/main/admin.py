from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CPUmanufacturer, CPU


class CPUmanufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'cpuManufacturer', 'timeCpuManufacturerCreated')


class CPUAdmin(admin.ModelAdmin):
    list_display = ('id', 'cpuName', 'cpuManufacturer', 'cpuPrice', 'timeCpuCreated')


admin.site.register(CPUmanufacturer, CPUmanufacturerAdmin)
admin.site.register(CPU, CPUAdmin)