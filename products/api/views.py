from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action, permission_classes
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, BarSerializer
from products.models import Product, Bar
from .permissions import IsFactory, IsOwnerProduct, IsFreight, IsDriver
from accounts.models import FactoryMember


class ProductViewSet(ViewSet):

    def list(self, request):
        """
        The freight company can see the list of products of
         the manufacturing factories in which it is a member
        :param request:
        :return:
        """
        factories_company = FactoryMember.objects.filter(freight=request.user).values_list('factory')
        products = get_list_or_404(Product, factory_company__in=list(factories_company))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(factory_company=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"Message": f"Delete Product with ID {product.title}"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def product_list_each_company(self, request):
        """  factory
        Each factory can see its product list
        :param request:
        :return:
        """
        products = get_list_or_404(Product, factory_company=request.user, factory_company__role='factory')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsFactory]
        elif self.request.method in ['PATCH', 'DELETE']:
            permission_classes = [IsOwnerProduct]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class BarViewSet(ViewSet):
    def list(self, request):
        """
        Shows the list of bills of lading to the manufacturing plant
        :param request:
        :return:
        """
        bars = Bar.objects.select_related('product').filter(product__factory_company=request.user)
        serializer = BarSerializer(bars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Shipping companies can register a new bill of lading
        :param request:
        :return:
        """
        serializer = BarSerializer(data=request.data)
        if serializer.is_valid():
            product_id, product_amount = request.data['product'], request.data['amount']
            product = Product.objects.get(pk=product_id)
            product.amount -= product_amount
            if product.amount == 0: product.status = "close"
            product.save()
            serializer.save(freight=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def bar_confirmation(self, request):
        """
        The manufacturing plant can confirm the bill of lading
        :param request:
        :return:
        """
        barcode, status = request.data["barcode"], request.data["status"]
        bar = get_object_or_404(
            Bar.objects.select_related('product'),
            barcode__exact=barcode,
            product__factory_company=request.user
        )
        bar.status = status
        bar.save()
        return Response({
            'barcode': bar.barcode,
            'status': bar.status
        })

    @action(detail=False, methods=["get"])
    def list_bars_driver(self, request):
        """
        Every driver can see the list of her loads
        :param request:
        :return:
        """
        bars = get_list_or_404(Bar, driver=request.user)
        serializer = BarSerializer(bars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.request.method == "POST" and self.action == "bar_confirmation":
            permission_classes = [IsFactory]
        elif self.request.method == "GET" and self.action == "list":
            permission_classes = [IsFactory]
        elif self.request.method == "POST" and self.action == "create":
            permission_classes = [IsFreight]
        elif self.request.method == "GET" and self.action == "list_bars_driver":
            permission_classes = [IsDriver]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
