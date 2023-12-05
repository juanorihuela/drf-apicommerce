from django.db import models
import requests


# Product
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()

    name = models.CharField(max_length=250)
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return f'Product: {self.name} - Stock: {self.stock}'


# Order
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    
    order_status = models.CharField(max_length=50)
    date_time= models.DateTimeField()

    def get_total(self):
        total = 0
        details = OrderDetail.objects.filter(order__id=self.id)
        for detail in details:
            total += detail.quantity * detail.product.price
        return total
    
    def get_total_usd(self):
        url = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
        total = 0

        response = requests.get(url)
        if not response.status_code == 200:
            return 'No disponible'
        element = next((item for item in response.json() if item['casa']['nombre'] == 'Dolar Blue'), None)
        dolar = float(element['casa']['compra'].replace(',', '.'))

        details = OrderDetail.objects.filter(order__id=self.id)
        for detail in details:
            total += (detail.quantity * detail.product.price) / dolar

        return total

    def __str__(self):
        return f'Order Id: {self.id}'


# Order Detail
class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()

    def __str__(self):
        return f'Detail for order {self.order.id}'
