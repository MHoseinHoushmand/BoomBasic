from .forms import CreateUserForm,CreateAddressForm
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
def logoutUser(request):
    logout(request)
    return redirect('login')

def store(request):
    artworks = Artwork.objects.all()
    if request.user.is_authenticated and request.user.is_staff == False:
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer)
        get_cart_items = orders.count()
    else:
        get_cart_items = 0
    context ={'artworks':artworks, 'get_cart_items':get_cart_items}
    return render(request,'store/store.html',context)

@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated and request.user.is_staff == False:
        customer = Customer.objects.get(user = request.user)
        orders = Order.objects.filter(customer = customer)
        get_cart_items = orders.count()
        get_cart_total = 0
        items = []
        for i in orders:
            get_cart_total = get_cart_total + i.artwork.price
            items.append(i.artwork)
        order = {'get_cart_total': get_cart_total, 'get_cart_items': get_cart_items}
    else:
        items = []
        get_cart_total= 0
        get_cart_items= 0
    context = {'items':items, 'get_cart_total':get_cart_total, 'get_cart_items':get_cart_items }
    return render(request,'store/cart.html',context)

########################################################

#def addShoppingAddress(request):

#    if request.user.is_authenticated and request.user.is_staff == False:
#        if request.method == 'POST':
#                shopping_add = ShoppingAddress.objects.create()
#                shopping_add.customer = Customer.objects.get(user=request.user)
#                shopping_add.city = request.POST.get('city')
#                shopping_add.zipcode = request.POST.get('zipcode')
#                shopping_add.state = request.POST.get('state')
#                shopping_add.address = request.POST.get('address')
#                print("dddddd")
#                shopping_add.save()
#                return redirect('store')

#########################################################

@login_required(login_url='login')
def checkout(request):
    items = []
    get_cart_total = 0
    get_cart_items = 0
    if request.user.is_authenticated and request.user.is_staff == False:
        customer = Customer.objects.get(user = request.user)
        orders = Order.objects.filter(customer=customer)
        get_cart_items = orders.count()
        for i in orders:
            items.append(i.artwork)
            get_cart_total = get_cart_total + i.artwork.price
    else:
        get_cart_total = 0
        get_cart_items = 0
    #########################

    if request.user.is_authenticated and request.user.is_staff == False:
          if request.method == 'POST':
                    shopping_add = ShoppingAddress.objects.create()
                    shopping_add.customer = Customer.objects.get(user=request.user)
                    shopping_add.city = request.POST.get('city')
                    shopping_add.zipcode = request.POST.get('zipcode')
                    shopping_add.state = request.POST.get('state')
                    shopping_add.address = request.POST.get('address')
                    shopping_add.save()
                    return redirect('store')


    context ={'items':items, 'get_cart_total':get_cart_total , 'get_cart_items':get_cart_items}
    return render(request,'store/checkout.html',context)




def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            customer = Customer.objects.create()
            customer.name = form.cleaned_data.get('username')
            customer.email = form.cleaned_data.get('email')
            user = User.objects.get(username = customer.name)
            customer.user = user
            customer.save()
            return redirect('login')
    context = {'form':form}
    return  render(request, 'store/register.html',context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('store')
        else: messages.info(request,'نام کاربری یا رمز عبور شما نادرست است :(')
    context = {}
    return  render(request, 'store/login.html',context)


@login_required(login_url='login')
def addOrder(request,pk):
    print(pk)
    if request.user.is_authenticated and request.user.is_staff == False:
       print(request.method)
       if request.method == 'GET':
           customer = Customer.objects.get(user=request.user)
           artwork = Artwork.objects.get(id=pk)
           if artwork.status == 'موجود':
              artwork.status = 'نا موجود'
              artwork.save()
              new_order = Order.objects.create()
              new_order.artwork = artwork
              new_order.customer = customer
              new_order.save()
    return redirect('cart')



@login_required(login_url='login')
def deleteOrder(request,pk):

    if request.user.is_authenticated and request.user.is_staff == False:
       print(request.method)
       if request.method == 'GET':
           artwork = Artwork.objects.get(id=pk)
           customer = Customer.objects.get(user=request.user)
           order = Order.objects.get(artwork=artwork)
           if artwork.status == 'نا موجود' and customer.user == order.customer.user:
               order.delete()
               artwork.status = 'موجود'
               artwork.save()
    return redirect('cart')



