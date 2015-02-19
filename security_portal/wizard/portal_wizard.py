# -*- coding: utf-8 -*-
# ##############################################################################
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
from openerp import SUPERUSER_ID


class Wizard(models.TransientModel):
    _inherit = 'portal.wizard'

    def _default_manager(self):
        manager_ids = self.env['res.groups'].search(
            [('is_portalmanager', '=', True)])
        return manager_ids and manager_ids[0] or False

    manager_id = fields.Many2one(
        comodel_name='res.groups',
        string='Portal Manager',
        domain=[('is_portalmanager', '=', True)],
        default=_default_manager,
        required=True,
        help="The portal that Manager can be added in or removed from."
    )

    @api.multi
    def onchange_portal_id(self, portal_id):
        # for each partner, determine corresponding portal.wizard.user records
        res = super(Wizard, self).onchange_portal_id(portal_id=portal_id, )
        res_partner = self.env['res.partner']
        user_changes = []
        # Comprobamos si hay usuarios en la lista
        for user_id in res['value']['user_ids']:
            if user_id:
                portalmanager = False
                partner = res_partner.browse(user_id[2]['partner_id'])
                if partner.user_ids:
                    for group in partner.user_ids[0].groups_id:
                        if group.is_portalmanager:
                            portalmanager = True
                if portalmanager:
                    user_changes.append((0, 0, {
                        'partner_id': user_id[2]['partner_id'],
                        'email': user_id[2]['email'],
                        'in_portal': user_id[2]['in_portal'],
                        'in_portalmanager': portalmanager,
                    }))
                else:
                    user_changes.append(user_id)
        return {'value': {'user_ids': user_changes}}

    def action_apply(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context)
        portal_user_ids = [user.id for user in wizard.user_ids]
        self.pool.get('portal.wizard.user').action_apply(cr, uid,
                                                         portal_user_ids,
                                                         context)
        # Aqui el codigo no estandar agregado para nosotros
        for wizard_user in wizard.user_ids:
            if wizard_user.in_portalmanager:
                user = self.pool.get('portal.wizard.user')._retrieve_user(
                    SUPERUSER_ID, wizard_user, context)
                user.write({'groups_id': [(4, wizard.manager_id.id)]})
        return {'type': 'ir.actions.act_window_close'}


class WizardManager(models.TransientModel):
    _inherit = 'portal.wizard.user'

    in_portalmanager = fields.Boolean(
        string='Portal Manager',
        default=False
    )
