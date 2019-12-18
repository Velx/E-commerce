import uuid
from decimal import Decimal
from django.db import models, IntegrityError
from django.utils.crypto import get_random_string
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return str(self.name)


class Products(models.Model):
    name = models.CharField(max_length=150)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    products = models.ManyToManyField(Products, through='Entry')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Entry(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('product', 'cart', 'quantity')


class Delivery(models.Model):
    DELIVERY_STATUS_OPTIONS = [
        ('BP', 'обрабатывается'),  # being processed
        ('BF', 'формируется'),  # being formed
        ('ID', 'доставляется'),  # in delivery
        ('D', 'доставлен')  # delivered
    ]
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='cart_code')
    address = models.CharField(max_length=100)
    status = models.CharField(max_length=2, choices=DELIVERY_STATUS_OPTIONS, default='BP')
    code = models.CharField(max_length=15, blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                self.code = get_random_string(length=15)
                super().save(*args, **kwargs)
            except IntegrityError:
                self.save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'


class Feedback(models.Model):
    email = models.EmailField()
    text = models.TextField()

# # sender - заменить на Ентри и посмотреть, пофиксить метод
# @receiver(models.signals.post_save, sender=Entry)
# def update_total(sender, instance, **kwargs):
#     cost = instance.quantity * instance.product.price
#     instance.cart.total += cost
#     instance.cart.save()


@receiver(models.signals.pre_save, sender=Entry)
def updates(sender, instance, **kwargs):
    try:
        pre_saved_instance = Entry.objects.get(pk=instance.pk)
    except Entry.DoesNotExist:
        pre_saved_instance = None
    if pre_saved_instance and pre_saved_instance.quantity != 0:
        pre_saved_cost = pre_saved_instance.quantity * pre_saved_instance.product.price
        instance.cart.total -= pre_saved_cost
    cost = instance.quantity * instance.product.price
    instance.cart.total += cost
    instance.cart.save()
