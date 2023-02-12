from django.contrib import admin
from .models import Brand,Category,ProductImage,Product,ProductOption,ProductOptionValues,CardItem,Card
# Register your models here.
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Product)
admin.site.register(ProductOption)
admin.site.register(ProductOptionValues)
admin.site.register(CardItem)
admin.site.register(Card)