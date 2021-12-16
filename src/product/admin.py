from django.contrib import admin

# Register your models here.
from .models import Product,ProductVariant,Variant,ProductVariantPrice
admin.site.register(Variant)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)


