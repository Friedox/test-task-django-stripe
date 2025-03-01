import stripe
from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from .models import Item, Order


def buy(request, id):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    item = get_object_or_404(Item, id=id)
    currency = item.currency.lower() if hasattr(item, 'currency') else 'usd'

    if currency == 'eur':
        amount = int(item.price * Decimal("1.1") * 100)
        final_currency = 'usd'
        stripe.api_key = settings.STRIPE_SECRET_KEY
    else:
        amount = int(item.price * 100)
        final_currency = currency
        stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=final_currency,
            payment_method_types=['card'],
        )
        return JsonResponse({'client_secret': intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    currency = item.currency.lower() if hasattr(item, 'currency') else 'usd'
    public_key = settings.STRIPE_PUBLIC_KEY
    return render(request, 'item.html', {
        'item': item,
        'stripe_public_key': public_key
    })


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    converted_items = []
    total_usd = Decimal("0.00")
    conversion_rate = Decimal("1.1")

    for item in order.items.all():
        if item.currency.lower() == 'eur':
            price_usd = (item.price * conversion_rate).quantize(Decimal("0.01"))
        else:
            price_usd = item.price
        total_usd += price_usd
        converted_items.append({
            'item': item,
            'price_usd': price_usd,
        })

    public_key = settings.STRIPE_PUBLIC_KEY
    return render(request, 'order_detail.html', {
        'order': order,
        'converted_items': converted_items,
        'total_usd': total_usd,
        'stripe_public_key': public_key,
    })


def create_order_payment_intent(request, order_id):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    order = get_object_or_404(Order, id=order_id)
    total = Decimal("0.00")
    conversion_rate = Decimal("1.1")

    for item in order.items.all():
        if item.currency.lower() == 'eur':
            total += item.price * conversion_rate
        else:
            total += item.price

    final_currency = 'usd'
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),
            currency=final_currency,
            payment_method_types=['card'],
            metadata={'order_id': order.id},
        )
        return JsonResponse({'client_secret': intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def payment_success(request):
    return render(request, 'success.html')
