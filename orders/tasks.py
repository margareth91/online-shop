from celery import shared_task
from django.core.mail import send_mail

from .models import Order


@shared_task
def order_created(order_id):
    """Zadanie wysyłające powiadomienie za pomocą wiadomości e-mail po zakończonym powodzeniem utworzeniu obiektu
    zamówienia"""
    order = Order.objects.get(id=order_id)
    subject = f"Zamówienie nr {order.id}"
    message = (
        f"Witaj, {order.first_name}!\n\nZłożyłeś zamówienie w naszym sklepie.\nIdentyfikator zamówienia to "
        f"{order.id}."
    )
    mail_sent = send_mail(subject, message, "admin@online_shop.com", [order.email])
    return mail_sent
