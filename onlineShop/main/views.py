import logging
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import *
from main.serializers import *
from django.shortcuts import get_object_or_404, get_list_or_404, render

logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        querySet = Category.objects.all()
        serializer = CategorySerializer(querySet, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        querySet = Category.objects.all()
        user = get_object_or_404(querySet, pk=pk)
        serializer = CategorySerializer(user)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, permission_classes=(IsAdminUser,))
    def create(self, request):
        category_data = request.data
        new_category = Category.objects.create(category_name=category_data['category_name'])
        new_category.save()
        serializer = CategorySerializer(new_category)
        # logger.debug(f'Category object created, ID: {serializer.instance}')
        # logger.info(f'Category object created, ID: {serializer.instance}')
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            instance = Category.objects.get(id=pk)
            instance.delete()
            logger.debug(f'Category object deleted, ID: {instance}')
            logger.info(f'Category object deleted, ID: {instance}')
        except Http404:
            logger.error(f'Category object cannot be deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['PUT'], detail=False, permission_classes=(IsAdminUser,))
    def update(self, request, pk):
        category = Category.objects.get(id=pk)
        category.category_name = request.data['category_name']
        category.save()
        serializer = CategorySerializer(category)
        logger.debug(f'Category object updated, ID: {serializer.instance}')
        logger.info(f'Category object updated, ID: {serializer.instance}')
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.filter(category=pk)
        user = get_list_or_404(queryset)
        serializer = ProductSerializer(user, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, permission_classes=(IsAdminUser,))
    def create(self, request):
        data = request.data
        category = Category.objects.get(id=data['category'])
        new_product = Product.objects.create(title=data['title'], price=data['price'],
                                           description=data['description'], category=category)
        new_product.save()
        serializer = ProductSerializer(new_product)
        logger.debug(f'Item object created, ID: {serializer.instance}')
        logger.info(f'Item object created, ID: {serializer.instance}')
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            instance = Product.objects.get(id=pk)
            instance.delete()
            logger.debug(f'Item object deleted, ID: {instance}')
            logger.info(f'Item object deleted, ID: {instance}')
        except Http404:
            logger.error(f'Item object cannot be deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)

    def select(self, request, pk=None):
        queryset = Product.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(user)
        return Response(serializer.data)

    @action(methods=['PUT'], detail=False, permission_classes=(IsAdminUser,))
    def update(self, request, pk, form=None):
        product = Product.objects.get(id=pk)
        product.title = request.data['title']
        product.price = request.data['price']
        product.description = request.data['description']
        #category = Category.objects.get(category_name=request.data['category'])
        #product.category = category
        product.save()
        serializer = ProductSerializer(product)
        logger.debug(f'Item object updated, ID: {serializer.instance}')
        logger.info(f'Item object updated, ID: {serializer.instance}')
        return Response(serializer.data)


class CartAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Cart.objects.get(customer_id=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request):
        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'ingCart object updated, ID: {serializer.instance}')
            logger.info(f'Cart object updated, ID: {serializer.instance}')
            return Response(serializer.data)
        logger.error(f'Cart object cannot be updated')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart = self.get_object(pk)
        cart.delete()
        logger.debug(f'ShoppingCart object deleted')
        logger.info(f'ShoppingCart object deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt

def cart_detail(request, pk):
    if request.method == 'GET':
        cart_item = Cart.objects.get(pk=pk)
        serializer = CartSerializer(cart_item)

        return JsonResponse(serializer.data)


class OrderAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order= self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'Order object updated, ID: {serializer.instance}')
            logger.info(f'Order object updated, ID: {serializer.instance}')
            return Response(serializer.data)
        logger.error(f'Order object cannot be updated, {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, pk):
                order = self.get_object(pk)
                order.delete()
                logger.debug(f'Order object deleted')
                logger.info(f'Order object deleted')
                return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def orders(request):
    if request.method == 'GET':
        all_orders = Order.objects.all()
        serializer = OrderSerializer(all_orders, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        json_data = JSONParser().parse(request)
        serializer = OrderSerializer(data=json_data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'Order object created, ID: {serializer.instance}')
            logger.info(f'Order object created, ID: {serializer.instance}')
            return JsonResponse(serializer.data, safe=False)
        else:
            logger.error(f'Order object cannot be created, {serializer.errors}')
            return JsonResponse(serializer.errors, safe=False)
