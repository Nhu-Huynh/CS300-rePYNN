from django.shortcuts import render
from .models import Dish, Category
from django.http import Http404
from cart.forms import CartAddDishForm

def dish_menu(request):
    dishes = Dish.objects.all()
    categories = Category.objects.all()
    cart_dish_form = CartAddDishForm()
    return render(request, 'dish_menu.html', {
        'dishes': dishes,
        'categories': categories,
        'cart_dish_form': cart_dish_form
    })


def dish_detail(request, pid):
    try:
        dish_detail = Dish.objects.get(id=pid)
        cart_dish_form = CartAddDishForm()
    except Dish.DoesNotExist:
        raise Http404("Dish is not found.")
    return render(request, 'dish_detail.html', {'dish': dish_detail, 'cart_dish_form': cart_dish_form})

