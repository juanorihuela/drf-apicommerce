# .
from . import helpers
# DRF
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# Save Product
class SaveProductView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        product = request.data

        try:
            product_saved = helpers.save_product_info(product)
        except Exception as ex:
            return Response({'message': f'{ex}'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'product_id': product_saved.id}, status=status.HTTP_201_CREATED)


# Get Product
class GetProductView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        product = request.data

        try:
            response = helpers.get_product_by_id(product)
        except Exception as ex:
            return Response({'message': f'{ex}'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'product': response}, status=status.HTTP_200_OK)


# Product List
class GetProductListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            response = helpers.get_product_list()
        except Exception as ex:
            return Response({'message': f'{ex}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'products': response}, status=status.HTTP_200_OK)


# Update Stock
class UpdateProductStockView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        product = request.data

        try:
            response = helpers.update_product_stock(product)
        except Exception as ex:
            return Response({'message': f'{ex}'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'product': response.name, 'stock_updated': response.stock}, status=status.HTTP_200_OK)


# Save Order
class SaveOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        order = request.data

        try:
            response = helpers.save_order(order)
        except Exception as ex:
            return Response({'message': f'{ex}'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'order': response.id}, status=status.HTTP_200_OK)


# Delete Order
class DeleteOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        order= request.data

        try:
            response = helpers.delete_order(order)
        except Exception as ex:
            return Response({'message': f'{ex}'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK)


# Get Order
class GetOrderDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        order = request.data

        try:
            response = helpers.get_order_by_id(order)
        except Exception as ex:
            return Response({'message': f'{ex}'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'order': response}, status=status.HTTP_200_OK)


# Get Order List
class GetOrderListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            response = helpers.get_order_list()
        except Exception as ex:
            return Response({'message': f'{ex}'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'orders': response}, status=status.HTTP_200_OK)
