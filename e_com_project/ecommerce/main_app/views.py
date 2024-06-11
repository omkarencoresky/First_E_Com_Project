import json
import uuid
import stripe
import logging
from decimal import Decimal
from django.views import View
from datetime import timedelta
from django.urls import reverse
from urllib.parse import unquote
from django.conf import settings
from django.utils import timezone
from django.template import loader
from typing import Optional, Union
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required   
from main_app.forms import registerform, loginform, contactform
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, HttpResponseRedirect
from main_app.models import  Product, Addtocart, wishlist_model, Product_details_for_order, Billing_details_for_order, Contactmodel


endpoint_secret = settings.STRIPE_WEBHOOK_KEY
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
logger = logging.getLogger(__name__)
curl = settings.CURRECT_URL
context = {'curl':curl}


def Index(request: HttpRequest) -> HttpResponse:    
    """
    Render the homepage with a list of all products.

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



def user_login(request: HttpRequest) -> HttpResponse:
    """
    Render the login page and handle user login using Django's authentication system.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: Redirects to the user's account page on successful login,
                      or re-renders the login page with an error message on failure.
    """

    if request.method == "POST":
        form = loginform(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(request.user.is_authenticated)
                print(request.user.username)
                if request.user.is_authenticated:
                    messages.success(request, "You are login successfully......!")
                    return redirect('Home')
        else:
            messages.error(request, "Invalid data entered here, try again.......!")
    else:
        form = loginform()
    return render(request, 'login.html', {'form': form})


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

    form = registerform()
    if request.method == 'POST':
        form = registerform(request.POST)
        print('form:-', form)
        if form.is_valid():
            email = request.POST['email']
            username = request.POST['username']
            if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
                messages.success(request, "Username or Email is already used try again with other details...!")
                return render(request, 'registration.html', {'form': form})
            else:
                user = form.save()
                login(request, user)
                messages.success(request, "You have been registered successfully.")
                return redirect("Home")  # Replace 'login_name' with the URL name of your login page
        else:
            messages.error(request,"Invalid details. Please check the form and try again.")
    return render(request, 'registration.html', {'form': form})


def product_list(request: HttpRequest) -> HttpResponse:
    """
    Render the product list page with pagination.

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
def user_logout(request):
    """
    Log out the user and clear the session.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponseRedirect: Redirects to the homepage after logging out.
    """

    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return HttpResponseRedirect(reverse('Home'))


@login_required         
def cart(request: HttpRequest) -> HttpResponse:
    """
    Render the cart page with the current items in the cart.

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
    
    """
    Render the cart page with all items in the cart.

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
    """
    Add a product to the cart.

    Args:
        request (HttpRequest): The request object containing metadata about the request.
        product_id (int): The ID of the product to be added.

    Returns:
        HttpResponse: Redirects to the cart page after adding the product to the cart.
    """

    # if request.method == 'POST':
    if request.user.is_authenticated:
        # try:
            # Fetch the Registration instance associated with the logged-in user
        registration_instance = User.objects.get(username=request.user.username)
        product = Product.objects.filter(id=product_id).first()
        wishlist_item = wishlist_model.objects.filter(product_id=product_id).first()
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
                    new_cart_item.save()

                print('wishlist_item',wishlist_item)
                if wishlist_item:
                    wishlist_item.delete()
                messages.success(request, "Item added into your cart.......!")
                return redirect('show_cart')
            else:
                messages.error(request, f"Product not found with ID: {product_id}")
                return redirect('index')
        except User.DoesNotExist:
            messages.error(request, "User not found.")
        return redirect('login_page')   
    else:
        messages.error(request, "User is not authenticate.....!")
        return redirect('index')


