from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class Book(models.Model):
    objects = None
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    publication_year = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Обычный пользователь'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    print("CustomUser model loaded")


class CartItem(models.Model): #корзина
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.book.price

class Order(models.Model): #заказ
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_cost(self):
        return sum(item.book.price * item.quantity for item in self.items.all())

class OrderItem(models.Model): #элемент заказа(товар в заказе)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
