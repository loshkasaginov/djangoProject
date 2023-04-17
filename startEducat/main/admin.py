from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CPUmanufacturer, CPU


class CPUmanufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'cpuManufacturer', 'timeCpuManufacturerCreated')


class CPUAdmin(admin.ModelAdmin):
    # Ваши существующие настройки, если есть
    list_display = ('id', 'cpuName', 'cpuManufacturer', 'cpuPrice', 'cpuImage', 'timeCpuCreated')
    # Добавьте поле cpuImage в fields
    fields = ['cpuName', 'cpuDescription', 'cpuManufacturer', 'cpuPrice', 'cpuImage']


admin.site.register(CPUmanufacturer, CPUmanufacturerAdmin)
admin.site.register(CPU, CPUAdmin)

#"/"
#"/about"
#"/products/cpu"
#"/products/manufacturer"
#"/products/cpu/<id>"
#"/products/manufacturer/<id>"