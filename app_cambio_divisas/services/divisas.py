import requests
from django.http import JsonResponse, HttpResponse
import json
from django.template import loader
from django.shortcuts import render

import logging

logger = logging.getLogger(__name__)

base_url = 'https://api-metapod.onrender.com'

def service_obtener_todas_las_divisas(request):
    url=f'{base_url}/get/divisas'
    if request.method == 'GET':
        csrf_token = request.COOKIES.get('csrftoken')
        headers = {'X-CSRFToken': csrf_token}
        response_service = requests.get(url, headers=headers)
        divisas = []
        divisas.append(response_service.json())
        return divisas

def service_crear_divisa(request):
    url = f'{base_url}/post/divisa'
    if request.method == 'POST':
        data = request.POST
        token = request.COOKIES['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        response_service = requests.post(url, json=data, headers=headers)
        if response_service.status_code < 300:
            return 'Divisa creada exitosamente'
        else:
            return 'Error al crear la divisa'
        
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