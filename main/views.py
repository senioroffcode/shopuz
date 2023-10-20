from django.shortcuts import render, redirect
from .models import *
import datetime
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginator_page(query, num, request):
    paginator = Paginator(query, num)
    pages = request.GET.get('page')
    try:
        list = paginator.page(pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list


def get_card_wishlist(user):
    card = Cart.objects.filter(user=user)
    wishlist = Wishlist.objects.filter(user=user)
    return card.count(), card, wishlist


def get_bonus_product():
    my_date = datetime.timedelta(minutes=0)
    bonus_with_time_count = Product.objects.filter(bonus_duration__gt=my_date).count()
    product_time_one = 0
    product_time_two = 0
    product_time_three = 0
    if bonus_with_time_count >= 3:
        product_time_one = Product.objects.filter(bonus_duration__gt=my_date).order_by('-id')[0]
        product_time_two = Product.objects.filter(bonus_duration__gt=my_date).order_by('-id')[1]
        product_time_three = Product.objects.filter(bonus_duration__gt=my_date).order_by('-id')[2]
    elif bonus_with_time_count == 2:
        product_time_one = Product.objects.filter(bonus_duration__gt=my_date).order_by('-id')[0]
        product_time_two = Product.objects.filter(bonus_duration__gt=my_date).order_by('-id')[1]
    elif bonus_with_time_count == 1:
        product_time_one = Product.objects.filter(bonus_duration__gt=my_date).order_by('-id')[0]
    return product_time_one, product_time_two, product_time_three, bonus_with_time_count


def index_view(request):
    card_count, card, wishlist = 0, [], []
    if not request.user.is_anonymous:
        card_count, card, wishlist = get_card_wishlist(request.user)
    product_time_one, product_time_two, product_time_three, bonus_with_time_count = get_bonus_product()
    context = {
        'card': card,
        'card_count': card_count,
        "wishlist": wishlist,
        'slider': Product.objects.filter(in_slider=True).order_by('-id'),
        'in_ad_product': Product.objects.filter(in_ad=True).order_by('-id')[:4],
        "info": Information.objects.all(),
        'ad': Ad.objects.last(),
        'product_time_one': product_time_one,
        'product_time_two': product_time_two,
        'product_time_three': product_time_three,
        "bonus_with_time_count": bonus_with_time_count,
        'all_feedbacks': Feedback.objects.all().order_by('-id'),
        "last_blogs": Blog.objects.all().order_by('-id')[:2],
        'partners': Partner.objects.all(),
        'product': Product.objects.all().order_by('-id')[:16],
    }
    return render(request, 'index.html', context)


def about_view(request):
    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last(),
        'about': About.objects.last(),
        'team': Team.objects.all(),
        'service': Service.objects.all().order_by('-id')[:3],
        "last_blogs": Blog.objects.all().order_by('-id')[:2],
        'all_feedbacks': Feedback.objects.all().order_by('-id'),
    }
    return render(request, 'about.html', context)


def blog_view(request):
    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last(),
        'blog': Blog.objects.all(),
    }
    return render(request, 'blog-list.html', context)


def blog_single_view(request, pk):
    blog = Blog.objects.get(pk=pk)

    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        'blog': blog,
        "info": Information.objects.last()
    }
    return render(request, 'blog-single.html', context)


def cart_view(request):
    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    total = 0
    for i in card:
        if i.product.bonus_price:
            total += i.product.bonus_price
        else:
            total += i.product.price
    context = {
        'total': total,
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last()
    }
    return render(request, 'cart.html', context)


def checkout_view(request):
    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    total = 0
    for i in card:
        if i.product.bonus_price:
            total += i.product.bonus_price
        else:
            total += i.product.price
    context = {
        'total': total,
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last()
    }
    return render(request, 'checkout.html', context)


def compare_view(request):
    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last()
    }
    return render(request, 'compare.html', context)


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        return redirect("contact")

    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last(),

    }
    return render(request, 'contact.html', context)


def faq_view(request):
    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last(),
        'faq': Faq.objects.all()
    }
    return render(request, 'faq.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if user.count() > 0:
            usr = authenticate(username=username, password=password)
            if usr is not None:
                login(request, usr)
                return redirect('index')
            else:
                messages.warning(request, 'Login yoki parol xato!')
                return redirect('login')
        else:
            messages.warning(request, 'Bunday foydalanuvchi mavjud emas!')
            return redirect('login')

    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last()
    }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if User.objects.filter(username=username).count() > 0:
            messages.warning(request, 'Bunday foydalanuvchi mavjud!')
            return redirect('login')
        if len(password) != 6:
            messages.warning(request, 'Parol minimum 6 harfdan iborat bolishi kerak!')
            return redirect('login')
        usr = User.objects.create_user(username=username, email=email, password=password)
        login(request, usr)
        return redirect('index')


