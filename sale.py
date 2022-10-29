# This file is part of Sale/Purchase to Invoice module.  
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @classmethod
    def process(cls, sales):
        super(Sale, cls).process(sales)
        pool = Pool()
        Config = pool.get('account.configuration')
        Invoice = pool.get('account.invoice')
        Shipment = pool.get('stock.shipment.out')

        config = Config(1)
        if not config.allow_sale_to_invoice:
            return

        invoices = []
        shipments = []
        for sale in sales:
            if sale.invoice_method != 'order' or \
                    sale.shipment_method != 'order':
                continue
            if sale.state != 'processing':
                continue
            if sale.shipments:
                if len(sale.shipments) > 1:
                    continue
                for ship in sale.shipments:
                    if ship.__class__.__name__ != 'stock.shipment.out':
                        continue
                    if ship.state not in ['waiting']:
                        continue
                    shipments.append(ship)

            for inv in sale.invoices:
                if inv.state == 'draft':
                    inv.invoice_date = sale.sale_date
                    invoices.append(inv)

        Invoice.post(invoices)
        Shipment.assign(shipments)
        Shipment.pick(shipments)
        Shipment.pack(shipments)
        Shipment.done(shipments)
