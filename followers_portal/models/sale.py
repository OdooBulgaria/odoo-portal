# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.##

from openerp import models, api, fields, exceptions, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        result = super(SaleOrder, self).create(vals)
        resuers_obj = self.env['res.users']
        partner_obj = self.env['res.partner']
        orders_obj = self.env['sale.order']
        followers_ids = []
        if 'partner_id' in vals:
            partner = partner_obj.browse(vals['partner_id'])
            for contact in partner.child_ids:
                user = resuers_obj.search([('partner_id', '=', contact.id)])
                for group in user.groups_id:
                    if group.is_portalmanager:
                        followers_ids.append(contact.id)
            if followers_ids:
                order = orders_obj.browse(result.id)
                for follower in order.message_follower_ids:
                    followers_ids.append(follower.id)
                    order.write({'message_follower_ids': [(6, 0, followers_ids)]})
        return result


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def create(self, vals):
        result = super(AccountInvoice, self).create(vals)
        resuers_obj = self.env['res.users']
        partner_obj = self.env['res.partner']
        invoice_obj = self.env['account.invoice']
        followers_ids = []
        if 'partner_id' in vals:
            partner = partner_obj.browse(vals['partner_id'])
            for contact in partner.child_ids:
                user = resuers_obj.search([('partner_id', '=', contact.id)])
                for group in user.groups_id:
                    if group.is_portalmanager:
                        followers_ids.append(contact.id)
            if followers_ids:
                print followers_ids
                print result.id
                print result
                invoice = invoice_obj.browse(result.id)
                for follower in invoice.message_follower_ids:
                    followers_ids.append(follower.id)
                    invoice.write({'message_follower_ids': [
                        (6, 0, set(followers_ids))]})
        return result
