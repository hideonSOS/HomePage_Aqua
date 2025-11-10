from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Schedule
from .forms import ScheduleForm

class ScheduleShow(TemplateView):
    template_name = 'input_page/input_page.html'


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'input_page/input.html'
    model = Schedule
    form_class = ScheduleForm
    success_url = reverse_lazy('input_page:input')
    login_url='/input_page/login/'

class ScheduleListView(LoginRequiredMixin,ListView):
    template_name = "input_page/list.html"
    model = Schedule
    # form_class = ScheduleForm
    login_url='/input_page/login/'
    context_object_name = 'schedule_list'
    

class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "input_page/delete.html"
    model = Schedule
    
    success_url = reverse_lazy('input_page:list')
    login_url='/input_page/login/'

class ScheduleUpdateView(TemplateView):
    template_name = "input_page/update.html"