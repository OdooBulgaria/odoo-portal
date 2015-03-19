# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.##

from openerp import models, api, fields, exceptions, _
from openerp import SUPERUSER_ID


class Wizard(models.TransientModel):
    _inherit = 'portal.wizard'

    @api.model
    def _default_manager(self):
        manager_ids = self.env['res.groups'].search(
            [('is_portalmanager', '=', True)])
        return manager_ids or manager_ids[0] or False

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

    @api.multi
    def action_apply(self):
        res = super(Wizard, self).action_apply()
        # Aqui el codigo no estandar agregado para nosotros
        for wizard_user in self[0].user_ids:
            if wizard_user.in_portalmanager:
                domain = [('partner_id', '=', wizard_user.partner_id.id),
                          ('email', '=', wizard_user.email)]
                res_user_ids = self.env['res.users'].search(domain)
                for res_user_id in res_user_ids:
                    res_user_id.groups_id = [(4, self.manager_id.id)]
        return res


class WizardManager(models.TransientModel):
    _inherit = 'portal.wizard.user'

    in_portalmanager = fields.Boolean(
        string='Portal Manager',
        default=False
    )
