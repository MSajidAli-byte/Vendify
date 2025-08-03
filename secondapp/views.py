from datetime import datetime
import hmac
import pprint
import random

# payments gateway jazzcash, easypaisa, bank transfer, etc.
import hashlib
import requests
from django.shortcuts import render, redirect

# from email.message import EmailMessage
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from secondapp.models import Contact_Us, Category, add_product, cart, register_table
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from secondapp.forms import JazzCashForm, add_product_form
from django.db.models import Q


# Create your views here.
def index(request):
    if "user_id" in request.COOKIES:
        uid = request.COOKIES["user_id"]
        usr = get_object_or_404(User, id=uid)
        login(request, usr)
        if usr.is_superuser:
            return HttpResponseRedirect(reverse("admin:index"))
        if usr.is_active:
            return HttpResponseRedirect(reverse("cust_dashboard"))

    recent = Contact_Us.objects.all().order_by("-added_on")[:5]
    cat = Category.objects.all()
    # print("Recent: ", recent)
    return render(
        request, "home.html", {"numbers": range(3), "recent": recent, "categories": cat}
    )


def aboutpage(request):
    cat = Category.objects.all()
    return render(request, "about.html", {"categories": cat})


def register(request):
    return render(request, "register.html")


def contactpage(request):
    # print("Data: ", request.POST)
    cat = Category.objects.all()
    all_data = Contact_Us.objects.all()
    if request.method == "POST":
        # print("Data: ", request.POST)
        name = request.POST.get("name")
        con = request.POST.get("contact")
        sub = request.POST.get("subject")
        msg = request.POST.get("message")

        data = Contact_Us(name=name, contact_number=con, subject=sub, message=msg)
        data.save()
        res = "Dear {} Data Submitted Successfully".format(name)
        return render(request, "contact.html", {"status": res, "messages": all_data})
        # return HttpResponse("Dear {} Data Submitted Successfully".format(name))

    return render(request, "contact.html", {"messages": all_data, "categories": cat})


def register(request):
    cat = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        uname = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        con_password = request.POST.get("confirm_password")
        utype = request.POST.get("utype")
        contact = request.POST.get("contact")
        # print("Data: ", name, last_name, uname, email, password, utype)

        if password != con_password:
            res = "Dear {} Password Mismatch".format(name)
            return render(
                request,
                "register.html",
                {"categories": cat, "status": res, "alert": True},
            )

        # usr = User.objects.create_user(username=uname, contact_number=contact)
        usr = User.objects.create_user(uname, email, password)
        usr.first_name = name
        usr.last_name = last_name

        if utype == "sell":
            usr.is_staff = True

        usr.save()
        reg = register_table(user=usr, contact_number=contact)
        reg.save()

        res = "Dear {} Data Submitted Successfully".format(name)
        return render(
            request, "register.html", {"categories": cat, "status": res, "alert": True}
        )
    return render(request, "register.html", {"categories": cat})


def check_user(request):
    # uname = request.GET.get('usern')  # Get the username from the query parameter
    if request.method == "GET":
        uname = request.GET.get("usern")  # Get the username from the POST request
        print(f"Received username: {uname}")  # Debugging statement
    print(request.POST)  # This will show all key-value pairs in the POST request
    print(request.GET)  # This will show all key-value pairs in the POST request
    if uname:  # Ensure the username is not empty
        check = User.objects.filter(
            username=uname
        )  # Check if the username exists in the database
        print("Check: ", check)  # Debugging statement
        if check.exists():  # Use `.exists()` to check if the queryset is not empty
            return HttpResponse("Exists")  # Return "Exists" if the username exists
        else:
            return HttpResponse(
                "Available"
            )  # Return "Available" if the username does not exist
    return HttpResponse(
        "Invalid Request"
    )  # Return "Invalid Request" if no username is provided


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        un = request.POST.get("username")
        passw = request.POST.get("password")
        user = authenticate(username=un, password=passw)

        if user:
            login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect(
                    reverse("admin:index")
                )  # Redirect to admin panel
            # if user.is_staff:
            else:
                res = HttpResponseRedirect(
                    reverse("cust_dashboard")
                )  # Redirect to seller dashboard
                # return HttpResponseRedirect(reverse("seller_dashboard"))  # Redirect to seller dashboard
                # if user.is_active:
                #     return HttpResponseRedirect(reverse("cust_dashboard"))  # Redirect to customer dashboard
                if "rememberme" in request.POST:
                    res.set_cookie("user_id", user.id)
                    res.set_cookie("date_login", datetime.now())
                return res
        else:
            return render(request, "home.html", {"status": "Invalid Credentials"})

    return HttpResponse("coming soon")  # Return a valid response


