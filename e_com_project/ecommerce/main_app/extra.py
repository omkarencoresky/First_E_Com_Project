
from django.template.defaultfilters import slugify
from django.utils import timezone
from datetime import timedelta
from django.db import models
from PIL import Image   


# Create your models here.
# class Registration(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(null=True, blank=True)
#     mobno = models.CharField(max_length=20, null=True, blank=True)
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(auto_now=True)  

#     def __str__(self) -> str:
#         return f'{self.first_name} {self.last_name} ({self.username})'


class Contactmodel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=2000)

    def __str__(self)-> str:
        return f"{self.name}({self.subject})"
    

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100,default="")
    price = models.IntegerField(default=1.99)
    old_price = models.IntegerField(default=2.99)
    description = models.CharField(max_length=500)
    specification = models.TextField(max_length=1000)
    publish_date = models.DateField()
    slug = models.CharField(max_length = 100, null = True, blank = True)
    image = models.ImageField(upload_to='media/')

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        return super().save(*args,**kwargs)
       

    def __str__(self) -> str:
        return f"{self.product_name} ===> {self.category}"
    

class ProductReview(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    review_text = models.TextField(max_length=500)

    def __str__(self) -> str:
        return self.name,self.email
    
    
class Addtocart(models.Model):
    product_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    quantity  = models.IntegerField(default=1)
    product_price = models.IntegerField()
    image = models.ImageField()
    total_itme_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def save(self, *args, **kwargs):
        # Calculate the total_item_price before saving
        print(f"Quantity: {self.quantity}, Price: {self.product_price}")
        self.total_item_price = self.quantity * self.product_price
        print(f"Total Item Price: {self.total_itme_price}")
        super(Addtocart, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return f"{self.product_name}"
    

class User_details_for_order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=100,blank=False)
    mobno = models.IntegerField()
    landmark = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

def get_future_date():
    return timezone.now().date() + timedelta(days=8)

class Product_details_for_order(models.Model):
    product_name = models.CharField(max_length=100)
    quantity  = models.IntegerField(default=1)
    product_price = models.IntegerField()
    total_itme_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    order_date = models.DateField(default=timezone.now)
    order_arrival_date = models.DateField(default=get_future_date)
    image = models.ImageField()

    def __str__(self) -> str:
        return f"{self.product_name} - Qty: {self.quantity} - Total: {self.total_itme_price}"
    
    
                # email = form.cleaned_data['email']
                # username = form.cleaned_data['username']
                # user = Billing_details_for_order.objects.filter(email=email,username=username).exists()
                # print(user)
                # if user:
                #     data = Addtocart.objects.filter(user=request.user)
                #     for item in data:
                #         order_product = Product_details_for_order.objects.create(
                #         product_name=item.product.product_name,
                #         quantity=item.quantity,
                #         product_price=item.product.price,
                #         image=item.product.image,
                #         total_itme_price=item.total_item_price,
                #         order_date=timezone.now(),
                #         order_arrival_date=timezone.now() + timedelta(days=8)
                #     )
                #         order_product.save()
                #     Addtocart.objects.filter(user=request.user).delete()
                #     return redirect('myorders')
                # else:
            # user_details = Billing_details_for_order.objects.create(
            #                                                         first_name = form.cleaned_data['first_name'], 
            #                                                         last_name = form.cleaned_data['last_name'], 
            #                                                         email = form.cleaned_data['email'], 
            #                                                         mobno = form.cleaned_data['mobno'], 
            #                                                         landmark = form.cleaned_data['landmark'], 
            #                                                         address = form.cleaned_data['address'], 
            #                                                         country = form.cleaned_data['country'], 
            #                                                         city = form.cleaned_data['city'], 
            #                                                         state = form.cleaned_data['state'], 
            #                                                         zip_code = form.cleaned_data['zip_code'],
            #                                                         order_date = timezone.now(), 
            #                                                         )



if request.user.is_authenticated:
        return redirect('/my_account/')
    msg= ""
    next_url = request.GET.get('next', '')
    print('next_url:-',next_url)
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            hashed_password = hash_password(password)
            print(hashed_password)
            print(f"Username: {username}, Password: {password}")
            user = authenticate(request, username=username, password=hashed_password)
            print('hereuser',user)
            if user is not None:
                login(request, user)
                print(username)
                messages.success(request, f"Login successfully......{username}")
                return redirect('/my_account/')
            else:
                msg= "Invalid email or password. Please try again."
    else:
        form = loginform()  
    return render(request, 'login.html', {'form': form,'msg':msg})




###################################################################################################################



import uuid
import stripe
import logging
from django.views import View
from datetime import timedelta
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.template import loader
from typing import Optional, Union
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from main_app.forms import registerform, loginform, Billing_details_for_order_form
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, HttpResponseRedirect
from main_app.models import  Product, Addtocart, Product_details_for_order, Billing_details_for_order



# Create your views here.
logger = logging.getLogger(__name__)

curl = settings.CURRECT_URL

context = {'curl':curl}


def Index(request: HttpRequest) -> HttpResponse:    
    """Render the homepage with a list of all products.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered homepage with product data.
    """
    data = Product.objects.all().values()
    template = loader.get_template('index.html')
    context = {'curl':curl,'data':data}
    render_template = template.render(context,request)
    return HttpResponse(render_template, content_type='text/html')



def login_page(request: HttpRequest) -> HttpResponse:
    """
    Render the login page.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered login page.
    """
    template = loader.get_template('login.html')
    context = {'curl':curl}
    render_template = template.render(context,request)
    return HttpResponse(render_template, content_type='text/html')



def user_login(request: HttpRequest) -> HttpResponse:
    """
    Handle user login using Django's authentication system.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: Redirects to the user's account page on successful login, 
                      or re-renders the login page with an error message on failure.
    """
    form = loginform()
    if request.method == "POST":
        form = loginform(request, data=request.POST)
        print(form)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            print('username:',username)
            print('password:',password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                auth.login(request, user)
                print('sucess')
                return redirect('my_account')  
        else:
            msg = "Enter details is not valid"
    else:
        msg = "invalid login request"

    return render(request, 'login.html', {'form':form, 'msg':msg})


def registration_page(request: HttpRequest) -> HttpResponse:
    """
    Render the registration page.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered registration page.
    """
    template = loader.get_template('registration.html')
    context = {'curl':curl}
    render_template = template.render(context,request)
    return HttpResponse(render_template,content_type='text/html')



def register(request: HttpRequest) -> HttpResponse:
    """
    Handle user registration.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: Redirects to the homepage on successful registration,
                      or re-renders the registration page with an error message on failure.
    """
    msg = ""
    form = registerform()
    if request.method == 'POST':
        form = registerform(request.POST)
        print('form:-', form)
        if form.is_valid():
            user = form.save()
            print('user:-', user)
            login(request, user)
            messages.success(request, "You have been registered successfully.")
            return redirect("Home")  # Replace 'login_name' with the URL name of your login page
        else:
            print('form errors:', form.errors)
            msg = "Invalid details. Please check the form and try again."
    return render(request, 'registration.html', {'form': form, 'msg': msg})



def product_list(request: HttpRequest) -> HttpResponse:
    """Render the product list page with pagination.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered product list page with paginated product data.
    """
    data = Product.objects.all().values()
    paginator = Paginator(data, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = loader.get_template('product-list.html')
    context = {'curl': curl, 'product_list': page_obj}
    render_template = template.render(context, request)
    return HttpResponse(render_template, content_type='text/html') 




def product_detail(request: HttpRequest, slug_url: str) -> HttpResponse:
    """
    Render the product detail page for a given product.

    Args:
        request (HttpRequest): The request object containing metadata about the request.
        slug_url (str): The slug URL of the product.

    Returns:
        HttpResponse: The rendered product detail page, or the product list page if the product is not found.
    """
    msg=""
    item_data = Product.objects.filter(slug=slug_url).values()
    if item_data:
        single_item_detail = item_data
        products = Product.objects.all()
        template = loader.get_template('product-detail.html')
        context = {'curl':curl,'item_details':single_item_detail, 'products':products}
        return HttpResponse(template.render(context, request))
    else:
        msg = "Product not found."
        template = loader.get_template('product-list.html')
        context = {'curl':curl,'msg':msg}
        return HttpResponse(template.render(context, request))



@login_required
def user_logout(request: HttpRequest) -> HttpResponseRedirect:
    """
    Log out the user and clear the session.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponseRedirect: Redirects to the homepage after logging out.
    """
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    request.session.flush()
    return HttpResponseRedirect(reverse('Home'))



@login_required         
def cart(request: HttpRequest) -> HttpResponse:
    """ Render the cart page with the current items in the cart.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered cart page with cart items.
    """
    data = Addtocart.objects.filter(user=request.user.id)
    # print(f"User {request.user.username} is authenticated: {request.user.is_authenticated}")
    template = loader.get_template('cart.html')
    context = {'curl':curl,'data':data}
    render_template = template.render(context,request)
    return HttpResponse(render_template,content_type='text/html')



@login_required
def show_cart(request: HttpRequest) -> HttpResponse:
    
    """ Render the cart page with all items in the cart.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered cart page with all cart items.
    """
    all_cart_item = Addtocart.objects.filter(user=request.user.id)
    template = loader.get_template('cart.html')
    context = {'curl':curl, 'data': all_cart_item}
    print(all_cart_item)
    render_template = template.render(context,request)
    return HttpResponse(render_template,content_type='text/html')



@login_required
def add_to_cart(request: HttpRequest, product_id:int) -> HttpResponse:
    """ Add a product to the cart.

    Args:
        request (HttpRequest): The request object containing metadata about the request.
        slug (str): The slug URL of the product.

    Returns:
        HttpResponse: Redirects to the cart page after adding the product to the cart.
    """
    # if request.method == 'POST':
    print(f"User authenticated. Username: {request.user.username}")
    if request.user.is_authenticated:
        # try:
            # Fetch the Registration instance associated with the logged-in user
        registration_instance = User.objects.get(username=request.user.username)
        print(f"Registration found: {registration_instance}")
        product = Product.objects.filter(id=product_id).first()
        quantity = int(request.POST.get('quantity', 1))  # Assuming quantity is submitted via POST
        total_item_price = quantity * product.price
        try:
            if product:
                existing_item = Addtocart.objects.filter(product=product, user=registration_instance).first()
                if existing_item:
                    existing_item.quantity += quantity
                    existing_item.total_item_price += total_item_price
                    existing_item.save()
                    return redirect('show_cart')
                else:
                    new_cart_item = Addtocart(user=registration_instance, 
                                              product=product, 
                                              product_name=product.product_name,
                                              price=product.price,
                                              image=product.image,
                                              quantity=quantity,
                                              total_item_price=product.price*quantity)
                    print(new_cart_item)
                    new_cart_item.save()
                    print("Item added to cart.")
                    return redirect('show_cart')
            else:
                print(f"Product not found with ID: {product_id}")
                return HttpResponse("Product not found")
        except Registration.DoesNotExist:
            print("Registration does not exist.")
            return HttpResponse("Registration not found")
    else:
        print("User not authenticated.")
        return redirect('login_page')



@login_required  
def delete_item(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    """ Delete an item from the cart.

    Args:
        request (HttpRequest): The request object containing metadata about the request.
        product_id (int): The ID of the product to be deleted from the cart.

    Returns:
        HttpResponse: Redirects to the cart page after deleting the item.
    """
    data = Addtocart.objects.filter(user=request.user.id, product_id = product_id).first()
    if data:
        data.delete()
        return redirect('show_cart')
    else:
        return redirect('show_cart')



@login_required   
def update_cart_item(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    """ Update the quantity of a cart item.

    Args:
        request (HttpRequest): The request object containing metadata about the request.
        product_id (int): The ID of the product to be updated.

    Returns:
        HttpResponse: Redirects to the cart page after updating the item.
    """
    cart_item = Addtocart.objects.filter(user=request.user.id,product_id=product_id).first()
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        cart_item.quantity = new_quantity
        cart_item.total_item_price = cart_item.quantity * cart_item.price
        cart_item.save()
        return redirect('show_cart')
    return redirect(reverse('update_cart_item', kwargs={'product_id': product_id}))



@login_required 
def checkout(request: HttpRequest) -> HttpResponse:
    """ Render the checkout page with current cart items.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered checkout page with cart items.
    """
    if request.user.is_authenticated:
        user_id = request.user.id
        user_data = User.objects.get(id=user_id)
        data = Addtocart.objects.filter(user=request.user.id).values()
        template = loader.get_template('checkout.html') 
        context = {'curl':curl,'data':data,'user_data':user_data}
        render_template = template.render(context,request)
        return HttpResponse(render_template,content_type='text/html')



@login_required
def place_order(request: HttpRequest)-> Union[HttpResponse, HttpResponseRedirect]:
    """ Handle the order placement process.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: Redirects to the order page after placing the order.
    """

    if request.method == 'POST':
        form = Billing_details_for_order_form(request.POST)
        if form.is_valid():
            data = Addtocart.objects.filter(user=request.user)
            order_id = uuid.uuid4()
            try:
                registration_user = User.objects.get(username=request.user.username)
            except User.DoesNotExist:
                messages.success(request,"User not registered, please register yourself first.")
                return redirect('registration_page')
            if not data.exists():
                messages.success(request,"No items in the cart to place an order.")
                return redirect('Home')
            for item in data:
                order_product = Product_details_for_order.objects.create(
                    user=registration_user,
                    order_id=order_id,
                    product=item.product,
                    product_name=item.product.product_name,
                    quantity=item.quantity,
                    price=item.product.price,
                    image=item.product.image,
                    total_item_price=item.quantity * item.product.price,
                    order_date=timezone.now(),
                    order_arrival_date=timezone.now() + timedelta(days=8)
                )
                order_product.save()
            Addtocart.objects.filter(user=request.user.id).delete()
            billing_details = form.save(commit=False)
            billing_details.order_id = order_product
            billing_details.save()
            messages.success(request,"Your order has been successfully complete...!")
            return redirect('Home')
        else:
            return HttpResponseBadRequest("Form data is not valid. Please check your input.")
    else:
        form = Billing_details_for_order_form()

    return render(request, 'checkout.html', {'form': form})



@login_required
def myorders(request: HttpRequest) -> HttpResponse:
    """ Render the user's order page with all their orders.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered order page with the user's order data.
    """
    data = Product_details_for_order.objects.filter(user=request.user.id).values()
    template = loader.get_template('order.html')
    context = {'curl':curl,'data':data}
    render_template = template.render(context,request)
    return HttpResponse(render_template,content_type='text/html')



def contact(request: HttpRequest) -> HttpResponse:
    """ Render the contact page.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered contact page.
    """
    template = loader.get_template('contact.html')
    context = {'curl':curl}
    render_template = template.render(context,request)
    return HttpResponse(render_template,content_type='text/html')



@login_required 
def my_account(request: HttpRequest) -> HttpResponse:
    """ Render the user's account page.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered account page.
    """
    if request.user.is_authenticated:
        template = loader.get_template('my-account.html')
        context = {'curl':curl}
        render_template = template.render(context,request)
        return HttpResponse(render_template,content_type='text/html')
    else:
        return HttpResponse("not authenticate")



@login_required 
def wishlist(request: HttpRequest) -> HttpResponse:

    """ Render the user's wishlist page.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered wishlist page.
    """
    template = loader.get_template('wishlist.html')
    context = {'curl':curl}
    render_template = template.render(context,request)
    return HttpResponse(render_template,content_type='text/html')



# This is your test secret API key.


# class CreateCheckoutSessionView(View):
#     def get(self, request, *args, **kwargs):
#         # Handle GET requests here if needed
#         return redirect('Home')

#     def post(self, request, *args, **kwargs):
#         YOUR_DOMAIN = "http://127.0.0.1:8000"

#         cart_items = Product_details_for_order.objects.filter(user=request.user)

#         line_items = []
#         for item in cart_items:
#             line_items.append({
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': item.product_name,  # Assuming 'image' is an ImageField
#                     },
#                     'unit_amount': int(item.total_item_price * 100),  # Convert price to cents
#                 },
#                 'quantity': item.quantity,
#             })
#         checkout_session = None
#         try:
#             checkout_session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=line_items,
#                 mode='payment',
#                 success_url=YOUR_DOMAIN + reverse('success'),
#                 cancel_url=YOUR_DOMAIN + reverse('cancel'),
#             )
#         except Exception as e:
#             logger.error(f"Error creating checkout session: {e}")
#             # Handle the error appropriately, such as redirecting to an error page

#         if checkout_session:
#             return redirect(checkout_session.url, code=303)
#         else:
#             # Handle the case where checkout_session is not created
#             return HttpResponse("Failed to create checkout session")

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    # if request.method == 'POST':
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        print('YOUR_DOMAIN:',YOUR_DOMAIN)

        cart_items = Product_details_for_order.objects.filter(user=request.user)
        print('cart_items',cart_items)
        line_items = []
        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product_name,  # Assuming 'image' is an ImageField
                    },
                    'unit_amount': int(item.total_item_price * 100),  # Convert price to cents
                },
                'quantity': item.quantity,
            })
        print('cart_items',cart_items)
        checkout_session = None
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=YOUR_DOMAIN + reverse('success'),
                cancel_url=YOUR_DOMAIN + reverse('cancel'),
            )
        except Exception as e:
            # Handle the error appropriately, such as redirecting to an error page or logging
            return HttpResponse(f"Error creating checkout session: {e}")

        if checkout_session:
            return redirect(checkout_session.url, code=303)
        else:
            # Handle the case where checkout_session is not created
            return HttpResponse("Failed to create checkout session")
    # else:
    #     # Handle GET requests here if needed
    #     return redirect('Home')

