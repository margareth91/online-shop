from django.conf import settings


class Cart(object):
    def __init__(self, request):
        """Inicjalizacja koszyka na zakupy"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Zapis pustego koszyka na zakupy w sesji
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Dodanie produktu do koszyka lub zmiana jego ilości"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        pass
