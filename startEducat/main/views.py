from django.shortcuts import render
from .models import CPU, CPUmanufacturer
from django.views import generic


def index(request):
    num_cpu = CPU.objects.all().count()
    num_cpumanufaturer = CPUmanufacturer.objects.all().count()
    return render(request,
                  'main/index.html',
                  context={
                      'num_cpu': num_cpu, 'num_cpumanufacturer': num_cpumanufaturer
                  })


def about(request):
    return render(request, 'main/about.html',)


class Cpus(generic.ListView):
    model = CPU
    # context_object_name = 'my_cpu_list'
    # queryset = CPU.objects.all()
    template_name = 'main/cpus.html'
    paginate_by = 10


class CpuDetailView(generic.DetailView):
    model = CPU
    template_name = 'main/cpu-detail.html'


class CpumanufacDetailView(generic.DetailView):
    model = CPUmanufacturer
    template_name = 'main/cpumanufac-detail.html'
