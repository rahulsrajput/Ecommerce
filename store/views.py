from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from .utils import cookieCart, cartData, guestOrder
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import auth
from django.contrib.auth.models import User
from django.contrib import messages
from unicodedata import name
from .models import *
import datetime
import json


# Create your views here.

def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']

        # Create a new user
        newUser = User.objects.create_user(username, email, password)
        newUser.first_name = fname
        newUser.last_name = lname
        newUser.save()

        # Create a new customer and associate it with the user
        Customer.objects.create(user=newUser , email=email , name = fname + ' ' + lname)

        messages.success(request, 'You have successfully registered!')
        return redirect('store')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(request, username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('store')
        else:
            messages.warning(request, 'Invalid username or password')
            return redirect('store')
    else:
        return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('store')    


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products , 'cartItems': cartItems} 
    return render(request, 'store/store.html' , context)

def cart(request):


    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

        

    context = {'items': items , 'order': order , 'cartItems': cartItems}
    
    return render(request, 'store/cart.html' , context)



def checkout(request):
  
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']



    context = {'items': items , 'order': order , 'cartItems': cartItems}
    return render(request, 'store/checkout.html' , context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)


    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    
    return JsonResponse('Item was added', safe=False)

#
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
#


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    
    return JsonResponse('Payment submitted..', safe=False)