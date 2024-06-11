from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import success, cancel, create_checkout_session, place_order



urlpatterns =[
    path('',views.Index,name="Home"),
    # path('login/', views.login_page, name="login_name"),
    path('user_login/',views.user_login,name='user_login'),
    path('product_list/',views.product_list,name='product_list'),
    path('product_detail/<str:slug_url>',views.product_detail,name="product_detail"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('contact/',views.contact,name='contact'),
    path('contact_message/', views.contact_message, name="contact_message"),
    path('my_account/',views.my_account,name='my_account'),
    path('wishlist/',views.wishlist,name="wishlist"),   
    path('wishlist_items/<int:product_id>/',views.wishlist_items, name="wishlist_items"),
    path('wishlist_item_delete/<int:product_id>/',views.wishlist_item_delete,name="wishlist_item_delete"),
    path('register/',views.register,name='register'),
    path('registration_page/',views.registration_page, name='registration_page'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('show_cart/',views.show_cart,name="show_cart"),
    path('delete_item/<int:product_id>', views.delete_item, name='delete_item'),
    path('update_cart_item/<int:product_id>',views.update_cart_item, name='update_cart_item'),
    path('logout/',views.user_logout,name='logout'),
    path('place_order/', place_order, name='place_order'),
    path('myorders',views.myorders, name='myorders'),
    path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('my_webhook_view/',views.my_webhook_view, name="my_webhook_view"),
    path('stripe/webhook/', views.my_webhook_view, name='stripe_webhook'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)        