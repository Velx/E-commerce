from rest_framework import generics, viewsets
from rest_framework.response import Response
from .models import Category, Products, Cart, Delivery, Feedback
from .serializers import CategorySerializer, ProductsSerializer, CartSerializer, DeliverySerializer, \
    DeliveryCreateSerializer,FeedbackSerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductList(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


# class CartCreate(generics.ListCreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer


class DeliveryCreateView(generics.CreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliveryCreateSerializer


class DeliveryRetrieveView(generics.RetrieveAPIView):
    serializer_class = DeliverySerializer
    lookup_field = 'code'

    def get_queryset(self):
        queryset = Delivery.objects.filter(code=self.kwargs.get('code'))
        return queryset


class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
