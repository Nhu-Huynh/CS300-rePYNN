from django.db import models
from django.contrib.auth.models import User
from dish.models import Dish
# Create your models here.


class Order(models.Model):
    customer = models.ForeignKey(User,
                                 null=False,
                                 blank=False,
                                 on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)
    STATUS = (
        ("0", "pending"),
        ("1", "cooking"),
        ("2", "prepared"),
        ("3", "served"),
    )
    status = models.CharField(max_length=1, choices=STATUS, default='0')
    
    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