@login_required  
def delete_item(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    """
    Delete an item from the cart.

    Args:
        request (HttpRequest): The request object containing metadata about the request.
        product_id (int): The ID of the product to be deleted from the cart.

    Returns:
        HttpResponse: Redirects to the cart page after deleting the item.
    """

    data = Addtocart.objects.filter(user=request.user.id, product_id = product_id).first()
    if data:
        data.delete()
        messages.success(request, "Item removed from your cart....!")
        return redirect('show_cart')
    else:
        return redirect('show_cart')


@login_required   
def update_cart_item(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    """
    Update the quantity of a cart item.

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
    """
    Render the checkout page with current cart items.

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
    """
    Handle the order placement process.

    This function handles the process of placing an order by decoding the data from the request,
    creating order and billing details, and saving them to the database.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse or HttpResponseRedirect: Redirects to the order page after placing the order.
    """

    data_str = request.GET.get('data')
    try:
        decoded_data = json.loads(data_str)
    except json.JSONDecodeError as e:
        return HttpResponse(f"Error decoding data: {e}", status=400)
    
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
    billing_order = Billing_details_for_order.objects.create(
                                    user=registration_user,
                                    order_id=order_product,
                                    first_name=decoded_data['first_name'],
                                    last_name=decoded_data['last_name'],
                                    email=decoded_data['email'],
                                    mobno=decoded_data['mobno'],
                                    landmark=decoded_data['landmark'],
                                    address=decoded_data['address'],
                                    country=decoded_data['country'],
                                    city=decoded_data['city'],
                                    state=decoded_data['state'],
                                    zip_code=decoded_data['zip_code'],
                                    order_date=decoded_data['order_date']
                                )
    billing_order.save()
    print("fourth")
    messages.success(request,"Your order has been successfully complete...!")
    return redirect('myorders')



@login_required
def myorders(request: HttpRequest) -> HttpResponse:
    """
    Render the user's order page with all their orders.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered order page with the user's order data.
    """

    data = Product_details_for_order.objects.filter(user=request.user.id).values()
    paginator = Paginator(data, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'curl': curl, 'product_list': page_obj}
    template = loader.get_template('order.html')
    render_template = template.render(context,request)
    return HttpResponse(render_template,content_type='text/html')



def contact(request: HttpRequest) -> HttpResponse:
    """
    Render the contact page.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered contact page.
    """
     
    template = loader.get_template('contact.html')
    context = {'curl':curl}
    render_template = template.render(context,request)
    return HttpResponse(render_template,content_type='text/html')


def contact_message(request):
    
    
    if request.method == 'POST':
        form_data = contactform(request.POST)
        if form_data.is_valid():
            form_data.instance.date = timezone.now()
            contact_data = form_data.save(commit=False)
            contact_data.save()
            messages.success(request, "Your response is save our team will work on it.")
            return redirect('contact')
        else:
            messages.error(request, "Your response contains invalid details. Please try again.")
    else:
        form = contactform()
    
    messages.error(request, "Your response has not valid details, try again.")
    return render(request, 'contact_message.html', {'form': form})


@login_required 
def my_account(request: HttpRequest) -> HttpResponse:
    """
    Render the user's account page.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered account page.
    """

    order_details = Product_details_for_order.objects.filter(user=request.user)[:5]
    address_details = Billing_details_for_order.objects.filter(user=request.user)
    user_details = User.objects.filter(id=request.user.id)
    template = loader.get_template('my-account.html')
    context = {'curl':curl, 'order_details':order_details, 'address_details':address_details, 'user_details':user_details}
    render_template = template.render(context,request)
    return HttpResponse(render_template,content_type='text/html')


@login_required 
def wishlist(request: HttpRequest) -> HttpResponse: 
    """
    Render the user's wishlist page.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered wishlist page.
    """

    if request.user.is_authenticated:
        data = wishlist_model.objects.filter(user=request.user)
        template = loader.get_template('wishlist.html')
        context = {'curl':curl,'data':data}
        render_template = template.render(context,request)
        return HttpResponse(render_template,content_type='text/html')
    else:
        messages.success(request, "user is not logged in")
        return render(request, "login.html")



@login_required 
def wishlist_items(request: HttpRequest, product_id:int) -> HttpResponse:
    """
    Handle adding items to the wishlist.

    Args:
        request (HttpRequest): The request object containing metadata about the request.
        product_id (int): The ID of the product to be added to the wishlist.

    Returns:
        HttpResponse: Redirects to the home page after adding the item to the wishlist.
    """

    if request.user.is_authenticated:
        try:
            registration_instance = User.objects.get(username=request.user.username)
            product_instance = Product.objects.filter(id=product_id).first()

            if product_instance:
                existing_item = wishlist_model.objects.filter(product=product_instance, user=registration_instance).first()
                if existing_item:
                    messages.success(request, "Item already into the wish-list.")
                    return redirect('Home')
                else:
                    new_wishlist_item = wishlist_model(user=registration_instance, product=product_instance)
                    new_wishlist_item.save()
                    messages.success(request,"Item added into wishlist successfully..!")
                    return redirect ('Home')
            else:
                messages.error(request, f"Product not found with ID: {product_id}")
                return HttpResponse(render(request, "index.html", {'messages': messages}))
            
        except User.DoesNotExist:
            messages.error(request, "User does not exist. Please register first.")
            return render(request,'registration.html')
    else:
        messages.error(request, "User not authenticated.")
        return redirect('login_page')


@login_required
def wishlist_item_delete(request: HttpRequest, product_id:int) -> HttpResponse:
    """
    Handle deleting an item from the wishlist.

    Args:
        request (HttpRequest): The request object containing metadata about the request.
        product_id (int): The ID of the product to be removed from the wishlist.

    Returns:
        HttpResponse: Redirects to the wishlist page after deleting the item.
    """
    if request.user.is_authenticated:
        item = wishlist_model.objects.filter(product_id=product_id, user=request.user).first()
        print(product_id)
        if item:
            item.delete()
            messages.success(request, "Item removed from wishlist successfully.")
            return redirect('wishlist')
        else:
            messages.error(request, "Item not found in your wishlist......!") 
    else:
        messages.error(request, "User not authenticated.")
        return redirect('login_page')
    return redirect('wishlist')



def create_checkout_session(request: HttpRequest) -> HttpResponse:
    """
    Create a checkout session for Stripe.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the Stripe checkout session URL or an error response.
    """

    if request.method == 'POST':
        YOUR_DOMAIN = "http://127.0.0.1:8000"

        # Fetch cart items for the current user
        cart_items = Addtocart.objects.filter(user=request.user)

        # Calculate subtotal and grand total
        subtotal = sum(item.total_item_price for item in cart_items)
        shipping_cost = Decimal('0')  # Assuming no shipping cost
        grand_total = subtotal + shipping_cost

        # Prepare line items for Stripe checkout
        line_items = []
        item_count = 0
        for item in cart_items:
            item_count += 1            
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
        
        if item_count < 5:
            shipping_cost = Decimal('10')
            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Shipping Cost',
                    },
                    'unit_amount': int(shipping_cost * 100),  # Convert shipping cost to cents
                },
                'quantity': 1,
            })
        elif 5 < item_count < 10 :
            shipping_cost = Decimal('20')
            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Shipping Cost',
                    },
                    'unit_amount': int(shipping_cost * 100),  # Convert shipping cost to cents
                },
                'quantity': 1,
            })
        elif 10 < item_count < 15 :
            shipping_cost = Decimal('30')
            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Shipping Cost',
                    },
                    'unit_amount': int(shipping_cost * 100),  # Convert shipping cost to cents
                },
                'quantity': 1,
            })
        else :
            shipping_cost = Decimal('40')
            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Shipping Cost',
                    },
                    'unit_amount': int(shipping_cost * 100),  # Convert shipping cost to cents
                },
                'quantity': 1,
            })

        # Get customer's name and address from the request
        customer_name = request.POST.get('customer_name', '')
        customer_email = request.user.email  # Assuming you have user's email
        customer_address = request.POST.get('customer_address', '')

        checkout_session = None
        success_url=None
        form_data = request.POST
        request.session['form_data'] = json.dumps(form_data)
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=YOUR_DOMAIN + reverse('success'),
                cancel_url=YOUR_DOMAIN + reverse('cancel'),
                customer_email=customer_email,
                shipping_address_collection={
                    'allowed_countries': ['US', 'CA', 'GB', 'AU', 'NZ'],
                },
                metadata={
                    'customer_name': customer_name,
                    'customer_address': customer_address,
                    'grand_total': str(grand_total),
                }
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