@login_required
def cust_dashboard(request):
    context = {}

    data = register_table.objects.filter(user__id=request.user.id).first()
    if not data:
        return HttpResponse("User does not exist")

    return render(request, "cust_dashboard.html", {"data": data})


@login_required
def seller_dashboard(request):
    data = register_table.objects.get(user__id=request.user.id)

    return render(request, "seller_dashboard.html", {"data": data})


@login_required
def logout_user(request):
    logout(request)
    # res =  HttpResponseRedirect("/")
    res = HttpResponseRedirect(reverse("index"))
    res.delete_cookie("user_id")
    res.delete_cookie("date_login")
    return res
    # return HttpResponseRedirect(reverse("index"))  # Redirect to the home page


def edit_profile(request):
    context = {}
    data = register_table.objects.get(user__id=request.user.id)
    context["data"] = data

    if request.method == "POST":
        fn = request.POST.get("fname")
        ln = request.POST.get("lname")
        em = request.POST.get("email")
        con = request.POST.get("contact")
        age = request.POST.get("age")
        city = request.POST.get("city")
        abt = request.POST.get("about")
        occ = request.POST.get("occupation")
        gen = request.POST.get("gender")

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        data.contact_number = con
        data.age = age
        data.city = city
        data.about = abt
        data.occupation = occ
        data.gender = gen
        data.save()

        if "image" in request.FILES:
            pic = request.FILES["image"]
            data.profile_pic = pic
            data.save()

        context["status"] = "Profile Updated Successfully"
        context["alert"] = True

    return render(request, "edit_profile.html", context)


def change_password(request):
    context = {}

    data = register_table.objects.filter(user__id=request.user.id).first()
    if data:
        context["data"] = data
    # context["data"] = data
    if request.method == "POST":
        current_pass = request.POST.get("cpwd")
        new_pass = request.POST.get("npwd")
        user = User.objects.get(id=request.user.id)

        if user.check_password(current_pass):
            user.set_password(new_pass)
            user.save()

            user = authenticate(username=user.username, password=new_pass)
            if user:
                login(request, user)
            context["status"] = "Password Changed Successfully"
            context["alert"] = True
        else:
            context["status"] = "Incorrect Current Password"
            context["alert"] = True

    return render(request, "change_password.html", context)


@login_required
def add_product_view(request):
    context = {}
    check = register_table.objects.filter(user__id=request.user.id).first()
    # data = register_table.objects.get(user__id=request.user.id)
    if check:
        context["data"] = check
    else:
        return HttpResponse("User does not exist")

    forms = add_product_form()
    context["form"] = forms

    if request.method == "POST":
        forms = add_product_form(request.POST, request.FILES)
        if forms.is_valid():
            data = forms.save(commit=False)
            login_user = User.objects.get(id=request.user.id)
            data.user = login_user
            # data.seller = request.login_user
            data.seller = request.user
            data.save()
            context["status"] = "{} Product Added Successfully".format(
                data.product_name
            )

    """ 
    data = register_table.objects.filter(user__id=request.user.id).first()
    if data:
        context["data"] = data
    # context["data"] = data
    
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        product_price = request.POST.get("product_price")
        sale_price = request.POST.get("sale_price")
        product_desc = request.POST.get("product_desc")
        details = request.POST.get("details")
        category = request.POST.get("category")
        
        if "image" in request.FILES:
            pic = request.FILES["image"]
            data.product_image = pic
        
        data.save()
        
        context["status"] = "Product Added Successfully"
        context["alert"] = True """

    return render(request, "add_product.html", context)


def my_products(request):
    context = {}
    data = register_table.objects.filter(user__id=request.user.id).first()
    if data:
        context["data"] = data
    # all = add_product.objects.all()
    all = add_product.objects.filter(seller__id=request.user.id)
    context["products"] = all
    return render(request, "myproducts.html", context)


