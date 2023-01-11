from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

# Create your views here.

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         customer=request.user,
                                         dish=item['dish'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            return render(request, 'created.html',
                          {'order': order})
        else:
            form = OrderCreateForm()
        # return render(request, 'create.html', {
        #     'cart': cart,
        #     'form': form
        # })
        return redirect('dishes:dish_menu')