def my_account_view(request):
    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last()
    }
    return render(request, 'my-account.html', context)


def order_tracking_view(request):
    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last()
    }
    return render(request, 'order-tracking.html', context)


def shop_view(request):
    product = Product.objects.all().order_by("-id")
    price = request.GET.get("price")
    if price is not None:
        min_price, max_price = price.split(" - ")[0], price.split(" - ")[1]
        product = product.filter(price__gte=min_price, price__lte=max_price)

    card_count, card, wishlist = 0, [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card_count,
        "wishlist": wishlist,
        "info": Information.objects.last(),
        'brand': Brand.objects.all(),
        'category': Category.objects.all(),
        'product': paginator_page(product, 10, request)
    }
    return render(request, 'shop-left-sidebar.html', context)

# bonusi bolsa bonus search qilish kerak


def product_single_view(request, pk):
    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last(),
        'product': Product.objects.get(id=pk),
        'related': Product.objects.filter(category_id=Product.objects.get(id=pk).category.id)
    }
    return render(request, 'single-product.html', context)


def thank_view(request):
    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last()
    }
    return render(request, 'thank-you-page.html', context)


def wishlist_view(request):
    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "info": Information.objects.last()
    }
    return render(request, 'wishlist.html', context)


def category_view(request, pk):
    product = Product.objects.filter(category_id=pk)
    price = request.GET.get("price")
    if price is not None:
        min_price, max_price = price.split(" - ")[0], price.split(" - ")[1]
        product = product.filter(price__gte=min_price, price__lte=max_price)

    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        "product": product,
        'brand': Brand.objects.all(),
        'category': Category.objects.all(),

    }
    return render(request, 'category.html', context)


def brand_view(request, pk):
    product = Product.objects.filter(brand_id=pk)
    price = request.GET.get("price")
    if price is not None:
        min_price, max_price = price.split(" - ")[0], price.split(" - ")[1]
        product = product.filter(price__gte=min_price, price__lte=max_price)

    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        'product': product,
        'brand': Brand.objects.all(),
        'category': Category.objects.all(),
    }
    return render(request, 'category.html', context)


def search_view(request):
    search = request.GET.get("search")
    product = Product.objects.filter(name__icontains=search)
    price = request.GET.get("price")
    if price is not None:
        min_price, max_price = price.split(" - ")[0], price.split(" - ")[1]
        product = product.filter(price__gte=min_price, price__lte=max_price)

    card, wishlist = [], []
    if not request.user.is_anonymous:
        card, wishlist = get_card_wishlist(request.user)
    context = {
        'card': card,
        'card_count': card.count(),
        "wishlist": wishlist,
        'product': product,
        'brand': Brand.objects.all(),
        'category': Category.objects.all(),
        "info": Information.objects.last()
    }
    return render(request, 'search.html', context)


def add_cart(request, pk, page):
    if request.user.is_authenticated:
        product = Product.objects.get(id=pk)
        user = request.user
        if Cart.objects.filter(product=product, user=user).count() == 0:
            Cart.objects.create(product=product, user=user)
        if page == "shop":
            return redirect("shop")
        elif page == "single":
            return redirect("product-single", product.id)
        elif page == "index":
            return redirect("index")
        else:
            return redirect("index")
    else:
        return redirect("login")


def add_wishlist(request, pk, page):
    if request.user.is_authenticated:
        print(request.user)
        product = Product.objects.get(id=pk)
        user = request.user
        if Wishlist.objects.filter(product=product, user=user).count() == 0:
            Wishlist.objects.create(product=product, user=user)
        if page == "shop":
            return redirect("shop")
        elif page == "single":
            return redirect("product-single", product.id)
        else:
            return redirect("index")
    else:
        return redirect("login")


def card_remove(request, pk):
    Cart.objects.get(id=pk).delete()
    return redirect('index')


def wishlist_remove(request, pk):
    Wishlist.objects.get(id=pk).delete()
    return redirect('index')


def clear_card(request):
    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user).delete()
    return redirect('cart')

import requests
def create_order(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            region = request.POST.get('region')
            city = request.POST.get('city')
            address = request.POST.get('address')
            zip = request.POST.get('zip')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            order = Order.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                region=region,
                city=city,
                address=address,
                zip=zip,
                phone=phone,
                email=email,
            )
            for i in Cart.objects.filter(user=user):
                OrderItem.objects.create(order=order, product=i.product, quantity=1, total_price=i.product.bonus_price if i.product.bonus_price else i.product.price)
            Cart.objects.filter(user=user).delete()
            bot_token = '6605169627:AAEO4Vqbs5lyfF7bhRSyK8BzgL0DI8cwtZM'
            notification_text = 'Yangi buyurtma keldi'
            base_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id=5962822399&text={notification_text}'
            requests.get(base_url)
            return redirect('index')
