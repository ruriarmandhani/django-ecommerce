import json
import os
import requests
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F
from django.urls import reverse
from .models import *
from .forms import LoginForm, RegisterForm, ShippingForm
from .context_processors import count_cart_items
# from .firebase import FirebaseStorage

# # Currently not used because the firebase storage is already set in settings.py
# try:
#     # Setting up the firebase storage integration
#     JSON_PATH = './shop/firebase-key.json'
#     BUCKET_NAME = 'django-olshop.appspot.com'
#     FS = FirebaseStorage(JSON_PATH, BUCKET_NAME)
# except:
#     print("Firebase already exist")

GEODB_API_KEY = os.getenv('GEODB_API_KEY')


def index(request):
    items = Item.objects.all()

    unique_product = []
    unique_product_id = []
    for count, item in enumerate(items):
        if len(unique_product) == count + 1:
            break
        if str(item.product) not in unique_product:
            unique_product.append(str(item.product))
            unique_product_id.append(item.id)
    top_collections = Item.objects.filter(
        id__in=unique_product_id).order_by('-sold')[:4]
    context = {
        'top_collections': top_collections
    }

    return render(request, 'index.html', context)


def login_page(request):
    login_form = LoginForm()
    reg_form = RegisterForm()

    # redirect to index user already login
    if request.user.is_authenticated:
        return redirect('index')

    # create new account for user
    if request.method == 'POST' and 'signup' in request.POST:
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            messages.success(
                request, "Account has been successfully created.", extra_tags="signup")

    # user login
    elif request.method == 'POST' and 'login' in request.POST:
        username = request.POST['email_login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(
                request, 'Incorrect email address or password.', extra_tags="login")

    context = {'login_form': login_form, 'reg_form': reg_form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')


def paginate(request, obj, num_item):
    paginator = Paginator(obj, num_item)
    page = request.GET.get('page', 1)
    try:
        obj = paginator.page(page)
    except PageNotAnInteger:
        obj = paginator.page(1)
    except EmptyPage:
        obj = paginator.page(paginator.num_pages)
    return obj


def sort_item(request, obj):
    sort = request.GET.get('sort-by')
    if sort == 'high':
        obj = obj.order_by('-price')
    elif sort == 'low':
        obj = obj.order_by('price')
    else:
        obj = obj.order_by('-sold')
    return obj


def filter_item_by_color(request, obj):
    colors = request.GET.get('color')
    query = None
    for color in colors.split(','):
        if query == None:
            query = Q(product__color__slug=color)
        else:
            query |= Q(product__color__slug=color)
    obj = obj.filter(query)
    return obj


def shop(request, category_slug=''):
    category = ''
    if category_slug != '':
        # check if category has a parent
        parent = Category.objects.filter(
            slug=category_slug).values_list('parent__category_name', 'parent__slug')[0]
        # print(parent)
        category = Category.objects.filter(
            slug=category_slug).values_list('category_name', 'slug')[0]
        # print(category)
        if parent[0] is None:
            collections = Item.objects.filter(
                product__category__parent__slug=category_slug)
        else:
            collections = Item.objects.filter(
                product__category__slug=category_slug)
    else:
        parent = ''
        collections = Item.objects.all()

    # print(collections)

    unique_item = []
    filter_color = []
    for item in collections:
        if str(item.product) not in unique_item:
            unique_item.append(str(item.product))
            color = {'name': str(item.product.color),
                     'slug': str(item.product.color.slug)}
            if color not in filter_color:
                filter_color.append(color)
        else:
            collections = collections.exclude(id=item.id)

    if 'search' in request.GET:
        q = request.GET.get('search')
        collections = collections.filter(
            Q(product__product_name__contains=q) |
            Q(product__category__category_name__contains=q)
        )

    if 'min-price' in request.GET and 'max-price' in request.GET:
        min = request.GET.get('min-price')
        max = request.GET.get('max-price')
        collections = collections.filter(price__gte=min, price__lte=max)

    if 'sort-by' in request.GET:
        collections = sort_item(request, collections)

    if 'color' in request.GET:
        collections = filter_item_by_color(request, collections)

    collections = paginate(request, collections, 12)

    context = {
        'category_name': None,
        'category_slug': None,
        'parent_name': None,
        'parent_slug': None,
        'collections': collections,
        'filter_color': filter_color
    }

    if category:
        context['category_name'] = category[0]
        context['category_slug'] = category[1]

    if parent:
        context['parent_name'] = parent[0]
        context['parent_slug'] = parent[1]

    return render(request, 'shop.html', context)


def product(request, slug, id):
    items = Item.objects.filter(product__slug=slug).order_by('size__id')
    try:
        item = items.get(id=id)
    except Item.DoesNotExist:
        return redirect('shop')

    item_variants = Item.objects.filter(
        product__product_name=item.product.product_name)

    unique_color = []
    for iv in item_variants:
        if str(iv.product.color) not in unique_color:
            unique_color.append(str(iv.product.color))
        else:
            item_variants = item_variants.exclude(id=iv.id)

    context = {
        'items': items,
        'item_display': item,
        'item_variants': item_variants
    }

    return render(request, 'product.html', context)


@login_required
def cart(request):
    user_id = request.user.id
    order_items = OrderItem.objects.filter(
        user__id=user_id, ordered=False).order_by('item__product__product_name', 'item__product__color')

    count_items = sum([item.quantity for item in order_items])
    price_to_pay = sum([item.get_total_price for item in order_items])

    context = {
        'order_items': order_items,
        'price_to_pay': price_to_pay,
        'count_items': count_items
    }
    return render(request, 'cart.html', context)


@login_required
def add_item_to_cart(request, item_id, quantity):
    item = Item.objects.get(id=item_id)
    if OrderItem.objects.filter(user=request.user, item__id=item_id, ordered=False).exists():
        order_item = OrderItem.objects.get(
            user=request.user, item__id=item_id, ordered=False)
        if order_item.quantity + quantity <= order_item.item.stock:
            order_item.quantity = order_item.quantity + quantity
    else:
        order_item = OrderItem.objects.create(
            user=request.user, item=item, quantity=quantity)
    order_item.save()
    slug = order_item.item.product.slug
    return redirect(reverse('product', kwargs={"slug": slug, "id": item_id}))


@login_required
def change_quantity(request, orderitem_id, flag):
    try:
        orderitem = OrderItem.objects.get(id=orderitem_id)
    except OrderItem.DoesNotExist:
        return redirect('cart')

    if flag == 'add':
        orderitem.quantity = orderitem.quantity + 1
    else:
        if orderitem.quantity - 1 < 1 or flag == "rm-item":
            orderitem.delete()
            return redirect('cart')
        else:
            orderitem.quantity = orderitem.quantity - 1
    orderitem.save()
    return redirect('cart')


@login_required
def checkout(request):
    if count_cart_items(request)['total_item_in_cart'] <= 0:
        return redirect('cart')
    user_id = request.user.id
    order_items = OrderItem.objects.filter(
        user__id=user_id, ordered=False).order_by('item__product__product_name', 'item__product__color')

    price_to_pay = sum([item.get_total_price for item in order_items])

    form = ShippingForm()

    context = {
        'form': form,
        'order_items': order_items,
        'price_to_pay': price_to_pay
    }
    return render(request, 'checkout.html', context)


@login_required
def create_order(request, transaction_id):
    if request.method == 'POST':
        order_items = OrderItem.objects.filter(
            user=request.user, ordered=False)

        item_ids = order_items.values_list('item__id', flat=True)
        quantity = order_items.values_list('quantity', flat=True)

        Item.objects.filter(id__in=item_ids).update(
            stock=F('stock')-quantity, sold=F('sold')+quantity)

        order = Order.objects.create(
            user=request.user, transaction_id=transaction_id)
        order.order_item.set(order_items)
        order.save()

        order_items.update(ordered=True)

        recipient = request.POST['recipient']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        country = request.POST['country']

        shipping_address = ShippingAddress.objects.create(
            user=request.user,
            order=order,
            recipient=recipient,
            recipient_email=email,
            recipient_phone=phone,
            address=address,
            city=city,
            state=state,
            zipcode=zip_code,
            country=country
        )
        shipping_address.save()

    return redirect('order_status')


@login_required
def order_status(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    orders = paginate(request, orders, 5)
    context = {'orders': orders}
    return render(request, 'order-status.html', context)


@login_required
def order_details(request, transaction_id):
    shipping_address = ShippingAddress.objects.get(
        order__transaction_id=transaction_id)
    price_to_pay = sum(
        [item.get_total_price for item in shipping_address.order.order_item.all()])
    context = {
        'order_details': shipping_address,
        'price_to_pay': price_to_pay
    }
    return render(request, 'order-details.html', context)


@login_required
def cities(request, q):
    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"

    querystring = {"namePrefix": q, "limit": 10}

    headers = {
        'x-rapidapi-host': "wft-geo-db.p.rapidapi.com",
        'x-rapidapi-key': GEODB_API_KEY
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    json_response = json.loads(response.text)

    return JsonResponse(json_response, safe=False)


@login_required
def account(request):
    return render(request, 'account.html', {})


@login_required
def edit_profile(request):
    context = {}
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        user.first_name = request.POST['first-name']
        user.last_name = request.POST['last-name']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.save()
        return redirect('account')
    return render(request, 'edit-profile.html', context)


@login_required
def change_password(request):
    context = {}
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        if user.check_password(request.POST['old-password']):
            if request.POST['new-password'] == request.POST['new-password-confirmation']:
                user.set_password(request.POST['new-password'])
                user.save()
                logout(request)
                return redirect('login_page')
            else:
                messages.error(
                    request, "Password confimation does not match.")
        else:
            messages.error(request, "Incorrect old password.")

    return render(request, 'change-password.html', context)
