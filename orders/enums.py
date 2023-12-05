from enum import Enum


# Order Status
class OrderStatus(Enum):

    IN_PROCESS = 'En proceso'
    CANCELED = 'Cancelado'
    CLOSED = 'Cerrado'
