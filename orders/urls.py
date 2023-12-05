from django.urls import path
# .
from . import views


urlpatterns = [
    path('save-product/', views.SaveProductView.as_view(), name='save_product'),
    path('get-product/', views.GetProductView.as_view(), name='get_product'),
    path('get-product-list/', views.GetProductListView.as_view(), name='get_product_list'),
    path('update-stock/', views.UpdateProductStockView.as_view(), name='update_stock'),
    path('save-order/', views.SaveOrderView.as_view(), name='save_order'),
    path('delete-order/', views.DeleteOrderView.as_view(), name='delete_order'),
    path('get-order/', views.GetOrderDetailView.as_view(), name='get_order'),
    path('get-order-list/', views.GetOrderListView.as_view(), name='get_order_list')
]