def single_product(request):
    pid = request.GET.get("pid")  # Get the 'pid' query parameter
    # obj = add_product.objects.get(id=id)  # Retrieve the product by ID

    # Check if the product exists
    # If the product does not exist, it will raise a 404 error
    # if not obj:
    #     return render(request, '404.html', {"message": "Product not found"})

    print(f"Received PID: {pid}")  # Debugging statement
    if not pid:
        return render(
            request, "404.html", {"message": "Product ID not provided"}
        )  # Handle missing 'pid'

    # Retrieve the product or return a 404 error if not found
    product = get_object_or_404(add_product, id=pid)
    return render(request, "single_product.html", {"product": product})


def update_product(request):
    context = {}
    cats = Category.objects.all().order_by("cat_name")
    context["category"] = cats

    pid = request.GET["pid"]
    product = get_object_or_404(add_product, id=pid)
    context["product"] = product

    if request.method == "POST":
        pn = request.POST["pname"]
        ct_id = request.POST["pcat"]
        pr = request.POST["pp"]
        sp = request.POST["sp"]
        des = request.POST["des"]

        cat_obj = Category.objects.get(id=ct_id)

        product.product_name = pn
        product.product_category = cat_obj
        product.product_price = pr
        product.sale_price = sp
        product.details = des
        if "pimg" in request.FILES:
            img = request.FILES["pimg"]
            product.product_image = img
        product.save()
        context["status"] = "Changes Saved Successfully"
        context["id"] = pid
    return render(request, "update_product.html", context)


def all_products(request):
    context = {}
    context["category"] = Category.objects.all()

    data = register_table.objects.filter(user__id=request.user.id).first()
    if data:
        context["data"] = data
    # all = add_product.objects.all()

    all = add_product.objects.all().order_by(
        "product_name"
    )  # Get all products ordered by the product name
    context["products"] = all

    cats = Category.objects.all().order_by(
        "cat_name"
    )  # Get all categories ordered by category name
    context["categories"] = cats

    if "qry" in request.GET:
        q = request.GET["qry"]
        # p = request.GET["price"]

        # p = request.GET["price"]
        prd = add_product.objects.filter(
            Q(product_name__icontains=q) | Q(category__cat_name__contains=q)
        )
        # prd = add_product.objects.filter(Q(product_name__icontains=q)& Q(sale_price__lt=p))
        # prd = add_product.objects.filter(product_name__icontains=q)
        context["products"] = prd
        context["abcd"] = "Some Value"

    if "cat" in request.GET:
        cid = request.GET["cat"]
        prd = add_product.objects.filter(category__id=cid)
        context["products"] = prd
        context["abcd"] = "search"

    return render(request, "allproducts.html", context)


def delete_product(request):
    context = {}
    if "pid" in request.GET:
        pid = request.GET["pid"]
        prd = get_object_or_404(add_product, id=pid)
        context["product"] = prd

        if "action" in request.GET:
            prd.delete()
            context["status"] = str(prd.product_name) + " removed Successfully!!!"
    return render(request, "delete_product.html", context)


def sendemail(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch) > 0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data

    if request.method == "POST":
        # print("Data: ", request.POST)

        if (
            "to" not in request.POST
            or "sub" not in request.POST
            or "msz" not in request.POST
        ):
            context["status"] = "Please fill all fields"
            context["cls"] = "alert-danger"

        rec = request.POST["to"].split(",")
        print(rec)
        sub = request.POST["sub"]
        msz = request.POST["msz"]

        try:
            em = EmailMessage(sub, msz, to=rec)
            em.send()
            context["status"] = "Email Sent"
            context["cls"] = "alert-success"
        except:
            context["status"] = (
                "Could not Send, Please check Internet Connection / Email Address"
            )
            context["cls"] = "alert-danger"

    # em = EmailMessage("Hellow my brother ",to=["g.aliali208@gmail.com"])
    # em.send()
    return render(request, "sendemail.html", context)


def forgotpass(request):
    context = {}
    if request.method == "POST":
        un = request.POST["username"]
        pwd = request.POST["npass"]

        user = get_object_or_404(User, username=un)
        user.set_password(pwd)
        user.save()

        login(request, user)
        if user.is_superuser:
            return HttpResponseRedirect(reverse("admin:index"))
        else:
            return HttpResponseRedirect(reverse("cust_dashboard"))
        # context["status"] = "Password Changed Successfully!!!"

    return render(request, "forgot_pass.html", context)


