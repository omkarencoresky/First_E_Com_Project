from django.contrib import admin
from main_app.models import Product, ProductReview, Addtocart, Billing_details_for_order, Product_details_for_order, wishlist_model, Contactmodel


# Register your models here.

class ContactmodelAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'date')
    

admin.site.register(Product)
admin.site.register(Addtocart)
admin.site.register(Contactmodel,ContactmodelAdmin)
admin.site.register(ProductReview)
admin.site.register(wishlist_model)
admin.site.register(Billing_details_for_order)
admin.site.register(Product_details_for_order)
