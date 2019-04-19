from django.contrib import admin


# Register your models here.

from .models import Article
from .models import Product
from .models import Staff
from .models import OrderItem
from .models import Ingredient

admin.site.register(Article)

admin.site.register(Product)

admin.site.register(Staff)

admin.site.register(OrderItem)

admin.site.register(Ingredient)
