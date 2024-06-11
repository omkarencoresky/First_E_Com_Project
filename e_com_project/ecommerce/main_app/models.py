from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db import models
from PIL import Image
import uuid   


# Create your models here. 

class Product(models.Model):
    """
    Represents a product in the store.

    Attributes:
        product_name (str): The name of the product.
        category (str): The category of the product.
        price (int): The price of the product.
        old_price (int): The old price of the product.
        description (str): The description of the product.
        specification (str): The specification of the product.
        publish_date (date): The publish date of the product.
        slug (str): The slug for the product's URL.
        image (ImageField): The image of the product.
    """

    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100,default="")
    price = models.IntegerField(default=1.99)
    old_price = models.IntegerField(default=2.99)
    description = models.CharField(max_length=500)
    specification = models.TextField(max_length=1000)
    publish_date = models.DateField()
    slug = models.CharField(max_length = 100, null = True, blank = True)
    image = models.ImageField(upload_to='')

    def save(self,*args,**kwargs):
        """
        Overrides the save method to auto-generate slug and resize image.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

        if self.image:
            image_path = self.image.path
            fixed_size = (300, 200)  # Define your desired fixed size (width, height)
            image = Image.open(image_path)
            image.thumbnail(fixed_size)
            image.save(image_path)

    def __str__(self) -> str:
        """
        Returns the string representation of the product.

        Returns:
            str: The string representation.
        """
        return f"{self.product_name} ===> {self.category}"
    

class ProductReview(models.Model):
    """
    Represents a product review by a user.

    Attributes:
        name (str): The name of the reviewer.
        email (str): The email of the reviewer.
        review_text (str): The review text.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    review_text = models.TextField(max_length=500)

    def __str__(self) -> str:
        """
        Returns the string representation of the product review.

        Returns:
            str: The string representation.
        """
        return f"{self.name} ({self.email})"
    

class Addtocart(models.Model):
    """
    Represents an item added to the cart by a user.

    Attributes:
        user (User): The user who added the item.
        product (Product): The product added to the cart.
        product_name (str): The name of the product.
        price (int): The price of the product.
        image (ImageField): The image of the product.
        quantity (int): The quantity of the product.
        total_item_price (int): The total price of the item(s).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)  # Default product ID
    product_name = models.CharField(max_length=100,blank=True)
    price = models.IntegerField(default=1.99)
    image = models.ImageField(upload_to='',blank=True)
    quantity = models.IntegerField(default=1)
    total_item_price = models.IntegerField(default=0)

    def __str__(self) -> str:
        """
        Returns the string representation of the item in the cart.

        Returns:
            str: The string representation.
        """
        return f'{self.user} - {self.product}'
    

def get_future_date() -> timezone.datetime:
    """
    Get a future date.

    Returns:
        datetime: The future date.
    """
    return timezone.now().date() + timedelta(days=8)


class Product_details_for_order(models.Model):
    """
    Represents product details for an order.

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100,blank=True)
    quantity  = models.IntegerField(default=1)
    price = models.IntegerField(default=1.99)
    image = models.ImageField()
    total_item_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    order_date = models.DateField(default=timezone.now)
    order_arrival_date = models.DateField(default=get_future_date)

    def save(self, *args, **kwargs) -> None:
        """
        Calculates the total item price before saving the cart item.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        
        self.total_item_price = self.quantity * self.price
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        """
        Returns a string representation of the cart item.

        Returns:
            str: A formatted string with quantity, total price, and username.
        """

        return f"Qty: {self.quantity} - Total: {self.total_item_price} - Username: {self.user} "


class Billing_details_for_order(models.Model):
    """
    Represents billing details for an order.

    Attributes:
        user (User): The user who placed the order.
        order_id (Product_details_for_order): The order ID associated with the billing.
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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Product_details_for_order, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=False)
    mobno = models.CharField(max_length=20)
    landmark = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    order_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the billing details.

        Returns:
            str: A formatted string with the customer's full name.
        """
        return f"{self.first_name} {self.last_name}"
    
    
class wishlist_model(models.Model):
    """
    Represents an item in the wishlist.

    Attributes:
        user (User): The user who added the product to the wishlist.
        product (Product): The product in the wishlist.
    """
     
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Returns a string representation of the wishlist item.

        Returns:
            str: A formatted string with username and product name.
        """
        return f'(Username - {self.user.username}, Product -  {self.product.product_name})'
    

class Contactmodel(models.Model):
    """
    Represents a contact message.

    Attributes:
        name (str): The name of the sender.
        email (str): The email of the sender.
        subject (str): The subject of the message.
        message (str): The message content.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=2000)
    date = models.DateTimeField()

    # def __str__(self)-> str:
    #     """
    #     Returns a string representation of the contact message.

    #     Returns:
    #         str: A formatted string with sender's name and subject.
    #     """

    #     return f"{self.name}  -  ({self.subject}) - ({self.date})"