from datetime import date
from otrs_somconnexio.otrs_models.ticket_types.change_tariff_ticket import (
    ChangeTariffTicket, ChangeTariffExceptionalTicket,
)
from otrs_somconnexio.otrs_models.ticket_types.change_tariff_ticket_shared_bonds import (  # noqa
    ChangeTariffTicketSharedBond
)
from odoo import fields, api, models, _
from odoo.exceptions import MissingError, ValidationError

from ...services.contract_contract_service import ContractService
from ...helpers.date import first_day_next_month, date_to_str


class ContractMobileTariffChangeWizard(models.TransientModel):
    _name = 'contract.mobile.tariff.change.wizard'

    contract_id = fields.Many2one('contract.contract')
    partner_id = fields.Many2one(
        'res.partner',
        related='contract_id.partner_id'
    )
    start_date = fields.Date('Start Date')
    note = fields.Char()
    fiber_contract_code_to_link = fields.Char(
        compute='_compute_fiber_contract_code_to_link',
    )
    current_tariff_contract_line = fields.Many2one(
        'contract.line',
        related='contract_id.current_tariff_contract_line',
    )
    current_tariff_product = fields.Many2one(
        'product.product',
        related='current_tariff_contract_line.product_id',
        string="Current Tariff"
    )
    has_mobile_pack_offer_text = fields.Selection(
        [('yes', _('Yes')), ('no', 'No')],
        string='Is mobile pack offer available?',
        compute='_compute_has_mobile_pack_offer_text',
        readonly=True
    )
    new_tariff_product_id = fields.Many2one(
        'product.product',
        string='New tariff',
        required=True
    )
    exceptional_change = fields.Boolean(default=False)
    send_notification = fields.Boolean(
        string='Send notification', default=False
    )
    otrs_checked = fields.Boolean(
        string='I have checked OTRS and no other tariff change is pending',
        default=False,
    )
    available_products = fields.Many2many(
        "product.product",
        compute="_compute_available_products",
    )
    location = fields.Char(
        related='contract_id.phone_number'
    )
    mobile_contracts_to_share_with = fields.Many2many(
        comodel_name='contract.contract',
        inverse_name="id",
        string='With which mobile contracts should it share data with?',
    )
    fiber_contract_to_link = fields.Many2one(
        'contract.contract',
        string='To which fiber contract should be linked?',
    )
    mobile_contracts_wo_sharing_bond = fields.Many2many(
        'contract.contract',
        compute='_compute_mobile_contracts_wo_sharing_bond',
    )
    fiber_contracts_wo_sharing_data_mobiles = fields.Many2many(
        'contract.contract',
        compute='_compute_fiber_contracts_wo_sharing_data_mobiles',
    )
    sharing_data_options = fields.Selection(
        selection=lambda self: self._get_sharing_data_options(),
        string='Sharing bond option',
    )
    shared_bond_id_to_join = fields.Selection(
        selection=lambda self: self._get_shared_bond_id_to_join(),
        string='Shared bond id to join option',
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['contract_id'] = self.env.context['active_id']
        return defaults

    def _get_shared_bond_id_to_join(self):

        # TODO -> this method will be unused until existing_shared_bond is an option
        c_id = self.env.context.get('active_id')
        if not c_id:
            return

        contract_id = self.env["contract.contract"].browse(c_id)

        mobile_contracts_w_sharing_bond = self.env["contract.contract"].search(
            [
                ("id", "!=", contract_id.id),
                ("partner_id", "=", contract_id.partner_id.id),
                ("service_technology_id", "=", self.env.ref(
                    "somconnexio.service_technology_mobile").id,
                 ),
                ("is_terminated", "=", False),
            ]
        ).filtered(lambda c: len(c.sharing_bond_contract_ids) == 2)

        shared_bond_dict = {}
        shared_bond_options = []

        for contract in mobile_contracts_w_sharing_bond:
            # Group contracts by code
            if contract.shared_bond_id in shared_bond_dict:
                shared_bond_dict[contract.shared_bond_id].append(contract)
            else:
                shared_bond_dict[contract.shared_bond_id] = [contract]

        # Gather phone numbers for contracts sharing the same shared_bond_id
        for shared_bond_id, contracts in shared_bond_dict.items():
            shared_bond_options.append(
                (shared_bond_id, ','.join(
                    [contract.phone_number for contract in contracts]))
            )

        return shared_bond_options

    def _get_sharing_data_options(self):
        c_id = self.env.context.get('active_id')
        if not c_id:
            return

        contract_id = self.env["contract.contract"].browse(c_id)

        sharing_data_options = []

        if contract_id.shared_bond_id:
            return sharing_data_options

        mobile_contracts = self.env["contract.contract"].search(
            [
                ("id", "!=", contract_id.id),
                ("partner_id", "=", contract_id.partner_id.id),
                ("service_technology_id", "=", self.env.ref(
                    "somconnexio.service_technology_mobile").id,
                 ),
                ("is_terminated", "=", False),
            ]
        )
        # mobile_contracts_w_sharing_bond = mobile_contracts.filtered(
        #     lambda c: len(c.sharing_bond_contract_ids) == 2
        # )

        fiber_contracts_wo_sharing_data_mobiles = \
            self._get_fiber_contracts_wo_sharing_data_mobiles(
                contract_id.partner_id.ref
            )

        # fiber_contracts_w_sharing_data_mobiles = fiber_contracts.filtered(
        #     lambda c: len(c.children_pack_contract_ids) == 2
        # )

        if (fiber_contracts_wo_sharing_data_mobiles and mobile_contracts):
            sharing_data_options.append(
                ('new_shared_bond', _('Create new shared bond')),
            )
        # TODO -> decomment this code to add a mobile to an existing shared bond
        # if (
        #      fiber_contracts_w_sharing_data_mobiles and
        #      mobile_contracts_w_sharing_bond
        # ):
        #     sharing_data_options.append(
        #         ('existing_shared_bond', _('Add line to existing shared bond')),
        #     )

        return sharing_data_options

    @api.depends("partner_id")
    def _compute_fiber_contract_code_to_link(self):
        if self.partner_id:
            service = ContractService(self.env)
            try:
                fiber_contracts = service.get_fiber_contracts_to_pack(
                    partner_ref=self.partner_id.ref)
            except MissingError:
                return
            self.fiber_contract_code_to_link = fiber_contracts[0]['code']

    @api.depends("contract_id")
    def _compute_mobile_contracts_wo_sharing_bond(self):
        if not self.contract_id:
            return
        self.mobile_contracts_wo_sharing_bond = self.env["contract.contract"].search(
            [
                ("id", "!=", self.contract_id.id),
                ("partner_id", "=", self.partner_id.id),
                ("service_technology_id", "=", self.env.ref(
                    "somconnexio.service_technology_mobile").id,
                 ),
                ("is_terminated", "=", False),
            ]
        ).filtered(lambda c: not c.sharing_bond_contract_ids)

    @api.depends("contract_id")
    def _compute_fiber_contracts_wo_sharing_data_mobiles(self):
        """
        Returns all fiber contracts not linked to sharing data mobiles
        They can be linked to a single bonified mobile contract
        """
        if not self.contract_id:
            return

        self.fiber_contracts_wo_sharing_data_mobiles = \
            self._get_fiber_contracts_wo_sharing_data_mobiles(
                self.partner_id.ref
            )

    @api.depends("fiber_contract_code_to_link")
    def _compute_has_mobile_pack_offer_text(self):
        if self.fiber_contract_code_to_link:
            self.has_mobile_pack_offer_text = "yes"
        else:
            self.has_mobile_pack_offer_text = "no"

    @api.depends("has_mobile_pack_offer_text")
    def _compute_available_products(self):
        if not self.has_mobile_pack_offer_text:
            return
        mbl_product_templates = self.env["product.template"].search([
            ('categ_id', '=', self.env.ref('somconnexio.mobile_service').id),
        ])
        product_search_domain = [
            ("product_tmpl_id", "in", mbl_product_templates.ids),
            ("active", "=", True),
            ('has_sharing_data_bond', '=', False),
            ('attribute_value_ids', '!=', self.env.ref('somconnexio.IsInPack').id)
        ]
        if self.has_mobile_pack_offer_text == "yes":
            del product_search_domain[-1]

        self.available_products = self.env['product.product'].search(
            product_search_domain
        )

    @api.onchange('shared_bond_id_to_join')
    def onchange_shared_bond_id_to_join(self):
        if self.shared_bond_id_to_join:
            self.new_tariff_product_id = self.env.ref(
                'somconnexio.50GBCompartides3mobils').id

    @api.onchange('mobile_contracts_to_share_with')
    def onchange_mobile_contracts_to_share_with(self):
        # Assign shared product depending on how many contracts to share with
        # mobile_contracts_to_share_with cannot be empty
        if len(self.mobile_contracts_to_share_with) == 2:
            self.new_tariff_product_id = (
                self.env.ref('somconnexio.50GBCompartides2mobils').id
            )
        elif len(self.mobile_contracts_to_share_with) == 3:
            self.new_tariff_product_id = (
                self.env.ref('somconnexio.50GBCompartides3mobils').id
            )
        elif len(self.mobile_contracts_to_share_with) > 3:
            raise ValidationError(_(
                "Maximum 3 mobile contracts to build a shared data bond"
            ))

    @api.onchange('fiber_contract_to_link')
    def onchange_fiber_contract_to_link(self):
        if not self.fiber_contract_to_link:
            return

        # If chosen fiber is linked with mobile, that mobile contract should share data
        if self.fiber_contract_to_link.children_pack_contract_ids:
            mobile_pack = self.fiber_contract_to_link.children_pack_contract_ids[0]
            self.mobile_contracts_to_share_with = [(4, mobile_pack.id)]

    @api.onchange('sharing_data_options')
    def onchange_sharing_data_options(self):
        if self.sharing_data_options == "new_shared_bond":
            self.mobile_contracts_to_share_with = [(4, self.contract_id.id)]

    def _get_fiber_contracts_wo_sharing_data_mobiles(self, partner_ref):
        """
        Check fiber contracts available to link with mobile contracts sharing data
        """
        service = ContractService(self.env)
        try:
            fiber_contracts_dct = service.get_fiber_contracts_to_pack(
                partner_ref=partner_ref,
                mobiles_sharing_data="true")
        except MissingError:
            return

        return self.env["contract.contract"].search(
            [
                ("id", "in", [c["id"] for c in fiber_contracts_dct])
                ]
            ).filtered(
                lambda c: len(c.sharing_bond_contract_ids) == 1 or
                not c.sharing_bond_contract_ids
            )

    def button_change(self):
        self.ensure_one()

        if not self.otrs_checked:
            raise ValidationError(_(
                "You must check if any previous tariff change is found in OTRS"
            ))

        if self.exceptional_change:
            self.start_date = date.today()
            Ticket = ChangeTariffExceptionalTicket
        else:
            self.start_date = first_day_next_month()
            Ticket = ChangeTariffTicket

        fields_dict = {
            "phone_number": self.contract_id.phone_number,
            "new_product_code": self.new_tariff_product_id.default_code,
            "current_product_code": self.current_tariff_product.default_code,
            "subscription_email": self.contract_id.email_ids[0].email,
            "effective_date": date_to_str(self.start_date),
            "language": self.partner_id.lang,
            "fiber_linked": self.fiber_contract_code_to_link,
            "send_notification": self.send_notification,
        }

        if self.fiber_contract_to_link:
            fields_dict["fiber_linked"] = self.fiber_contract_to_link.code

        if self.sharing_data_options == 'new_shared_bond':
            if self.exceptional_change:
                raise ValidationError(_(
                    "A new shared bond creation cannot be an exceptional change"
                ))
            Ticket = ChangeTariffTicketSharedBond
            fields_dict["contracts"] = [
                {
                    "phone_number": contract.phone_number,
                    "current_product_code": contract.current_tariff_product.code,
                    "subscription_email": contract.email_ids[0].email,
                } for contract in self.mobile_contracts_to_share_with
            ]

        elif self.sharing_data_options == 'existing_shared_bond':
            fields_dict["shared_bond_id"] = self.shared_bond_id_to_join

        Ticket(self.partner_id.vat, self.partner_id.ref, fields_dict).create()

        message = _("OTRS change tariff ticket created. Tariff to be changed from '{}' to '{}' with start_date: {}")  # noqa
        self.contract_id.message_post(
            message.format(
                self.current_tariff_contract_line.product_id.showed_name,
                self.new_tariff_product_id.showed_name,
                self.start_date,
            )
        )
        self._create_activity()
        return True

    def _create_activity(self):
        self.env['mail.activity'].create(
            {
                'summary': " ".join(
                    [_('Tariff change'), self.new_tariff_product_id.showed_name]
                ),
                'res_id': self.contract_id.id,
                'res_model_id': self.env.ref('contract.model_contract_contract').id,
                'user_id': self.env.user.id,
                'activity_type_id': self.env.ref('somconnexio.mail_activity_type_tariff_change').id,  # noqa
                'done': True,
                'date_done': date.today(),
                'date_deadline': date.today(),
                'location': self.contract_id.phone_number,
                'note': self.note,
            }
        )
