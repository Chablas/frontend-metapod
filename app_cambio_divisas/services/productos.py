import requests
from django.http import JsonResponse, HttpResponse
import json
from django.template import loader
from django.shortcuts import render, redirect

import logging

logger = logging.getLogger(__name__)

#base_url = 'https://api-metapod.onrender.com'
base_url = 'http://127.0.0.1:8000'

def service_obtener_todos_los_productos(request):
    url=f'{base_url}/get/productos'
    if request.method == 'GET':
        csrf_token = request.COOKIES.get('csrftoken')
        headers = {'X-CSRFToken': csrf_token}
        response_service = requests.get(url, headers=headers)
        productos = []
        productos.append(response_service.json())
        return productos

def service_crear_producto(request):
    url = f'{base_url}/post/producto'
    if request.method == 'POST':
        data = request.POST
        token = request.COOKIES['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        response_service = requests.post(url, json=data, headers=headers)
        if response_service.status_code < 300:
            return 'Producto creado exitosamente'
        else:
            return 'Error al crear el producto'
        
def service_obtener_tipos_de_cambio(request):
    if request.method == 'GET':
        abbr_primary = request.GET.get('abbr_primary')
        abbr_secondary = request.GET.get('abbr_secondary')
        url = f'{base_url}/get/{abbr_primary}/tipo_cambio/{abbr_secondary}'
        data={
            'abbr_primary':abbr_primary,
            'abbr_secondary':abbr_secondary,
        }
        response_service = requests.get(url, data=data)
        json_data = response_service.json()
        dato = json_data.get('dato', {})
        venta = dato.get('venta')
        compra = dato.get('compra')
        return venta, compra
    
def service_obtener_todos_los_tipos_de_cambio(request):
    url = f'{base_url}/get/all/tipo_cambio'
    csrf_token = request.COOKIES.get('csrftoken')
    headers = {'X-CSRFToken': csrf_token}
    response_service = requests.get(url, headers=headers)
    divisas = []
    divisas.append(response_service.json())
    return divisas

def service_actualizar_tipo_de_cambio(request, abbr_primary, abbr_secondary):
    url = f'{base_url}/put/divisa/tipo_cambio'
    token = request.COOKIES['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    data={
            'abbr_primary':abbr_primary,
            'abbr_secondary':abbr_secondary,
            'compra': request.POST.get('compra'),
            'venta': request.POST.get('venta'),
        }
    response_service = requests.put(url, json=data, headers=headers)
    divisas = []
    divisas.append(response_service.json())
    response = redirect('/divisas')
    return response