def success(request: HttpRequest) -> HttpResponse:
    """
    Handle the success URL after completing a checkout session.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the place_order view with form data or an error response.
    """
      
    form_data = request.session.get('form_data')
    if form_data:
        try:
            decoded_form_data = json.loads(form_data)
        except json.JSONDecodeError as e:
            return HttpResponse(f"Error decoding form data: {e}", status=400)
        # Construct the URL with query parameters
        place_order_url = reverse('place_order') + f'?data={form_data}'
    
        # Redirect to the place_order view with query parameters
        return redirect(place_order_url, code=303)
    else:
        messages.error(request, "Form data not found in session")
        return redirect('checkout')



def cancel(request: HttpRequest) -> HttpResponse:
    """
    Handle the cancel URL after cancelling a checkout session.

    This function handles the cancel URL after cancelling a checkout session.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the cancel.html template.
    """
    
    return render(request, 'cancel.html')



@csrf_exempt
def my_webhook_view(request: HttpRequest) -> HttpResponse:
    """
    Handle the Stripe webhook events.

    This function handles the Stripe webhook events based on their type.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Returns an HTTP response based on the event handling.
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the webhook event based on its type
    if event['type'] == 'checkout.session.completed':
        handle_checkout_completed(event)
    elif event['type'] == 'payment_intent.requires_action':
        handle_requires_action_event(event)
    else:
        # Handle other webhook event types
        handle_other_event(event)

    return HttpResponse(status=200)



def handle_checkout_completed(event: dict) -> None:
    """
    Handle the checkout completed event.

    This function handles the checkout completed event from the Stripe webhook.

    Args:
        event (dict): The Stripe webhook event data.
    """
    print("Checkout completed:", event)



def handle_requires_action_event(event: dict) -> None:
    """
    Handle the payment intent requires action event.

    This function handles the payment intent requires action event from the Stripe webhook.

    Args:
        event (dict): The Stripe webhook event data.
    """
    print("Payment intent requires action:", event)



def handle_other_event(event: dict) -> None:
    """
    Handle other webhook event types.

    This function handles other webhook event types from the Stripe webhook.

    Args:
        event (dict): The Stripe webhook event data.
    """
    print("Other event:", event)