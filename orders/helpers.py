# .
from . import models, db_helpers, enums
from django.db import transaction


def save_product_info(product: dict):
    """
    Save product info in db

    Args:
        product: dict, product information
    Return:
        product_saved: object, product instance

    product{
        "id": int,
        "is_active": bool,
        "name": str,
        "price": float,
        "stock": int
    }
    """
    
    product_saved = ''
    # Create
    if not 'id' in product:
        product_saved = db_helpers.create_product(product)

    # Update
    else:
        product_saved = db_helpers.update_product(product)

    return product_saved


def get_product_by_id(product: dict):
    """
    Get product by product id

    Args:
        product: dict, product information
    Return:
        response: dict, product information

    product{
        "id": int
    }
    """

    response = models.Product.objects.values('name', 'price', 'stock', 'is_active').get(id=product['id'])

    return response


def get_product_list():
    """
    Get the product list

    Args:
        None
    Return:
        response: list, product information
    """

    response = models.Product.objects.values('name', 'price', 'stock', 'is_active').all()

    return response


def update_product_stock(product: dict):
    """
    Update product stock in db

    Args:
        product: dict, product information
    Return:
        None

    product{
        "id": int,
        "stock": int
    }
    """

    prod = models.Product.objects.get(id=product['id'])
    if not prod.is_active:
        raise Exception('Product is not active.')
    if not product['stock'] >= 0:
        raise Exception('Stock debe ser mayor o igual a cero.')
    
    response = db_helpers.update_product_stock_in_db(product)

    return response


def validate_duplicate_product(products: list):
    """
    Validate duplicate products in the Order
    
    Args:
        products: list, products in the Order
    Return:
        None

    products[{
        "product_id": int
    }]
    """
    
    checked_data = set()

    for product in products:
        id = product['product_id']
        if id in checked_data:
            raise Exception(f'El producto con id {id} esta duplicado.')
        checked_data.add(id)


def product_validations(product_instance: object, product_info: dict):
    """
    Product validations before save Order
    
    Args:
        product_instance: object, product instance
        product_info: dict, product information
    Return:
        None

    product_info{
        "quantity": int
    }
    """
    
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
    """
    Calculate the stock after a operation
    
    Args:
        product_info: dict, product information
        stock: int, product stock
    Return:
        None

    product_info{
        "product_id": int,
        "quantity": int
    }
    """

    # Update Product Stock
    new_stock = {
        'id': product_info['product_id'],
        'stock': stock - product_info['quantity']
    }
    product_updated = update_product_stock(new_stock)


def return_product_to_stock(order: object, product: dict):
    """
    Return product in the Order to Stock
    
    Args:
        order: object, Order instance
        product: dict, product information
    Return:
        None

    product{
        "product_id": int,
        "quantity": int
    }
    """

    product_stock = models.Product.objects.values('stock').get(id=product['product_id'])
    product_in_order = models.OrderDetail.objects.values('quantity').get(order=order, product__id=product['product_id'])
    new_stock = {
        'id':product['product_id'],
        'stock': product_stock['stock'] + product_in_order['quantity']
    }

    product_updated = update_product_stock(new_stock)


def save_order(order: dict):
    """
    Save order with it's products
    
    Args:
        order: dict, order information
    Return:
        order_saved: object, order instance

    order{
        "order": {
            "id": int,
            "order_status": str,
            "is_active": bool,
            "date_time": datetime
        },
        "products": [{
            "product_id": int,
			"quantity": int
        }]
    }
    """

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
    """
    Delete order (change status)
    
    Args:
        order: dict, order information
    Return:
        None

    order{
        "order": {
            "id": int
        }
    }
    """

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
    """
    Process Order Detail info with user format
    
    Args:
        order_info: object, order instance
        order_detail: object, orderDetail instance
    Return:
        response: dict, order detail
    """

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
    """
    Get Order Detail by id
    
    Args:
        order: dict, order information
    Return:
        response: dict, order detail
    """

    order_info = models.Order.objects.get(id=order['id'])
    order_detail = models.OrderDetail.objects.filter(order=order_info)

    response = process_orderdetail_format(order_info, order_detail)

    return response


def get_order_list():
    """
    Get List with Orders Detail
    
    Args:
        None
    Return:
        response: dict, order detail
    """

    response = list()
    orders_info = models.Order.objects.all()

    for order in orders_info:
        order_detail = models.OrderDetail.objects.filter(order=order.id)

        response.append(process_orderdetail_format(order, order_detail))
        
    return response
