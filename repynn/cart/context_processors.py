from .cart import Cart
# from .models import Cart
def cart(request):
    return {'cart': Cart(request)}