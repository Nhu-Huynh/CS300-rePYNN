from django.db import models
from django.conf import settings
from django.contrib.auth.models import User 

from decimal import Decimal
from dish.models import Dish
class Cart(models.Model):
    customer = models.ForeignKey(User,
                                 null=False,
                                 blank=False,
                                 on_delete=models.CASCADE)
    
    def __init__(self, request):
        """
        Initialize the cart.
        """
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(customer = request.user)
            except Cart.DoesNotExist:
                cart = False
            if not cart:
                self.customer = request.user
                self.cart = {}
            else:
                self.cart = cart
        else :
            self.session = request.session
            cart = self.session.get(settings.CART_SESSION_ID)
            if not cart:
            # save an empty cart in the session
                cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart


    def add(self, dish, quantity=1, override_quantity=False):
        """
        Add a dish to the cart or update its quantity.
        """
        dish_id = str(dish.id)
        if dish_id not in self.cart:
            self.cart[dish_id] = {'quantity': 0, 'price': str(dish.price)}
        if override_quantity:
            self.cart[dish_id]['quantity'] = quantity
        else:
            self.cart[dish_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, dish):
        """
        Remove a dish from cart
        """
        dish_id = str(dish.id)
        if dish_id in self.cart:
            del self.cart[dish_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the dishes from the database.
        """
        dish_ids = self.cart.keys()
        # get the dish objects and add them to the cart
        dishes = Dish.objects.filter(id__in=dish_ids)
        cart = self.cart.copy()
        for dish in dishes:
            cart[str(dish.id)]['dish'] = dish
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        Calculate the subtotal price for all current items in the cart
        """
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
        

    