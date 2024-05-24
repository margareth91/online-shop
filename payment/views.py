import braintree
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from orders.models import Order

# Utworzenie egzemplarza bramki płatności
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        # Pobranie tokena
        nonce = request.POST.get("payment_method_nonce", None)
        # Utworzenie i przesłanie transakcji
        result = braintree.Transaction.sale(
            {
                "amount": f"{order.get_total_cost():.2f}",
                "payment_method_nonce": nonce,
                "options": {"submit_for_settlement": True},
            }
        )
        if result.is_success:
            # Oznaczenie zamówienia jako opłacone
            order.paid = True
            # Zapisanie unikatowego identyfikatora transakcji
            order.braintree_id = result.transaction.id
            order.save()
            return redirect("payment:done")
        else:
            return redirect("payment:cancelled")
    else:
        # Wygenerowanie tokena
        client_token = braintree.ClientToken.generate()
        return render(
            request,
            "payment/process.html",
            {"order": order, "client_token": client_token},
        )


def payment_done(request):
    return render(request, "payment/done.html")


def payment_cancelled(request):
    return render(request, "payment/cancelled.html")
