# This file is part of Sale/Purchase to Invoice module.  
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import sale
from . import purchase


def register():
    Pool.register(
        sale.Sale,
        purchase.Purchase,
        module='sale_purchase_to_invoice', type_='model')
