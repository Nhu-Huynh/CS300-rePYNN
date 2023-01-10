from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from dish.models import Dish
from .models import Cart
from .forms import CartAddDishForm



def cart_detail(request):
    cart = Cart(request)    
    return render(request, 'detail.html', {'cart': cart})

@require_POST
def cart_add(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    form = CartAddDishForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(dish=dish,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id = dish_id)
    cart.remove(dish)
    return redirect('cart:cart_detail')