def reset_password(request):
    context = {}
    un = request.GET["username"]
    try:
        user = get_object_or_404(User, username=un)
        otp = random.randint(1000, 9999)
        msz = "Dear {} \n{} is your One Time Password (OTP) \nDo not share it with others \nThanks&Regards \nMyWebsite".format(
            user.username, otp
        )
        try:
            email = EmailMessage("Account Verification", msz, to=[user.email])
            email.send()
            return JsonResponse({"status": "sent", "email": user.email, "rotp": otp})
            # return JsonResponse({"status":"sent","email":user.email})
        except:
            return JsonResponse({"status": "error", "email": user.email})
    except:
        return JsonResponse({"status": "failed"})

    return render(request, "reset_password.html", context)


def add_to_cart(request):
    context = {}
    items = cart.objects.filter(user__id=request.user.id, status=False)
    context["items"] = items

    if request.user.is_authenticated:
        if request.method == "POST":
            pid = request.POST["pid"]
            qty = request.POST["qty"]
            is_exist = cart.objects.filter(
                product__id=pid, user__id=request.user.id, status=False
            )
            if len(is_exist) > 0:
                context["msz"] = "Item Already Exists in Your Cart"
                context["cls"] = "alert alert-warning"
            else:
                product = get_object_or_404(add_product, id=pid)
                usr = get_object_or_404(User, id=request.user.id)
                c = cart(user=usr, product=product, quantity=qty)
                c.save()
                context["msz"] = "{} Added in Your Cart".format(product.product_name)
                context["cls"] = "alert alert-success"
    else:
        context["status"] = "Please Login First to View Your Cart"
    return render(request, "cart.html", context)

def get_cart_data(request):
    items = cart.objects.filter(user__id=request.user.id, status=False)
    sale,total,quantity =0,0,0
    for i in items:
        sale += float(i.product.sale_price)*i.quantity
        total += float(i.product.product_price)*i.quantity
        quantity+= int(i.quantity)

    res = {
        "total":total,"offer":sale,"quan":quantity,
    }
    return JsonResponse(res)

def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(cart,id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)
    
    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(cart,id=id)
        cart_obj.delete()
        return HttpResponse(1)
    



from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime, timedelta
import hmac, hashlib

from django.views.decorators.csrf import csrf_exempt
from .forms import JazzCashForm
from .models import Order, cart  # Assuming this is your cart model

# # JazzCash configuration constants (use settings if preferred)
# JAZZCASH_MERCHANT_ID = "MC206732"
# JAZZCASH_PASSWORD = "dxhbvu78ev"
# JAZZCASH_RETURN_URL = "http://127.0.0.1:8000/"
# JAZZCASH_INTEGRITY_SALT = "10341399vu"
# JAZZCASH_POST_URL = "https://sandbox.jazzcash.com.pk/CustomerPortal/transactionmanagement/merchantform"

import hashlib

# def generate_secure_hash(post_data: dict, integrity_salt: str):
#     sorted_keys = sorted(post_data)
#     hash_string = "&".join(str(post_data[key]) for key in sorted_keys)
#     hash_string = f"{integrity_salt}&{hash_string}"
#     return hashlib.sha256(hash_string.encode()).hexdigest().upper()

def generate_secure_hash(data_dict, integrity_salt):
    sorted_keys = sorted(data_dict.keys())
    hash_string = ''
    for key in sorted_keys:
        if data_dict[key]:
            hash_string += f'{data_dict[key]}&'
    hash_string += integrity_salt
    return hashlib.sha256(hash_string.encode()).hexdigest().upper()

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
import datetime
from .models import cart

import datetime

# def process_payment(request):
#     items = cart.objects.filter(user_id=request.user, status=False)
#     products = ""
#     amt = 0
#     inv = "INV10001-"
#     cart_ids = ""
#     p_ids = ""

#     for j in items:
#         products += str(j.product.product_name) + "\n"
#         p_ids += str(j.product.id) + ","
#         amt += float(j.product.sale_price)
#         inv += str(j.id)
#         cart_ids += str(j.id) + ","

