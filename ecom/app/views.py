import os
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import login
from .models import Account,Product,Cart,Category
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode
from django.shortcuts import redirect,get_object_or_404,render
from django.urls import reverse
from django.db import transaction
from django.http import JsonResponse

def loginpage(request):
    return render (request,'loginpage.html')

def page3(request):
    return render (request,'page3.html')


def signuppage(request):
    return render (request,'signuppage.html')


def log(request):
    if request.method=='POST':
        username=request.POST['usname']
        password=request.POST['passd']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_authenticated:
                if user.is_staff:
                    print('ok')
                    login(request,user)
                    request.session['user'] = user.username
                    return redirect('adminmod')
                else:
                    login(request,user)
                    auth.login(request,user)
                    request.session['user'] = user.username
                    return redirect('usermod',id=user.id)
        else:
            messages.info(request,'Invalid Username or Password')
            return redirect('loginpage')
    return render(request,'loginpage.html')


def add_details(request): 
    if(request.method=='POST'):
        fname=request.POST['fname']
        lname=request.POST['lname']
        uname=request.POST['uname']
        pwd=request.POST['password']
        cpwd=request.POST['cp']
        ph=request.POST['phone']
        ad=request.POST['address']
        mail=request.POST['email']
        img=request.FILES.get('image')
        if pwd==cpwd:
            if User.objects.filter(username=uname).exists():
                messages.info(request,'Username already exists')
                return redirect('signuppage')
            else:
                user=User.objects.create_user(first_name=fname,last_name=lname,username=uname,password=pwd,email=mail)
                user.save()
                u=User.objects.get(id=user.id)
                reg=Account(contact=ph,image=img,user=u,address=ad)
                reg.save()
                return redirect('loginpage')
        else:
            messages.info(request,'Incorrect Password')
            return redirect('/')
        
@login_required(login_url='loginpage')
def adminmod(request):
    if request.user.is_staff:
        return render(request,'adminmod.html')
    else:
        query_params = {'error': 'access_denied'}
        url = '{}?{}'.format(reverse('loginpage'), urlencode(query_params))
        return redirect(url)

@login_required(login_url='loginpage')    
def usermod(request,id):
    user=User.objects.get(id=id)
    products=Product.objects.all()
    categories = Category.objects.all()
    if 'user' in request.session:
        return render (request,'usermod.html',{'user':user,'products':products,'categories': categories})
    else:
        query_params = {'error': 'access_denied'}
        url = '{}?{}'.format(reverse('loginpage'), urlencode(query_params))
        return redirect(url)



def home(request):
    products=Product.objects.all()
    return render (request,'home.html',{'products':products})

@login_required(login_url='loginpage')
def lgout(request):
    auth.logout(request)
    return redirect ('loginpage')    

@login_required(login_url='loginpage')
def add_category(request):
    return render (request,'add_category.html')

@login_required(login_url='loginpage')
def addcategory(request):
    if request.method == 'POST':
        cat = request.POST['name']
        Category.objects.create(cat=cat)
        return redirect('add_product')

@login_required(login_url='loginpage')    
def add_product(request):
    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})

@login_required(login_url='loginpage')
def addproduct(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        productname = request.POST.get('productname')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        img = request.FILES.get('img')

        category = Category.objects.get(id=category_id)

        product = Product(
            category=category,
            productname=productname,
            description=description,
            price=price,
            quantity=quantity,
            img=img
        )
        product.save()

    return redirect('list_products')



@login_required(login_url='loginpage')
def list_products(request):
    products = Product.objects.all()
    return render(request, 'list_products.html',{'products': products})


@login_required(login_url='loginpage')
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    categories = Category.objects.all()
    return render(request, 'edit_product.html', {'product': product,'categories': categories})


@login_required(login_url='loginpage')
def editproduct(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        category_id = request.POST.get('category')
        productname = request.POST.get('productname')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        img = request.FILES.get('img') if 'img' in request.FILES else product.img

        category = Category.objects.get(id=category_id)

        product.category = category
        product.productname = productname
        product.description = description
        product.price = price
        product.quantity = quantity
        product.img = img
        product.save()

        return redirect('list_products')  # Redirect to the product list view

@login_required(login_url='loginpage')    
def deleteproduct(request,product_id):
    product=Product.objects.get(id=product_id)
    product.delete()
    return redirect('list_products')


@login_required(login_url='loginpage')
def edit_user(request, id):
    user = User.objects.get(id=id)
    account = Account.objects.get(user=user)
    return render(request, 'edit_user.html', {'user': user,'account': account})

@login_required(login_url='loginpage')
def edituser(request, id):
    user = User.objects.get(id=id)
    account = Account.objects.get(user=user)

    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        phone = request.POST['phone']
        address = request.POST['address']
        email = request.POST['email']
        image = request.FILES.get('image')
           
        user.first_name = fname
        user.last_name = lname
        user.username = uname
        user.email = email
        user.save()

        account.contact = phone
        account.address = address
        if image:
            account.image = image
        account.save()

        messages.success(request, 'User details updated successfully')
        return redirect('usermod',id=user.id )  # Redirect to the user's profile page or any other page
        
@login_required(login_url='loginpage') 
def list_users(request):
    accounts = Account.objects.all()
    return render(request, 'list_users.html', {'accounts': accounts})


@login_required(login_url='loginpage')
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('list_users')

@login_required(login_url='loginpage')
def page2(request):
    categories = Category.objects.all()
    return render(request,'page2.html',{'categories': categories})

@login_required(login_url='loginpage')
def category(request,category_id):
    category = Category.objects.get(id=category_id)  
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category': category,'products': products})

# def category_view(request, category_id):
#     category = Category.objects.get(id=category_id)  
#     products = Product.objects.filter(category=category)
#     return render(request, 'category.html', {'category': category,'products': products})

# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     return redirect('cart')

# def cart_view(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     return render(request, 'cart.html', {'cart_items': cart_items})

# def update_cart_quantity(request):
#     if request.method == 'POST':
#         cart_item_id = request.POST.get('cart_item_id')
#         quantity = request.POST.get('quantity')
#         cart_item = get_object_or_404(Cart, id=cart_item_id)
#         cart_item.quantity = int(quantity)
#         cart_item.save()
#         return JsonResponse({'total_price': cart_item.total_price()})
#     return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='loginpage')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total_price =sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cartitems':cart_items, 'totalprice': total_price})

@login_required(login_url='loginpage')
def increase_quantity(request, id):
    cart_item = Cart.objects.get(product_id=id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    with transaction.atomic():
        cart_item.product.quantity -= 1
        cart_item.product.save()
    return redirect('cart')

@login_required(login_url='loginpage')
def decrease_quantity(request, id):
    cart_item = Cart.objects.get(product_id=id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        with transaction.atomic():
            cart_item.product.quantity += 1
            cart_item.product.save()
    return redirect('cart')

@login_required(login_url='loginpage')
def cart_details(request, id):
    product = Product.objects.get(id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required(login_url='loginpage')
def remove_cart(request, id):
    product = Product.objects.get(id=id)
    cart_item = Cart.objects.filter(user=request.user, product=product).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart')
