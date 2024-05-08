from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from app_cambio_divisas.services.usuarios import crear_empleado, service_iniciar_sesion, verify_islogged, service_cerrar_sesion
from app_cambio_divisas.services.divisas import service_crear_divisa, service_obtener_tipos_de_cambio, service_obtener_todas_las_divisas, service_obtener_todos_los_tipos_de_cambio, service_actualizar_tipo_de_cambio
from app_cambio_divisas.services.productos import service_obtener_todos_los_productos, service_crear_producto
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt
def index(request):
    top_nav_context = top_nav(request)
    
    divisas = service_obtener_todas_las_divisas(request)
    
    if request.method == 'GET' and 'cantidad' in request.GET:
        abbr_primary = request.GET.get('abbr_primary')
        abbr_secondary = request.GET.get('abbr_secondary')
        if abbr_primary == abbr_secondary:
            mensaje='No se puede calcular el tipo de cambio de la misma moneda'
            messages.error(request, mensaje)
            return render(request, 'index.html', {
            'top_nav_context': top_nav_context,
            'divisas': divisas,
            'abbr_primary': abbr_primary,
            'abbr_secondary': abbr_secondary,
        })
        venta, compra = service_obtener_tipos_de_cambio(request)
        cantidad= request.GET.get('cantidad')
        
        resultado1 = (float(cantidad)*float(compra))
        
        return render(request, 'index.html', {
            'top_nav_context': top_nav_context,
            'resultado1': resultado1,
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
        return response
    template = loader.get_template('registrar-usuario.html')
    return HttpResponse(template.render())

@csrf_exempt
def crear_divisas(request):
    top_nav_context = top_nav(request)
    if request.method == 'POST':
        response = service_crear_divisa(request)
        return render(request, 'divisas.html', top_nav_context)
    template = loader.get_template('divisas.html')
    return render(request, 'divisas.html', {
            'top_nav_context': top_nav_context,
            })

@csrf_exempt
def crear_productos(request):
    top_nav_context = top_nav(request)
    if request.method == 'POST':
        response = service_crear_producto(request)
        return render(request, 'productos.html', top_nav_context)
    template = loader.get_template('productos.html')
    return render(request, 'productos.html', {
            'top_nav_context': top_nav_context,
            })

@csrf_exempt
def index_divisas(request):
    top_nav_context = top_nav(request)
    divisas = service_obtener_todos_los_tipos_de_cambio(request)
    return render(request, 'index-divisas.html', {
        'top_nav_context': top_nav_context,
        'divisas': divisas,
    })

@csrf_exempt
def index_productos(request):
    top_nav_context = top_nav(request)
    productos = service_obtener_todos_los_productos(request)
    return render(request, 'index-productos.html', {
        'top_nav_context': top_nav_context,
        'productos': productos,
    })

@csrf_exempt
def edit_divisas(request, abbr_primary, abbr_secondary):
    top_nav_context = top_nav(request)
    if request.method == 'POST':
        response = service_actualizar_tipo_de_cambio(request, abbr_primary, abbr_secondary)
        return response
    return render(request, 'edit-divisas.html', {
        'top_nav_context': top_nav_context,
        'abbr_primary': abbr_primary,
        'abbr_secondary': abbr_secondary,
    })