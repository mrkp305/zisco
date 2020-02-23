from django.db.models import Manager

from .models import (
    Quotation, Order
)


class OrderManager(Manager):
    use_in_migrations = True

    def create_from_quotation(self, q: Quotation):
        if q.has_expired():
            return False, None
        _order: Order = self.model(
            customer=q.customer,
        )
        _order.save(using=self._db)
        for quote_item in q.items.all():
            _order.items.create(
                product=quote_item.product,
                qty=quote_item.qty,
                price=quote_item._price
            )

        return True, _order

    def cfq(self, q):
        return self.create_from_quotation(q)
