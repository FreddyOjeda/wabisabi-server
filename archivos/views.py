from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .models import Producto 
from .serializers import ProductoSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def guardar_productos(request):
    if request.method == 'POST':
        productos = request.data  # Suponiendo que la lista de productos se envía en el cuerpo de la solicitud en formato JSON
        serializer = ProductoSerializer(data=productos, many=True)
        
        if serializer.is_valid():
            serializer.save()  # Guarda los productos en la base de datos
            return Response({'message': 'Productos guardados exitosamente'})
        else:
            return Response(serializer.errors, status=400) 

@csrf_exempt
def guardar_imagen(request):
    if request.method == 'POST':
        archivo = request.FILES['imagen']
        descripcion = request.POST.get('descripcion', '')
        precio = request.POST.get('precio', 0)
        print(precio)
        # Ruta en la que deseas guardar la imagen
        directorio_destino = settings.BASE_DIR/'products'  # Reemplaza con la ruta deseada

        # Si el directorio de destino no existe, créalo
        os.makedirs(directorio_destino, exist_ok=True)

        # Combina la ruta de destino con el nombre del archivo
        ruta_destino = os.path.join(directorio_destino, archivo.name)

        with open(ruta_destino, 'wb') as destination:
            for chunk in archivo.chunks():
                destination.write(chunk)
        ruta_destino = f'https://wabisabi-server-production.up.railway.app/products/{archivo.name}'

        # Crea un nuevo Producto y guárdalo en la base de datos
        producto = Producto(descripcion=descripcion, precio=precio, imagen=ruta_destino)
        producto.save()

        return JsonResponse({'message': 'Imagen guardada exitosamente','ruta':ruta_destino,'directorio':directorio_destino})
    return JsonResponse({'message': 'Error al guardar la imagen'})

@csrf_exempt
def borrar_productos(request):
    if request.method == 'POST':
        # Borra todos los productos
        Producto.objects.all().delete()
        return JsonResponse({'message': 'Todos los productos han sido eliminados'})
    return JsonResponse({'message': 'Solicitud no válida'})

@csrf_exempt
def borrar_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        producto.delete()
        return JsonResponse({'message': 'Producto borrado exitosamente'})
    except Producto.DoesNotExist:
        return JsonResponse({'message': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'message': 'Error al borrar el producto'}, status=500)

class ListaProductos(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer