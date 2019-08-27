#!/usr/bin/python
# -*- coding:utf-8 -*-

from odoo import fields, models, api


class ProductConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'product.config.settings'

    client_id = fields.Char(string=u'客户端ID')
    secret_key = fields.Char(string=u'密钥')

    @api.model
    def get_default_all(self, fields):
        ir_config = self.env['ir.config_parameter']
        client_id = ir_config.get_param('client_id', default='client_id')
        secret_key = ir_config.get_param('secret_key', default='secret_key')

        return dict(
            client_id=client_id,
            secret_key=secret_key,
        )

    @api.multi
    def set_default_all(self):
        self.ensure_one()
        ir_config = self.env['ir.config_parameter']

        ir_config.set_param("client_id", self.client_id or "False")
        ir_config.set_param("secret_key", self.secret_key or "False")

        return True

