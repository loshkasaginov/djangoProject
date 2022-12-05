from django.db import models
from django.urls import reverse


class CPUmanufacturer(models.Model):
    class Meta:
        db_table = "СpuManufacturer"
        verbose_name = "производитель процессоров"
        verbose_name_plural = "производители процессоров"

    cpuManufacturer = models.CharField(max_length=100, help_text="Enter cpu manufacturer name", verbose_name="производитель")
    timeCpuManufacturerCreated = models.DateField(auto_now_add=True, verbose_name="время создания Производителя")

    def __str__(self):
        return f'{self.cpuManufacturer}'

    def get_absolute_url(self):
        return reverse('cpumanufact-detail', args=[str(self.id)])



class CPU(models.Model):
    class Meta:
        db_table = "cpu"
        verbose_name = "центральный процессор"
        verbose_name_plural = "центральные процессоры"
    cpuName = models.CharField(max_length=100, help_text="Enter cpu name", verbose_name="ЦП")
    cpuDescription = models.TextField(help_text="Enter cpu description", verbose_name="описание ЦП")
    cpuManufacturer = models.ForeignKey('CPUmanufacturer', on_delete=models.CASCADE, verbose_name="внешняя ссылка на производителя")
    cpuPrice = models.IntegerField(verbose_name="цена центрального процессора")
    timeCpuCreated = models.DateField(auto_now_add=True, verbose_name="время создания ЦП")

    def get_absolute_url(self):
        return reverse('cpu-detail', args=[str(self.id)])


    def __str__(self):
        return f'{self.cpuName, self.cpuManufacturer, self.cpuPrice, self.timeCpuCreated}'