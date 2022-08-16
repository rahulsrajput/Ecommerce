from django.urls import path
from . import views

urlpatterns = [
    path('' , views.store , name='store'),
    path('cart/' , views.cart , name='cart'),
    path('checkout/' , views.checkout , name='checkout'),
    path('update_item/' , views.updateItem , name='update_Item'),
    path('process_order/' , views.processOrder , name='process_Order'),
    path('signup/' , views.handleSignup , name='handleSignup'),
    path('login/' , views.handleLogin , name='handleLogin'),
    path('logout/' , views.handleLogout , name='handleLogout'),
]