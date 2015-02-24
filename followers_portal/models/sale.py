# -*- coding: utf-8 -*-
###############################################################################
#
#    Trey, Kilobytes de Soluciones
#    Copyright (C) 2014-Today Trey, Kilobytes de Soluciones <www.trey.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, api, fields, exceptions, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        result = super(SaleOrder, self).create(vals)
        resuers_obj = self.env['res.users']
        partner_obj = self.env['res.partner']
        followers_ids = []
        if 'partner_id' in vals:
            partner_ids = partner_obj.browse(vals['partner_id'])
            for partner in partner_ids.commercial_partner_id:
                users = resuers_obj.search([('partner_id', '=', partner.id)])
                for user in users:
                    for group in user.groups_id:
                        if group.is_portalmanager:
                            followers_ids.append(user.id)
            if followers_ids:
                self.message_subscribe(self.id, followers_ids)
                # subscribe the partner to the invoice
                print "Final del Create"

        return result
