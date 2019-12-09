"""ventas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
                    VentasPronostico, 
                    RegistroVentaView, 
                    PronosticoCompra, 
                    PronosticoGeneral, 
                    ErrorPronostico,
                    UserCreateView,
                    UserUpdateView,
                    UserDeleteView,
                    EntrenarRedView,
                    ServicioView,
                    ServicioUpdateView,
                    ServiciosView,
                    ServicioDeleteView,
                    VentasView,
                    VentaUpdateView,
                    VentaDeleteView,
                    RedesView)

urlpatterns = [
    path('ventas_pronostico/<str:periodo>/', VentasPronostico.as_view(), name='ventas_pronostico'),
    path('registro_venta', RegistroVentaView.as_view(), name='registro_venta'),
    path('pronostico_compra/<str:periodo>/', PronosticoCompra.as_view(), name='pronostico_compra'),
    path('pronostico_general/<str:periodo>/<str:clasificacion>/', PronosticoGeneral.as_view(), name='pronostico_general'),
    path('error_pronostico/<str:periodo>/', ErrorPronostico.as_view(), name='error_pronostico'),
    path('servicio', ServicioView.as_view(), name='servicio'),
    path('servicio_update/<int:pk>', ServicioUpdateView.as_view(), name='servicio_update'),
    path('servicio_delete/<int:pk>', ServicioDeleteView.as_view(), name='servicio_delete'),
    path('servicios', ServiciosView.as_view(), name='servicios'),
    path('venta_update/<int:pk>', VentaUpdateView.as_view(), name='venta_update'),
    path('venta_delete/<int:pk>', VentaDeleteView.as_view(), name='venta_delete'),
    path('ventas', VentasView.as_view(), name='ventas'),
    path('redes', RedesView.as_view(), name='redes'),

    #Sign up
    path('add_user/', UserCreateView.as_view(), name='add_user'),
    path('update_user/<int:pk>', UserUpdateView.as_view(), name='update_user'),
    path('delete_user/<int:pk>', UserDeleteView.as_view(), name='delete_user'),

    #Red neuronal
    path('entrenar_red/', EntrenarRedView.as_view(), name='entrenar_red'),
]
