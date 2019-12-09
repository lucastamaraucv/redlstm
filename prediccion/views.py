from django.shortcuts import render
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .forms import RegistroVentaForm, CustomUserCreationForm, EntrenarRedForm, ServicioForm
from django.views.generic import ListView
from django.views.generic import TemplateView

from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)

from .models import RedNeuronalResultados, RegistroVenta, Servicio, DatosRedNeuronalTrain, DatosRedNeuronalTest

# User manage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy

from .func import train_nn, populate_days, get_weeks, get_months, get_nn_tipos, get_future
from multiprocessing import Pool

from decimal import Decimal
import numpy as np

@method_decorator(login_required, name='dispatch')
class VentasPronostico(TemplateView):
    template_name = "ventas_pronostico.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = self.kwargs['periodo']
        queryset = RedNeuronalResultados.objects.filter(periodo=periodo, clasificacion='GENERAL').order_by('-id')[:1]
        queryset3 = DatosRedNeuronalTrain.objects.filter(entrenamiento=queryset[0]).order_by('id')
        context['objects'] = queryset
        context['datos'] = queryset3
        return context

@method_decorator(login_required, name='dispatch')
class PronosticoCompra(TemplateView):
    template_name = "pronostico_compra.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = self.kwargs['periodo']
        queryset = RedNeuronalResultados.objects.filter(periodo=periodo, clasificacion='GENERAL').order_by('-id')[:1]
        queryset3 = DatosRedNeuronalTrain.objects.filter(entrenamiento=queryset[0]).order_by('id')
        context['objects'] = queryset
        context['datos'] = queryset3
        return context

@method_decorator(login_required, name='dispatch')
class PronosticoGeneral(TemplateView):
    template_name = "pronostico_general.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = self.kwargs['periodo']
        clasificacion = self.kwargs['clasificacion']
        queryset = RedNeuronalResultados.objects.filter(periodo=periodo, clasificacion=clasificacion).order_by('-id')[:1]
        queryset2 = Servicio.objects.all()
        try:
            queryset3 = DatosRedNeuronalTrain.objects.filter(entrenamiento=queryset[0]).order_by('id')
            queryset4 = DatosRedNeuronalTest.objects.filter(entrenamiento=queryset[0]).order_by('id')
            context['train'] = queryset3
            context['test'] = queryset4
        except:
            pass
        context['periodo_anterior'] = periodo
        context['clasificacion_anterior'] = clasificacion
        context['objects'] = queryset
        context['servicios'] = queryset2
        return context

@method_decorator(login_required, name='dispatch')
class ErrorPronostico(TemplateView):
    template_name = "error_pronostico.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = self.kwargs['periodo']
        queryset = RedNeuronalResultados.objects.filter(periodo=periodo, clasificacion='GENERAL').order_by('-id')[:1]
        queryset3 = DatosRedNeuronalTrain.objects.filter(entrenamiento=queryset[0]).order_by('id')
        context['objects'] = queryset
        context['train'] = queryset3
        return context

@method_decorator(login_required, name='dispatch')
class RegistroVentaView(CreateView):
    template_name = 'registro_venta.html'
    form_class = RegistroVentaForm

    def get_success_url(self):
        return reverse_lazy('registro_venta')


@method_decorator(login_required, name='dispatch')
class ServicioView(CreateView):
    template_name = 'servicio.html'
    form_class = ServicioForm

    def get_success_url(self):
        return reverse_lazy('servicio')
        

@method_decorator(login_required, name='dispatch')
class ServicioUpdateView(UpdateView):
    template_name = 'servicio_update.html'
    form_class = ServicioForm

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Servicio.objects.filter(id=pk)
        return queryset
    
    def get_success_url(self):
        return reverse_lazy('servicios')

@method_decorator(login_required, name='dispatch')
class ServicioDeleteView(DeleteView):
    model = Servicio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        queryset = Servicio.objects.get(id=pk)
        context['object'] = queryset
        return context

    def get_success_url(self):
        return reverse_lazy('servicios')

@method_decorator(login_required, name='dispatch')
class ServiciosView(TemplateView):
    template_name = "servicios.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Servicio.objects.all()
        context['objects'] = queryset
        return context

@method_decorator(login_required, name='dispatch')
class VentasView(TemplateView):
    template_name = "ventas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = RegistroVenta.objects.all()
        context['objects'] = queryset
        return context

@method_decorator(login_required, name='dispatch')
class RedesView(TemplateView):
    template_name = "redes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = RedNeuronalResultados.objects.all()
        context['objects'] = queryset
        return context
        