def success(request):   
    return place_order(request)

def cancel(request):
    return render(request, 'cancel.html')


This is your test secret API key.


class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        # Handle GET requests here if needed
        return redirect('Home')

    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000"

        cart_items = Product_details_for_order.objects.filter(user=request.user)

        line_items = []
        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product_name,  # Assuming 'image' is an ImageField
                    },
                    'unit_amount': int(item.total_item_price * 100),  # Convert price to cents
                },
                'quantity': item.quantity,
            })
        checkout_session = None
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=YOUR_DOMAIN + reverse('success'),
                cancel_url=YOUR_DOMAIN + reverse('cancel'),
            )
        except Exception as e:
            logger.error(f"Error creating checkout session: {e}")
            # Handle the error appropriately, such as redirecting to an error page

        if checkout_session:
            return redirect(checkout_session.url, code=303)
        else:
            # Handle the case where checkout_session is not created
            return HttpResponse("Failed to create checkout session")


def create_checkout_session(request):
    if request.method == 'POST':
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        print('YOUR_DOMAIN:', YOUR_DOMAIN)

        # Fetch cart items for the current user
        cart_items = Addtocart.objects.filter(user=request.user)

        # Calculate subtotal and grand total
        subtotal = sum(item.total_item_price for item in cart_items)
        shipping_cost = Decimal('5')  # Assuming no shipping cost
        grand_total = subtotal + shipping_cost

        # Prepare line items for Stripe checkout
        line_items = []
        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': f"{item.product_name}",
                    },
                    'unit_amount': int(item.price * 100),  # Convert price to cents
                },
                'quantity': item.quantity,
            })


        print('cart_items', cart_items)
        checkout_session = None
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=YOUR_DOMAIN + reverse('success'),
                cancel_url=YOUR_DOMAIN + reverse('cancel'),
            )
        except Exception as e:
            # Handle the error appropriately, such as redirecting to an error page or logging
            return HttpResponse(f"Error creating checkout session: {e}")

        if checkout_session:
            return redirect(checkout_session.url, code=303)
        else:
            # Handle the case where checkout_session is not created
            return HttpResponse("Failed to create checkout session")
    else:
        # Handle GET requests here if needed
        return redirect('Home')


def login_page(request: HttpRequest) -> HttpResponse:
    """
    Render the login page.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered login page.
    """
    template = loader.get_template('login.html')
    form = loginform()
    context = {'form':form}
    return HttpResponse(template.render(context, request))


def user_login(request: HttpRequest) -> HttpResponse:
    """   
    Handle user login using Django's authentication system.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: Redirects to the user's account page on successful login, 
                      or re-renders the login page with an error message on failure.
    """
    print('method:-',request.method)
    if request.method == "POST":
        form = loginform(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('my_account')  
        else:
            messages.error(request, "Form data is not valid.")
    else:  
        form = loginform()

    return render(request, 'login.html', {'form':form})