#     integrity_salt = settings.JAZZCASH_INTEGRITY_SALT
#     txn_ref_no = f"TXN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
#     post_url = "https://sandbox.jazzcash.com.pk/CustomerPortal/transactionmanagement/merchantform/"
#     # txn_datetime = datetime.datetime.now()
#     # expiry_datetime = txn_datetime + timedelta(hours=1)
#     txn_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#     expiry_datetime = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y%m%d%H%M%S")

    
#     data = {
#         "pp_Version": "1.1",
#         "pp_TxnType": "MWALLET",
#         "pp_Language": "EN",
#         "pp_MerchantID": settings.JAZZCASH_MERCHANT_ID,
#         "pp_Password": settings.JAZZCASH_PASSWORD,
#         "pp_TxnRefNo": txn_ref_no,
#         "pp_Amount": str(amt * 100),  # Amount in paisa
#         "pp_TxnCurrency": "PKR",
#         "pp_TxnDateTime": txn_datetime,
#         "pp_BillReference": "INV10001-345",
#         "pp_Description": "Test transaction from Django site",
#         "pp_TxnExpiryDateTime": expiry_datetime,
#         "pp_ReturnURL": request.build_absolute_uri("/jazzcash_return/"),
#         "pp_SecureHash": "",  # Placeholder for now
#         "ppmpf_1": "",
#         "ppmpf_2": "",
#         "ppmpf_3": "",
#         "ppmpf_4": "",
#         "ppmpf_5": "",
#     }

      
#     ordered_keys = [
#     "pp_Amount", "pp_BankID", "pp_BillReference", "pp_Description", "pp_Language",
#     "pp_MerchantID", "pp_Password", "pp_ProductID", "pp_ReturnURL", "pp_SubMerchantID",
#     "pp_TxnCurrency", "pp_TxnDateTime", "pp_TxnExpiryDateTime", "pp_TxnRefNo",
#     "pp_TxnType", "pp_Version"
    
#     ]

    
#     # Generate the secure hash
#     sorted_keys = sorted([k for k in data.keys() if k != 'pp_SecureHash'])
#     hash_string = integrity_salt + '&' + '&'.join(data[k] for k in sorted_keys)
#     secure_hash = hashlib.sha256(hash_string.encode('utf-8')).hexdigest().upper()

#     data['pp_SecureHash'] = secure_hash

#     # JazzCash payment endpoint
#     jazzcash_url = settings.JAZZCASH_POST_URL  # Example: https://sandbox.jazzcash.com.pk/CustomerPortal/transactionmanagement/merchantform/

#     return render(request, 'process_payment.html', {'jazzcash_url': jazzcash_url, 'params': data})

import hashlib
from django.shortcuts import render, redirect
from django.conf import settings
from .models import cart
from datetime import datetime, timedelta

# def process_payment(request):
#     items = cart.objects.filter(user_id=request.user, status=False)
#     products = ""
#     amt = 0
#     txn_ref_no = f"TXN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
#     txn_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#     expiry_datetime = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y%m%d%H%M%S")

#     for j in items:
#         products += str(j.product.product_name) + "\n"
#         amt += float(j.product.sale_price)

#     # Optional: Cap high test amounts
#     amt = min(amt, 50000)  # Max Rs. 50,000 for sandbox

#     data = {
#         "pp_Version": "1.1",
#         "pp_TxnType": "MWALLET",
#         "pp_Language": "EN",
#         "pp_MerchantID": settings.JAZZCASH_MERCHANT_ID,
#         "pp_Password": settings.JAZZCASH_PASSWORD,
#         "pp_TxnRefNo": txn_ref_no,
#         "pp_Amount": str(int(amt * 100)),  # Amount in paisa as integer
#         "pp_TxnCurrency": "PKR",
#         "pp_TxnDateTime": txn_datetime,
#         "pp_BillReference": "INV10001-345",
#         "pp_Description": "Test transaction from Django site",
#         "pp_TxnExpiryDateTime": expiry_datetime,
#         "pp_ReturnURL": request.build_absolute_uri("/jazzcash_return/"),
#         "pp_BankID": "", "pp_ProductID": "", "pp_SubMerchantID": "",
#         "ppmpf_1": "", "ppmpf_2": "", "ppmpf_3": "", "ppmpf_4": "", "ppmpf_5": "",
#     }