@method_decorator(login_required, name='dispatch')
class VentaUpdateView(UpdateView):
    template_name = 'venta_update.html'
    form_class = RegistroVentaForm

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = RegistroVenta.objects.filter(id=pk)
        return queryset
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        queryset = RegistroVenta.objects.get(id=pk)
        context['object'] = queryset
        return context

    def get_success_url(self):
        return reverse_lazy('ventas')

@method_decorator(login_required, name='dispatch')
class VentaDeleteView(DeleteView):
    model = RegistroVenta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        queryset = RegistroVenta.objects.get(id=pk)
        context['object'] = queryset
        return context

    def get_success_url(self):
        return reverse_lazy('ventas')


@method_decorator(login_required, name='dispatch')
class EntrenarRedView(CreateView):
    template_name = 'entrenar_red.html'
    form_class = EntrenarRedForm

    def form_valid(self, form):
        periodo = form.cleaned_data['periodo']
        look_back = form.cleaned_data['look_back']
        neuronas = form.cleaned_data['neuronas']
        epocas = form.cleaned_data['epocas']
        clasificacion = form.cleaned_data['clasificacion']
        data_date = []
        data_price = []
        data_type = []

        if clasificacion=='GENERAL':
            ventas = RegistroVenta.objects.all().order_by('fecha')
            clasificacion = "VENTAS"
        else:
            ventas = RegistroVenta.objects.filter(tipo=clasificacion).order_by('fecha')

        if  clasificacion=='GENERAL':
            fecha = [ventas[0].fecha]
            precio = [ventas[0].precio]
            for i in ventas:
                if not i.fecha in fecha:
                    data_date.append(fecha[-1])
                    data_price.append(np.sum(np.array(precio)))
                    data_type.append('GENERAL')
                    precio = []
                    fecha.append(i.fecha)
                else:
                    precio.append(i.precio)
        else:
            for i in ventas:
                data_date.append(i.fecha)
                data_price.append(i.precio)
                data_type.append(i.tipo)

        #if clasificacion == "PRECIOS":
        if periodo == 'DIAS':
            data_date, data_price, nn_descriptions, nn_firms, nn_rucs = populate_days(data_date, data_price)
            future = get_future(data_date, 'DIAS')
            
        if periodo == 'SEMANAS':
            data_date, data_price, nn_descriptions, nn_firms, nn_rucs = populate_days(data_date, data_price)
            future = get_future(data_date, 'SEMANAS')
            data_date, data_price = get_weeks(data_date, data_price)

        if periodo == 'MESES':
            data_date, data_price, nn_descriptions, nn_firms, nn_rucs = populate_days(data_date, data_price)
            future = get_future(data_date, 'MESES')
            data_date, data_price = get_months(data_date, data_price)

        pool = Pool(processes=8)   
        trainPredict, testPredict, future, dam, pema, rmse, real, fecha = pool.apply(train_nn, [data_price, data_date, look_back, neuronas, epocas, periodo, clasificacion])

        self.object = RedNeuronalResultados.objects.create(periodo=periodo, look_back=look_back, neuronas=neuronas, epocas=epocas, clasificacion=clasificacion)

        form.instance.id = self.object.id

        for i in range(len(trainPredict)):
            DatosRedNeuronalTrain.objects.create(precio=trainPredict[i][0], entrenamiento=self.object, dam=dam[i][0], pema=pema[i][0], rmse=rmse[i][0], real=real[i][0], fecha=fecha[i])

        for i in range(len(testPredict)):
            DatosRedNeuronalTest.objects.create(precio=testPredict[i][0], entrenamiento=self.object, future=future[i])
    
        return super(EntrenarRedView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('entrenar_red')


# Vistors register (Sign up)


class UserCreateView(BSModalCreateView):
    template_name = "registration/create_user.html"
    form_class = CustomUserCreationForm
    success_message = 'Éxito: La cuenta fue creada.'

    def get_success_url(self, **kwargs):
        return reverse_lazy('login')

@method_decorator(login_required, name='dispatch')
class UserUpdateView(BSModalUpdateView):
    model = User
    template_name = 'registration/update.html'
    form_class = CustomUserCreationForm
    success_message = 'Éxito: La cuenta fue editada.'

    def get_success_url(self, **kwargs):
        return reverse_lazy('login')

@method_decorator(login_required, name='dispatch')
class UserDeleteView(BSModalDeleteView):
    model = User
    template_name = 'registration/delete.html'
    success_message = 'Éxito: La cuenta fue eliminada.'

    def get_success_url(self, **kwargs):
        return reverse_lazy('login')




