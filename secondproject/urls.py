"""
URL configuration for secondproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from secondapp import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('about/', views.aboutpage, name="about"),
    path('contact/', views.contactpage, name="contact"),
    path('signup/', views.register, name="reg"),
    path('check_user/', views.check_user, name="check_user"),
    path('login_user', views.login_user, name="login_user"),
    path("customer_dashboard/", views.cust_dashboard, name="cust_dashboard"),  # Add this line
    path("seller_dashboard/", views.seller_dashboard, name="seller_dashboard"),  # Ensure this exists
    path("logout/", views.logout_user, name="logout_user"),  # Ensure this exists
    path("edit_profile/", views.edit_profile, name="edit_profile"),  # Ensure this exists
    path("change_password/", views.change_password, name="change_password"),  # Ensure this exists
    path("add_product/", views.add_product_view, name="add_product_view"),  # Ensure this exists
    path("my_products/", views.my_products, name="my_products"),  # Ensure this exists
    path("sendemail/", views.sendemail, name="sendemail"),  # Ensure this exists
    path("forgotpass/", views.forgotpass, name="forgotpass"),  # Ensure this exists
    path("reset_password/", views.reset_password, name="reset_password"),  # Ensure this exists
    path("cart/", views.add_to_cart, name="cart"),  # Ensure this exists
    path("get_cart_data/", views.get_cart_data, name="get_cart_data"),  # Ensure this exists
    path("change_quan/", views.change_quan, name="change_quan"),  # Ensure this exists

    path('process_payment/',views.process_payment,name="process_payment"),
    # path("success/", views.jazzcash_return, name="jazzcash_return"),
    path('payment_done/',views.payment_done,name="payment_done"),
    path('payment_cancelled/',views.payment_cancelled,name="payment_cancelled"),
    path('jazzcash_return/',views.jazzcash_return,name="jazzcash_return"),
    path('order_history',views.order_history,name="order_history"),
    
    path("delete_product/", views.delete_product, name="delete_product"),  # Ensure this exists
    path("update_product/", views.update_product, name="update_product"),  # Ensure this exists
    path("single_product/", views.single_product, name="single_product"),  # Ensure this exists
    path("all_products/", views.all_products, name="all_products"),  # Ensure this exists
    
    path('paypal/', include('paypal.standard.ipn.urls')),
    
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
