# .
from . import models, enums


# Create Product
def create_product(product: dict) -> models.Product:

    product_instance = models.Product.objects.create(**product, is_active=True)

    return product_instance


# Update Product
def update_product(product: dict) -> models.Product:

    product_instance = models.Product.objects.get(id=product['id'])
    if 'price' in product:
        product_instance.price = product['price']
    if 'name' in product:
        product_instance.name = product['name']
    if 'is_active' in product:
        product_instance.is_active = product['is_active']
    product_instance.save()

    return product_instance


# Update Product stock
def update_product_stock_in_db(product: dict) -> models.Product:
    
    prod_updated = models.Product.objects.get(id=product['id'])
    prod_updated.stock = product['stock']
    prod_updated.save()

    return prod_updated


# Create Order
def create_order(order: dict) -> models.Order:

    new_order = models.Order.objects.create(**order, order_status=enums.OrderStatus.IN_PROCESS.value, is_active=True)

    return new_order


# Update Order
def update_order(order:dict) -> models.Order:

    order_instance = models.Order.objects.get(id=order['id'])
    if 'date_time' in order:
        order_instance.date_time = order['date_time']
    if 'order_status' in order:
        order_instance.order_status = order['order_status']
    if 'is_active' in order:
        order_instance.is_active = order['is_active']
    order_instance.save()

    return order_instance


# Create Order Detail
def create_orderdetail(order: object, product: dict) -> models.OrderDetail:

    orderdetail = models.OrderDetail.objects.create(
        order=order,
        quantity=product['quantity'],
        product=models.Product.objects.get(id=product['product_id'])
    )

    return orderdetail


# Update Order Detail
def update_orderdetail(order: object, product: dict) -> models.OrderDetail:
    
    order_detail = models.OrderDetail.objects.get(order=order, product_id=product['product_id'])
    order_detail.quantity = product['quantity']
    order_detail.save()

    return order_detail
