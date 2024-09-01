from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .models import Producto, Orders
import uuid
import json
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['POST'])
@csrf_exempt
def products(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            nombre = data.get('name')
            sku = data.get('sku') if data.get('sku') else str(uuid.uuid4())
            cantidad = 100
            
            nuevo_producto = Producto.objects.create(name=nombre, sku=sku, quantity=cantidad)
            
            return JsonResponse({'message': f"Producto '{nombre}' creado exitosamente con SKU: '{sku}' "}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e):
                return JsonResponse({'error': f'El SKU "{sku}" ya existe. Intenta con otro SKU o reenvía la petición.'}, status=400)
            else:
                return JsonResponse({'error': 'Error de integridad en la base de datos.'}, status=400)
        
        except KeyError as e:
            return JsonResponse({'error': f'Falta el campo requerido: {str(e)}'}, status=400)
        
    return HttpResponseNotAllowed(['POST'])


@api_view(['PATCH'])
@csrf_exempt
def inventories_product(request, product_id):
    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            cantidad = data.get("cantidad")
            
            if cantidad is None:
                return JsonResponse({'error': 'El campo "cantidad" es requerido.'}, status=400)
            if not isinstance(cantidad, int) or cantidad < 0:
                return JsonResponse({'error': 'El campo "cantidad" debe ser un entero positivo.'}, status=400)
            
            producto = get_object_or_404(Producto, id=product_id)
            
            nombre = producto.name
            producto.quantity += cantidad
            unidades = producto.quantity
            
            producto.save()
            
            return JsonResponse({'message': f'El stock del producto {nombre} se actualizado exitosamente a {unidades} unidades.'}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        
        except Http404:
            return JsonResponse({'error': f'Producto con ID: {product_id} no encontrado.'}, status=404)
        
        except KeyError as e:
            return JsonResponse({'error': f'Falta el campo requerido: {str(e)}'}, status=400)
        
    return HttpResponseNotAllowed(['PATCH'])


@api_view(['POST'])
@csrf_exempt
def orders(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            cantidad = data.get('quantity')
            
            if product_id is None or cantidad is None:
                return JsonResponse({'error': 'Los campos "product_id" y "quantity" son requeridos.'}, status=400)
            if not isinstance(cantidad, int) or cantidad <= 0:
                return JsonResponse({'error': 'El campo "quantity" debe ser un entero positivo mayor a 0.'}, status=400)
            
            producto = get_object_or_404(Producto, id=product_id)
            
            if producto.quantity < cantidad:
                return JsonResponse({'error': f'Stock insuficiente. Sólo quedan {producto.quantity} unidades.'}, status=400)
            
            nueva_orden = Orders.objects.create(product_id=producto, quantity=cantidad)
            
            producto.quantity -= cantidad
            producto.save()
            
            return JsonResponse({
                'message': 'Orden de compra creada exitosamente.',
                'order_id': nueva_orden.id,
                'remaining_stock': producto.quantity
            }, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        
        except Http404:
            return JsonResponse({'error': f'Producto con ID: {product_id} no encontrado.'}, status=404)
        
        except KeyError as e:
            return JsonResponse({'error': f'Falta el campo requerido: {str(e)}'}, status=400)
        
    return HttpResponseNotAllowed(['POST'])


def fallback(request):
    return HttpResponse("<h2> ---=== API para prueba técnica 3B ===--- </h2>")

def api_fallback(request):
    return HttpResponse("<h2> ---=== Fallback para el path:   api/ ===--- </h2>")

