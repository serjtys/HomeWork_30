import stripe
import os
from django.conf import settings

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def create_stripe_product(name, description):
    """Создание продукта в Stripe"""
    product = stripe.Product.create(
        name=name,
        description=description
    )
    return product.id

def create_stripe_price(product_id, amount):
    """Создание цены в Stripe"""
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),  # Конвертируем в копейки
        currency='rub'
    )
    return price.id

def create_stripe_session(price_id, success_url, cancel_url):
    """Создание сессии оплаты в Stripe"""
    session = stripe.checkout.Session.create(
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url, session.id