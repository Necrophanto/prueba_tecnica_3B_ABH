from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from .models import Producto, Orders
import json

# Create your tests here.

class ApiTests(TestCase):

    def setUp(self):
        # Crear un producto para usar en las pruebas
        self.producto = Producto.objects.create(name="Producto Pruebas Unitarias", sku="1234567890", quantity=500)
        self.order_data = {"product_id": self.producto.id, "quantity": 100}

    def test_create_product(self):
        url = reverse('products')  # Asegúrate de que la URL coincida con la que usas en urls.py
        data = {"sku": "0987654321", "name": "Nuevo Producto"}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Producto 'Nuevo Producto' creado exitosamente", response.json().get('message'))

    def test_update_inventory(self):
        url = reverse('inventories_product', kwargs={'product_id': self.producto.id})
        data = {"cantidad": 350}
        response = self.client.patch(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.producto.refresh_from_db()  # Refresca el objeto producto desde la base de datos
        self.assertEqual(self.producto.quantity, 850)

    def test_create_order(self):
        url = reverse('orders')
        response = self.client.post(url, json.dumps(self.order_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.quantity, 400)
        self.assertTrue('order_id' in response.json())

    def test_create_order_insufficient_stock(self):
        url = reverse('orders')
        data = {"product_id": self.producto.id, "quantity": 1000}  # Excede el stock disponible
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Stock insuficiente", response.json().get('error'))