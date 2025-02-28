from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:id>/', views.buy, name='buy'),
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/create_payment_intent/', views.create_order_payment_intent, name='create_order_payment_intent'),
    path('success/', views.payment_success, name='payment_success'),
]