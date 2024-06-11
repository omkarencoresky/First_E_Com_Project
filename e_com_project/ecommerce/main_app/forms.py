from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from main_app.models import Contactmodel,Billing_details_for_order,Product_details_for_order

class registerform(UserCreationForm):
    """
    Form for user registration.

    Inherits from UserCreationForm, adds fields for username, email, password1, and password2.

    Attributes:
        username (str): The username of the user.
        email (EmailField): The email of the user.
        password1 (str): The first password.
        password2 (str): The confirmation password.
    """
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class loginform(AuthenticationForm):
    """
    Form for user authentication.

    Inherits from AuthenticationForm, adds fields for username and password.

    Attributes:
        username (str): The username of the user.
        password (str): The password for authentication.
    """

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class contactform(forms.ModelForm):
    """
    Form for contacting.

    Inherits from ModelForm, adds fields for name, email, subject, and message.

    Attributes:
        name (str): The name of the contact.
        email (EmailField): The email of the contact.
        subject (str): The subject of the message.
        message (str): The content of the message.
    """
    class Meta:
        model = Contactmodel
        fields = ['name', 'email', 'subject', 'message']


class Billing_details_for_order_form(forms.ModelForm):
    """
    Form for billing details of an order.

    Inherits from ModelForm, adds fields for first name, last name, email, mobile number,
    landmark, address, country, city, state, ZIP code, and order date.

    Attributes:
        first_name (str): The first name of the customer.
        last_name (str): The last name of the customer.
        email (EmailField): The email of the customer.
        mobno (str): The mobile number of the customer.
        landmark (str): The landmark for the address.
        address (str): The complete address of the customer.
        country (str): The country of the customer.
        city (str): The city of the customer.
        state (str): The state of the customer.
        zip_code (str): The ZIP code of the customer.
        order_date (datetime): The date of the order.
    """
    class Meta:
        model = Billing_details_for_order
        fields = ['first_name', 'last_name', 'email', 'mobno', 'landmark', 'address', 'country', 'city', 'state', 'zip_code', "order_date"]


class Product_details_for_order_form(forms.ModelForm):
    """
    Form for product details of an order.

    Inherits from ModelForm, includes all fields from Product_details_for_order.

    Attributes:
        user (User): The user who placed the order.
        order_id (UUID): The unique ID of the order.
        product (Product): The product in the order.
        product_name (str): The name of the product.
        quantity (int): The quantity of the product.
        price (int): The price of the product.
        image (ImageField): The image of the product.
        total_item_price (Decimal): The total price of the item(s).
        order_date (date): The date of the order.
        order_arrival_date (date): The expected arrival date of the order.
    """
    class Meta:
        modle = Product_details_for_order
        field = '__all__'   