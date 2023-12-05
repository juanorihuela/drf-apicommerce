# .
from . import models, db_helpers, enums
from django.db import transaction


def save_product_info(product: dict):
    
    product_saved = ''
    # Create
    if not 'id' in product:
        product_saved = db_helpers.create_product(product)

    # Update
    else:
        product_saved = db_helpers.update_product(product)

    return product_saved


def get_product_by_id(product: dict):

    response = models.Product.objects.values('name', 'price', 'stock', 'is_active').get(id=product['id'])

    return response


def get_product_list():

    response = models.Product.objects.values('name', 'price', 'stock', 'is_active').all()

    return response


def update_product_stock(product: dict):

    prod = models.Product.objects.get(id=product['id'])
    if not prod.is_active:
        raise Exception('Product is not active.')
    if not product['stock'] >= 0:
        raise Exception('Stock debe ser mayor o igual a cero.')
    
    response = db_helpers.update_product_stock_in_db(product)

    return response


def validate_duplicate_product(products: dict):
    checked_data = set()

    for product in products:
        id = product['product_id']
        if id in checked_data:
            raise Exception(f'El producto con id {id} esta duplicado.')
        checked_data.add(id)


def product_validations(product_instance: object, product_info: dict):
    
    # Quantity
    if not product_info['quantity'] > 0:
        raise Exception(f'El producto {product_instance.name} debe contener al menos una pieza.')
    # Stock
    if not product_instance.stock >= product_info['quantity']:
        raise Exception(f'No hay suficiente stock para surtir orden del pedido {product_instance.name}')
    # Is active
    if not product_instance.is_active:
        raise Exception(f'El producto {product_instance.name} no esta disponible.')


def calculate_new_stock(product_info: dict, stock: int):
    # Update Product Stock
    new_stock = {
        'id': product_info['product_id'],
        'stock': stock - product_info['quantity']
    }
    product_updated = update_product_stock(new_stock)


def return_product_to_stock(order: object, product: dict):

    product_stock = models.Product.objects.values('stock').get(id=product['product_id'])
    product_in_order = models.OrderDetail.objects.values('quantity').get(order=order, product__id=product['product_id'])
    new_stock = {
        'id':product['product_id'],
        'stock': product_stock['stock'] + product_in_order['quantity']
    }

    product_updated = update_product_stock(new_stock)


def save_order(order: dict):

    order_saved = ''

    with transaction.atomic():
        # Create
        if not 'id' in order['order']:
            if not 'products' in order:
                raise Exception('La orden debe contener al menos un producto.')
            validate_duplicate_product(order['products'])

            # Create Order
            order_saved = db_helpers.create_order(order['order'])

            for product_info in order['products']:
                # Validate Product
                prod_instance = models.Product.objects.get(id=product_info['product_id'])
                product_validations(prod_instance, product_info)
                
                # Create Order detail
                orderdetail = db_helpers.create_orderdetail(order_saved, product_info)

                # Update Product Stock
                calculate_new_stock(product_info, prod_instance.stock)

        # Update
        else:
            # Update Order
            order_saved = db_helpers.update_order(order['order'])

            if 'products' in order:
                for product_info in order['products']:
                    # Return products to stock & validate
                    return_product_to_stock(order_saved, product_info)
                    prod_instance = models.Product.objects.get(id=product_info['product_id'])
                    product_validations(prod_instance, product_info)

                    # Update Orderdetail
                    orderdetail_updated = db_helpers.update_orderdetail(order_saved, product_info)

                    # Update Product Stock
                    calculate_new_stock(product_info, prod_instance.stock)

    return order_saved


def delete_order(order: dict):

    if not order['order']['id']:
        raise Exception('Debe incluir el Id de la orden a eliminar.')
    if models.Order.objects.get(id=order['order']['id'], is_active=False):
        raise Exception('La orden ya esta eliminada.')

    order['order']['is_active'] = False
    order['order']['order_status'] = enums.OrderStatus.CANCELED.value

    # Update Order
    order_deleted = db_helpers.update_order(order['order'])

    # Products
    orderdetails = models.OrderDetail.objects.filter(order=order_deleted)
    for odetail in orderdetails:
        prod = {
            'product_id': odetail.product.id
        }

        return_product_to_stock(order_deleted, prod)


def process_orderdetail_format(order_info: object, order_detail: object):

    response = {
        'id': order_info.id,
        'date_time': order_info.date_time,
        'is_active': order_info.is_active,
        'order_status': order_info.order_status,
        'last_updated': order_info.updated,
        'total': order_info.get_total(),
        'total_usd': order_info.get_total_usd()
    }

    products = list()
    for detail in order_detail:
        prod = {
            'product': detail.product.name,
            'product_price': detail.product.price,
            'quantity': detail.quantity
        }
        products.append(prod)
    response['products'] = products

    return response


def get_order_by_id(order: dict):

    order_info = models.Order.objects.get(id=order['id'])
    order_detail = models.OrderDetail.objects.filter(order=order_info)

    response = process_orderdetail_format(order_info, order_detail)

    return response


def get_order_list():

    response = list()
    orders_info = models.Order.objects.all()

    for order in orders_info:
        order_detail = models.OrderDetail.objects.filter(order=order.id)

        response.append(process_orderdetail_format(order, order_detail))
        
    return response