#     sorted_keys = sorted([k for k in data.keys() if k != 'pp_SecureHash'])
#     hash_string = settings.JAZZCASH_INTEGRITY_SALT + '&' + '&'.join(data[k] for k in sorted_keys)
#     secure_hash = hashlib.sha256(hash_string.encode('utf-8')).hexdigest().upper()
#     data['pp_SecureHash'] = secure_hash

#     # 🚀 Pass post-ready data to template
#     return render(request, 'process_payment.html', {'post_data': data})


from django.shortcuts import render
from datetime import datetime, timedelta
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt

# Replace these with your JazzCash sandbox credentials
JAZZCASH_MERCHANT_ID = settings.JAZZCASH_MERCHANT_ID
JAZZCASH_PASSWORD = settings.JAZZCASH_PASSWORD
JAZZCASH_RETURN_URL = "http://127.0.0.1:8000/jazzcash_return/"
JAZZCASH_INTEGRITY_SALT = settings.JAZZCASH_INTEGRITY_SALT

@csrf_exempt
def process_payment(request):
    from datetime import datetime, timedelta
    import hmac, hashlib

    items = cart.objects.filter(user_id=request.user, status=False)
    products = ""
    amt = 0
    inv = "INV10001-"
    cart_ids = ""
    p_ids = ""

    for j in items:
        products += str(j.product.product_name) + "\n"
        p_ids += str(j.product.id) + ","
        amt += float(j.product.sale_price)
        inv += str(j.id)
        cart_ids += str(j.id) + ","

    txn_datetime = datetime.now()
    expiry_datetime = txn_datetime + timedelta(hours=1)
    txn_ref_no = f"TXN{txn_datetime.strftime('%Y%m%d%H%M%S')}"

    post_url = "https://sandbox.jazzcash.com.pk/CustomerPortal/transactionmanagement/merchantform/"

    post_data = {
        "pp_Version": "1.1",
        # "pp_TxnType": "MWALLET",  # ✅ or "SALE"
        "pp_TxnType": "",  # ✅ or "SALE"
        "pp_Language": "EN",
        "pp_MerchantID": settings.JAZZCASH_MERCHANT_ID,
        "pp_SubMerchantID": "",
        "pp_Password": settings.JAZZCASH_PASSWORD,
        "pp_BankID": "TBANK",
        "pp_ProductID": "RETL",
        # "pp_TxnType": "MPAY",  # For Mobile Account payment
        "pp_TxnRefNo": txn_ref_no,
        "pp_Amount": str(int(amt * 100)),
        "pp_TxnCurrency": "PKR",
        "pp_TxnDateTime": txn_datetime.strftime("%Y%m%d%H%M%S"),
        "pp_BillReference": "billRef",
        "pp_Description": "Order Payment",
        "pp_TxnExpiryDateTime": expiry_datetime.strftime("%Y%m%d%H%M%S"),
        "pp_ReturnURL": settings.JAZZCASH_RETURN_URL,
        "pp_SecureHash": "",  # to be filled below
        "ppmpf_1": "info1",
        "ppmpf_2": "info2",
        "ppmpf_3": "info3",
        "ppmpf_4": "info4",
        "ppmpf_5": "info5"
    }

    # List of all keys to be used in secure hash
    ordered_keys = [
        "pp_Amount", "pp_BankID", "pp_BillReference", "pp_Description", "pp_Language",
        "pp_MerchantID", "pp_Password", "pp_ProductID", "pp_ReturnURL", "pp_SubMerchantID",
        "pp_TxnCurrency", "pp_TxnDateTime", "pp_TxnExpiryDateTime", "pp_TxnRefNo",
        "pp_TxnType", "pp_Version", "ppmpf_1", "ppmpf_2", "ppmpf_3", "ppmpf_4", "ppmpf_5"
    ]

    # Create secure hash string
    hash_string = '&'.join(f"{key}={post_data[key]}" for key in ordered_keys)
    secure_hash = hmac.new(
        settings.JAZZCASH_INTEGRITY_SALT.encode('utf-8'),
        hash_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest().upper()

    post_data["pp_SecureHash"] = secure_hash
    
    # Create the Order record before redirecting to the payment gateway.
    ord = Order(cust_id=request.user, cart_ids=cart_ids, product_ids=p_ids)
    ord.txn_ref = txn_ref_no  # Add this field to your Order model
    ord.save()
    ord.invoice_id = f"INV-{ord.id}"
    ord.save(update_fields=['invoice_id'])
    
    # ord = Order(cust_id=request.user, cart_ids=cart_ids, product_ids=p_ids)
    # ord.save()
    # ord.invoice_id = f"INV-{ord.id}" # A simpler, more reliable invoice ID
    # ord.save(update_fields=['invoice_id'])
    request.session["order_id"] = ord.id

    return render(request, "process_payment.html", {
        "post_url": post_url,
        "data": post_data
    })


    # return render(request, 'process_payment.html', context)

@csrf_exempt
# def payment_done(request):
#     if "order_id" in request.session:
#         order_id = request.session["order_id"]
#         ord_obj = get_object_or_404(Order,id=order_id)
#         ord_obj.status=True
#         ord_obj.save()

#         for i in ord_obj.cart_ids.split(",")[:-1]:
#             cart_object = cart.objects.get(id=i)
#             cart_object.status=True
#             cart_object.save()
#         del request.session["order_id"]  # Clear the order ID from session
#     else:
#         return HttpResponse("No order found in session.")

#     return render(request,"payment_success.html")
@csrf_exempt
def payment_done(request):
    txn_ref = request.POST.get("pp_TxnRefNo")
    if not txn_ref:
        return HttpResponse("Missing transaction reference.")

    try:
        ord_obj = Order.objects.get(txn_ref=txn_ref, status=False)
    except Order.DoesNotExist:
        return HttpResponse("No matching order found.")

    ord_obj.status = True
    ord_obj.save()

    cart_ids = [cid for cid in ord_obj.cart_ids.split(",") if cid.strip()]
    for cid in cart_ids:
        try:
            cart_object = cart.objects.get(id=cid)
            cart_object.status = True
            cart_object.save()
        except cart.DoesNotExist:
            continue

    return render(request, "payment_success.html")

@csrf_exempt
def payment_cancelled(request):
    return render(request, "payment_failed.html")


@csrf_exempt
def jazzcash_return(request):
    
    if request.method == "POST":
        # Debug print full response from JazzCash
        print("\n🎯 JazzCash Response:")
        pprint.pprint(dict(request.POST))

        response_code = request.POST.get('pp_ResponseCode')
        response_msg = request.POST.get('pp_ResponseMessage')
        secure_hash = request.POST.get('pp_SecureHash')

        # Optional: Verify hash (we can add this later)
        
        response_data = request.GET.dict()
        received_hash = response_data.pop('pp_SecureHash', None)

        ordered_keys = [k for k in sorted(response_data.keys())]  # or follow same order as request
        hash_string = '&'.join([response_data[k] for k in ordered_keys])
        hash_string = settings.JAZZCASH_INTEGRITY_SALT + '&' + hash_string
        generated_hash = hashlib.sha256(hash_string.encode('utf-8')).hexdigest()

        if received_hash == generated_hash and response_data.get('pp_ResponseCode') == '000':
            return HttpResponse("Payment Successful")
        else:
            return HttpResponse("Payment Failed: Sorry! Your transaction was not successful. Please try again later.")

        if response_code == "000":
            return HttpResponse("✅ Payment Successful: " + response_msg)
        else:
            return HttpResponse("❌ Payment Failed: " + response_msg)
    else:
        return HttpResponse("❗ Invalid request method.")

# @csrf_exempt
# def payment_done(request):
#     return render(request, "payment_success.html")

# @csrf_exempt
# def payment_cancelled(request):
#     return render(request, "payment_failed.html")
# @csrf_exempt
# def jazzcash_return(request):
#     # Here you can validate the JazzCash response
#     return render(request, "redirect_to_jazzcash.html")

def order_history(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data

    all_orders = []
    orders = Order.objects.filter(cust_id__id=request.user.id).order_by("-id")
    for order in orders:
        products = []
        for id in order.product_ids.split(",")[:-1]:
            pro = get_object_or_404(add_product, id=id)
            products.append(pro)
        ord = {
            "order_id":order.id,
            "products":products,
            "invoice":order.invoice_id,
            "status":order.status,
            "date":order.processed_on,
        }
        all_orders.append(ord)
    context["order_history"] = all_orders
    return render(request,"order_history.html",context)