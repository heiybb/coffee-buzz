from django.db import models
from django.contrib.auth.models import UserManager
# Create your models here.


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.TextField()
    brief_content = models.TextField()
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)

    # show title in admin instead of object
    def __str__(self):
        return self.title


class Product(models.Model):
    size_choice = (
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Large", "Large"))
    type = (
        ("Coffee", "Coffee"),
        ("Tea", "Tea"),
        ("Cake", "Cake"),
        ("Sandwiches", "Sandwiches")
    )
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=4, decimal_places=2)
    product_state = models.BooleanField(default=True)
    product_size = models.CharField(max_length=255,  choices=size_choice)
    product_type = models.CharField(max_length=255, choices=type, default="Coffee")
    product_quantity = models.IntegerField(default=0)

    # show title in admin instead of object
    def __str__(self):
        state = "Unavailable"
        if self.product_state:
            state = "Available"
        return self.product_name + "  " + self.product_size + "  " + state


class OrderItem(models.Model):
    status = (
        ("Preparing", "Preparing"),
        ("Done", "Done")
    )

    order_item_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, default="N")
    product_price = models.DecimalField(max_digits=4, decimal_places=2)
    order_status = models.CharField(max_length=255, choices=status)
    order_number = models.IntegerField(default=1)
    order_sub_total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)
    user_id = models.IntegerField()
    display_no = models.IntegerField()

    def __str__(self):
        return self.product_name + ",   order status : " + self.order_status


class Staff(models.Model):

    staff_id = models.AutoField(primary_key=True)
    staff_username = models.CharField(max_length=100)
    staff_password = models.CharField(max_length=100)
    staff_email = models.EmailField(max_length=70, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.staff_username


class Ingredient(models.Model):
    ingredients = (
        ("", "Coffee bean"),
        ("", "Full Cream Milk"),
        ("", "White Bread"),
        ("", "Black Tea"),
        ("", "Slim Milk")
    )
    ingredient_id = models.AutoField(primary_key=True)
    input_name = models.CharField(max_length=255, default="Add New Ingredient Here")
    quantity = models.IntegerField(default=10)

    def __str__(self):
        return self.input_name + " " + str(self.quantity)