from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from app_cambio_divisas.services.usuarios import crear_empleado, service_iniciar_sesion, verify_islogged, service_cerrar_sesion
from app_cambio_divisas.services.divisas import service_crear_divisa, service_obtener_tipos_de_cambio, service_obtener_todas_las_divisas
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt
def index(request):
    top_nav_context = top_nav(request)
    
    divisas = service_obtener_todas_las_divisas(request)
    
    if request.method == 'GET' and 'cantidad' in request.GET:
        
        venta, compra = service_obtener_tipos_de_cambio(request)
        cantidad= request.GET.get('cantidad')
        abbr_primary = request.GET.get('abbr_primary')
        abbr_secondary = request.GET.get('abbr_secondary')
        resultado1 = (float(cantidad)*float(compra))
        resultado2 = (float(cantidad)/float(venta))
        
        return render(request, 'index.html', {
            'top_nav_context': top_nav_context,
            'resultado1': resultado1,
            'resultado2': resultado2,
            'divisas': divisas,
            'abbr_primary': abbr_primary,
            'abbr_secondary': abbr_secondary,
            'cantidad': cantidad,
        })
    print(top_nav_context)
    return render(request, 'index.html', {
            'top_nav_context': top_nav_context,
            'divisas': divisas,
        })

def top_nav(request):
    is_user_authenticated = verify_islogged(request)
    return {'is_user_authenticated': is_user_authenticated}

@csrf_exempt
def iniciar_sesion(request):
    if request.method == 'POST':
        response = service_iniciar_sesion(request)
        return response
    template = loader.get_template('iniciar-sesion.html')
    return HttpResponse(template.render())

@csrf_exempt
def cerrar_sesion(request):
    response = service_cerrar_sesion(request)
    return response

@csrf_exempt
def registrar_usuario(request):
    if request.method == 'POST':
        response = crear_empleado(request)
        return render(request, 'registrar-usuario.html', {'response': response})
    template = loader.get_template('registrar-usuario.html')
    return HttpResponse(template.render())

@csrf_exempt
def crear_divisas(request):
    top_nav_context = top_nav(request)
    if request.method == 'POST':
        response = service_crear_divisa(request)
        return render(request, 'divisas.html', top_nav_context)
    template = loader.get_template('divisas.html')
    return render(request, 'divisas.html', top_nav_context)