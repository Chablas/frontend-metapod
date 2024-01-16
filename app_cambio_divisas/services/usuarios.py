import requests
from django.http import JsonResponse, HttpResponse
import json
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages

base_url = 'https://api-metapod.onrender.com'
create_user_url = f'{base_url}/post/usuarios'
obtain_token_url = f'{base_url}/auth/token'
login_state_url = f'{base_url}/put/login'

def service_iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'scope': '',
            'client_id': '',
            'client_secret': '',
        }
        data2 = {
            'email': username,
        }
        
        csrf_token = request.COOKIES.get('csrftoken')
        headers = {'X-CSRFToken': csrf_token, 'Content-Type': 'application/x-www-form-urlencoded'}
        response_create_user = requests.post(obtain_token_url, data=data, headers=headers)
        if response_create_user.status_code >= 400:
            messages.error(request, "Hubo un error al intentar procesar la operación")
            context = {
                'mensaje_error': 'Error al iniciar sesión'
            }
            response = render(request, 'iniciar-sesion.html', context)
            return response
        data2_json = json.dumps(data2)
        headers = {'Content-Type': 'application/json', 'X-CSRFToken': csrf_token}
        response_islogged = requests.put(login_state_url, data=data2_json, headers=headers)
        if response_islogged.status_code >= 400:
            response = render(request, 'iniciar-sesion.html', context)
            return response
        aasdasdas = guardar_email_en_cookie(username)
        if response_create_user.status_code < 300:
            context = {
                'mensaje_error': 'Error al iniciar sesión'
            }
            response = redirect('/conversor')
            response.set_cookie('access_token', response_create_user.json()['access_token'], httponly=True, secure=True, samesite='Lax')
            response.set_cookie('usuario_email', username, httponly=True, secure=True, samesite='Lax')
            return response
        else:
            return HttpResponse('Error al iniciar sesión')
    else:
        return HttpResponse('Error')

def crear_empleado(request):
    if request.method == 'POST':
        data = request.POST
        csrf_token = request.COOKIES.get('csrftoken')
        headers = {'X-CSRFToken': csrf_token}
        response_create_user = requests.post(create_user_url, json=data, headers=headers)
        if response_create_user.status_code < 300:
            return 'Usuario creado exitosamente'
        else:
            return 'Error al crear el usuario'
    else:
        return 'Error'
    
def verify_islogged(request):
    try:
        email = obtener_email_de_cookie(request)
        if email == False:
            return False
        url = f'{base_url}/get/usuario/{email}'
        token = request.COOKIES['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        respuesta = requests.get(url, headers=headers)
        json_respuesta = respuesta.json()
        respuesta_islogged = json_respuesta.get('dato')
        response = respuesta_islogged.get('islogged')
        if response:
            return True
        else:
            return False
    except:
        return False
    
def guardar_email_en_cookie(email):
    response = HttpResponse("Email guardado en la cookie")
    response.set_cookie('usuario_email', email)
    return response

def obtener_email_de_cookie(request):
    try:
        email = request.COOKIES['usuario_email']
        return email
    except:
        return False
    
def service_cerrar_sesion(request):
    url = f'{base_url}/put/logout'
    token = request.COOKIES['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    username = request.COOKIES['usuario_email']
    data2 = {
            'email': username,
        }
    data2_json = json.dumps(data2)
    respuesta = requests.put(url, data=data2_json, headers=headers)
    response = redirect('/conversor')
    return response