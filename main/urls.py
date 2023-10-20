from django.urls import path
from .views import *


urlpatterns = [
    path("", index_view, name="index"),
    path("about/", about_view, name="about"),
    path("blog/", blog_view, name="blog"),
    path("blog-single/<int:pk>/", blog_single_view, name="blog-single"),
    path("cart/", cart_view, name="cart"),
    path("checkout/", checkout_view, name="checkout"),
    path("compare/", compare_view, name="compare"),
    path("contact/", contact_view, name="contact"),
    path("faq/", faq_view, name="faq"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name='logout'),
    path("my-account/", my_account_view, name="my-account"),
    path("order-tracking/", order_tracking_view, name="order-tracking"),
    path("shop/", shop_view, name="shop"),
    path("product-single/<int:pk>/", product_single_view, name="product-single"),
    path("thank/", thank_view, name="thank"),
    path("wishlist/", wishlist_view, name="wishlist"),
    path("category/<int:pk>/", category_view, name="category"),
    path("brand/<int:pk>/", brand_view, name="brand"),
    path("search/", search_view, name="search"),

    path("add-cart/<int:pk>/<str:page>/", add_cart, name="add-cart"),
    path("add-wishlist/<int:pk>/<str:page>/", add_wishlist, name="add-wishlist"),
    path("card-remove/<int:pk>/", card_remove, name="card-remove"),
    path("wishlist-remove/<int:pk>/", wishlist_remove, name="wishlist-remove"),
    path("clear-card/", clear_card, name="clear-card"),
    path("create-order/", create_order, name="create-order"),
]
