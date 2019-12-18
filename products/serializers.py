from decimal import Decimal
from rest_framework import serializers
from .models import Category, Products, Cart, Entry, Delivery,Feedback


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',]


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['name', 'category', 'image', 'description', 'price', 'discount_price']

    # category = CategorySerializer(many=True)
    category = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')


class ShortProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['name']


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['quantity', 'product']

    product = ShortProductsSerializer()


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['products', 'total',] #'code' - for code field
        read_only_fields = ['total']

    products = EntrySerializer(many=True, source='entry_set')
    # code = serializers.SlugRelatedField(source='cart_code', slug_field='code', read_only=True, many=False)

    # def create(self, validated_data):
    #     # entry_set: list with Entry objects
    #     cart = Cart.objects.create()
    #     for entry in validated_data['entry_set']:
    #         quantity = entry['quantity']
    #         name = entry['product']['name']
    #         product = Products.objects.get(name=name)
    #         e = Entry(product=product, cart=cart, quantity=quantity)
    #         e.save()
    #     return cart


class DeliveryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['cart', 'code', 'address']
        read_only_fields = ['code']
        write_only_fields = ['address']

    cart = CartSerializer()

    def create(self, validated_data):
        products = validated_data.pop('cart')
        cart = Cart.objects.create()
        for entry in products['entry_set']:
            quantity = entry['quantity']
            name = entry['product']['name']
            product = Products.objects.get(name=name)
            e = Entry(product=product, cart=cart, quantity=quantity)
            e.save()
        delivery = Delivery.objects.create(cart=cart, address=validated_data['address'])
        return delivery


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['status', 'cart']

    cart = CartSerializer()
    status = serializers.CharField(source='get_status_display')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
