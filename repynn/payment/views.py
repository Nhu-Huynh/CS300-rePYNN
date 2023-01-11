
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404

from order.models import Order

# Create your views here.

# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY  # the Stripe API key
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    # get current order
    customer = request.session.get('customer', None)
    order = get_object_or_404(Order, id=customer)

    if request.method == 'POST':  # --> create a Stripe checkout session
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled')) 
        
        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,  # link Stripe payments to orders
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * int('1')),
                    'currency': 'vnd',
                    'dish_data': {
                        'name': item.dish.name,
                    },
                },
                'quantity': item.quantity,
            })

        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        
        # redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:  # GET request: the order summary and a button to proceed with the payment --> generate a POST request to the view.
        return render(request, 'process.html', locals())

def payment_completed(request):
    return render(request, 'completed.html')

def payment_canceled(request):
    return render(request, 'canceled.html')
    
