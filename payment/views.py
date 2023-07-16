import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from basket.basket import Basket
from orders.views import payment_confirmation


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')


class Error(TemplateView):
    template_name = 'payment/error.html'


@login_required
def BasketView(request):

    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    print('total')
    stripe.api_key = 'sk_test_51NUFzSSAnLLjPSZvNUQEOtJX0nVP8PFDDvs3DkOBYqNYnrnf8HoPkJV656ri9uk4X1bEqCrcolcdLVXr9sBq3AgS002fxMI8XY'
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/home.html', {'client_secret': intent.client_secret})
    # return render(request, 'payment/home.html')


# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     event = None

#     try:
#         event = stripe.Event.construct_from(
#             json.loads(payload), stripe.api_key
#         )
#     except ValueError as e:
#         print(e)
#         return HttpResponse(status=400)
    
#     if event.type == 'payment_intent.succeeded':
#         payment_confirmation(event.data.object.client_secret)

#     else:
#         print('Unhandled event type {}'.format(event.type))

#     return HttpResponse(status=200)
