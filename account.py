# This file is part of Sale/Purchase to Invoice module.  
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import ModelSQL, fields
from trytond.modules.company.model import CompanyValueMixin


class Configuration(metaclass=PoolMeta):
    __name__ = 'account.configuration'

    allow_sale_to_invoice = fields.MultiValue(
        fields.Boolean("Allow Sale to Invoice"))
    allow_sale_to_purchase = fields.MultiValue(
        fields.Boolean("Allow Purchase to Invoice"))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field in ('allow_sale_to_invoice', 'allow_purchase_to_invoice'):
            return pool.get('account.configuration.sale_purchase_to_invoice')
        return super().multivalue_model(field)


class ConfigurationSalePurchaseToInvoice(ModelSQL, CompanyValueMixin):
    "Account Configuration Sale / Purchase to Invoice"
    __name__ = 'account.configuration.sale_purchase_to_invoice'

    allow_sale_to_invoice = fields.Boolean("Allow Sale to Invoice")
    allow_sale_to_purchase = fields.Boolean("Allow Purchase to Invoice")
