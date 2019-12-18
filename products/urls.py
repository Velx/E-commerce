from django.urls import path
from rest_framework.routers import DefaultRouter
from .apiviews import CategoryList, ProductList, DeliveryRetrieveView, DeliveryCreateView, FeedbackCreateView
# ,CartCreate


urlpatterns = [
    path('categories/', CategoryList.as_view(), name='categories'),
    path('products/', ProductList.as_view(), name='products'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
    # path('carts/', CartCreate.as_view(), name='carts'),
    path('status/', DeliveryCreateView.as_view(), name='carts'),
    path('status/<str:code>', DeliveryRetrieveView.as_view(), name='status')
]
