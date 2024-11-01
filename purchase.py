# This file is part of Sale/Purchase to Invoice module.  
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta


class Purchase(metaclass=PoolMeta):
    __name__ = 'purchase.purchase'

    @classmethod
    def process(cls, purchases):
        super(Purchase, cls).process(purchases)
        pool = Pool()
        Config = pool.get('account.configuration')
        Invoice = pool.get('account.invoice')
        Move = pool.get('stock.move')

        config = Config(1)
        if not config.allow_purchase_to_invoice:
            return

        invoices = []
        moves = []
        for purchase in purchases:
            if purchase.invoice_method != 'order':
                continue
            if purchase.state != 'processing':
                continue
            for inv in purchase.invoices:
                if inv.state == 'draft':
                    inv.invoice_date = purchase.purchase_date
                    #inv.save()
                    invoices.append(inv)

            if purchase.shipments:
                continue
            #moves = []
            for line in purchase.lines:
                if not line.moves:
                    continue
                for move in line.moves:
                    if move.state == 'draft':
                        move.effective_date = purchase.purchase_date
                        move.save()
                        moves.append(move)

        Invoice.post(invoices)
        Move.do(moves)
