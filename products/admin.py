from django.contrib import admin

from .models import Category, Products, Cart, Entry, Delivery, Feedback


class CategoryAdmin(admin.ModelAdmin):
    pass


class ProductsAdmin(admin.ModelAdmin):
    model = Products
    filter_horizontal = ('category',)


class EntryInLine(admin.TabularInline):
    model = Entry
    extra = 2


class CartAdmin(admin.ModelAdmin):
    inlines = (EntryInLine,)


class DeliveryAdmin(admin.ModelAdmin):
    pass


class FeedbackAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Feedback, FeedbackAdmin)
