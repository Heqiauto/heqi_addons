#!/usr/bin/python
# -*- coding:utf-8 -*- 
from odoo import fields, models, api
import json
import requests


class epc_params(models.Model):
    _name = 'epc.params'
    _description = u'定时更新Epc产品类别及更新品牌关联表'
    _rec_name = 'brand_name'

    code = fields.Char(string=u'code')
    category_id = fields.Many2one('goods.class', string='所属分类ID')
    category_name = fields.Char(string=u'产品分类名称')
    epc_category_id = fields.Char(string=u'产品分类id')
    brand_name = fields.Char(String=u'产品品牌名称')
    epc_brand_id = fields.Integer(String=u'产品品牌id')
    form_code = fields.Char(String=u'唯一编码')

    @api.model
    def timing_get_params(self):
        """
        定时获取产品参数
        :return:
        """
        try:
            data_write = []
            obj_conf = self.env['product.config.settings'].search([], limit=1)
            client_id = obj_conf.client_id
            secret_key = obj_conf.secret_key

            start_url = 'http://api.epc.heqiauto.com/groups/4/category-virtual/1?resource=menu&client_id={}&secret_key={}'.format(client_id, secret_key)
            data_one = requests.get(url=start_url).text
            data_one = json.loads(data_one)
            target_data = data_one['result']

            for i in range(len(target_data)):
                for j in range(len(target_data[i]['category'])):
                    data_cache = {}
                    data_cache['category_name'] = target_data[i]['category'][j]['category_name']
                    data_cache['category_id'] = target_data[i]['category'][j]['category_id']
                    data_cache['parent_name'] = target_data[i]['categoryParent']['category_name']
                    data_write.append(data_cache)

            for i in range(len(data_write)):
                category_name = data_write[i]['category_name']
                category_id = data_write[i]['category_id'] if len(data_write[i]) > 1 else None
                parent_name = data_write[i]['parent_name'] if len(data_write[i]) > 1 else None

                if self.env['goods.class'].search([('name', '=', category_name)]):
                    obj = self.env['goods.class'].search([('name', '=', category_name)])
                    obj.write({
                        'epc_category_id': category_id,
                        'name': category_name,
                        'parent_name': parent_name,
                    })
                else:
                    vars = {
                        'epc_category_id': category_id,
                        'name': category_name,
                        'parent_name': parent_name
                    }
                    creat_data = self.env['goods.class'].create(vars)

            data_insert = {}
            type_url = 'http://api.epc.heqiauto.com/groups/4/category-virtual/1?resource=menu&client_id={}&secret_key={}'.format(client_id, secret_key)
            data = requests.get(url=type_url).text
            data = json.loads(data)
            category = {}
            for i in range(len(data['result'])):
                for j in range(len(data['result'][i]['category'])):
                    category[data['result'][i]['category'][j]['category_id']] = data['result'][i]['category'][j][
                        'category_name']
            for key in category.keys():
                brand_url = 'http://api.epc.heqiauto.com/part-brands?client_id={}&secret_key={}&category_id={}&brand_id=1'.format(client_id, secret_key, key)
                data = requests.get(url=brand_url).text
                data = json.loads(data)
                for i in range(len(data['result'])):
                    insert_cache = {}
                    insert_cache['code'] = data['result'][i]['code']
                    insert_cache['category_id'] = key
                    insert_cache['category_name'] = category[key]
                    insert_cache['brand_name'] = data['result'][i]['brand_name']
                    insert_cache['brand_id'] = data['result'][i]['brand_id']
                    form_code = str(key) + str(data['result'][i]['brand_id'])
                    data_insert[form_code] = insert_cache
            for key in data_insert:
                obj = self.env['epc.params'].search([('form_code', '=', key)])
                if obj:
                    name = data_insert[key]['category_name']
                    obj_1 = self.env['goods.class'].search([('name', '=', name)])
                    obj.write({
                        'code': data_insert[key]['code'],
                        'epc_category_id': obj_1.epc_category_id,
                        'category_name': obj_1.name,
                        'brand_name': data_insert[key]['brand_name'],
                        'epc_brand_id': data_insert[key]['brand_id'],
                    })
                else:
                    name = data_insert[key]['category_name']
                    obj = self.env['goods.class'].search([('name', '=', name)])
                    vars = {
                        'form_code': key,
                        'code': data_insert[key]['code'],
                        'category_id': obj.id,
                        'epc_category_id': obj.epc_category_id,
                        'category_name': obj.name,
                        'brand_name': data_insert[key]['brand_name'],
                        'epc_brand_id': data_insert[key]['brand_id'],
                    }
                    creat_data = self.env['epc.params'].create(vars)

            params = self.env['epc.params'].search([])

            for param in params:
                brand_name = param.brand_name
                if self.env['core.value'].search([('name', '=', brand_name)]):
                    obj = self.env['core.value'].search([('name', '=', brand_name)])
                    obj.write({
                        'company_id': 1,
                        'name': brand_name,
                        'type': 'brand',
                        'code': param.code,
                        'form_code': param.form_code,
                    })
                else:
                    vars = {
                        'company_id': 1,
                        'name': brand_name,
                        'type': 'brand',
                        'code': param.code,
                        'form_code': param.form_code,
                    }
                    creat_data = self.env['core.value'].create(vars)
        except Exception:
            raise ValueError(u'请求数据失败 请查看EPC参数配置是否符合要求')


class core_value(models.Model):
    _inherit = 'core.value'

    code = fields.Char(u'品牌code')
    form_code = fields.Char(u'唯一code')


class goods_class(models.Model):
    _inherit = 'goods.class'

    epc_category_id = fields.Char('产品类别id')
    parent_name = fields.Char('类别上级名称')


class EpcProduct(models.Model):
    _name = 'epc.product'
    _description = u'导入EPC产品信息'
    _rec_name = 'part_category'

    part_category = fields.Char(string=u"产品类别")
    epc_category_id = fields.Char(string=u"产品类别id")
    part_brand = fields.Char(string=u"产品品牌")
    part_brand_id = fields.Char(string=u'产品品牌id')
    part = fields.Char(string=u'产品key')
    psn = fields.Char(string=u'系统编码')
    epc_pn = fields.Char(string=u'配件编码')
    part_model = fields.Char(string=u'规格型号')
    part_name = fields.Char(string=u'配件名称')
    brand_manu_name = fields.Char(string=u'品牌名称')
    category_name = fields.Char(string=u'直属分类名称')
    series = fields.Char(string=u'等级、系列')
    pmanu_name = fields.Char(string=u'生产厂商')
    pmanu_code = fields.Char(string=u'出厂编码')
    pmanu_addr = fields.Char(string=u'产地')
    code = fields.Char(string=u'品牌编码')
    is_exist = fields.Char(string=u'存在状态')
    insert_line = fields.One2many('epc.line.product', 'order_id',u'明细行')
    state = fields.Selection([('draft', u'草稿'), ('done', u'已导入')], default='draft', string=u'状态', copy=False)
    level = fields.Selection(selection=[
        ('one', '1'),
        ('two', '2'),
        ('three', '3'),
    ])

    def epc_request_data(self):
        res_id = self.env['epc.wizard'].create(
            {
                'order_id':self.id,
                'level': 'one',
                'part_category': '',
                'epc_category_id':2,
            }
        )
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'epc.wizard',
            'name': u'产品类别选择',
            'res_id': res_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
            }
        }


class EpcWizard(models.TransientModel):
    _name = "epc.wizard"
    _description = u'创建EPC产品向导表'

    order_id = fields.Many2one('epc.product')
    part_category = fields.Many2one('goods.class')
    epc_category_id = fields.Char(string=u"产品类别id")
    part_brand = fields.Many2one('epc.params')
    part_brand_id = fields.Char(string=u'产品品牌id')
    part = fields.Char(string=u'产品名称')
    code = fields.Char(string=u'品牌编码')
    name_ids = fields.One2many('epc.name.wizard', 'wizard_id', u'明细')
    level = fields.Selection(selection=[
        ('one', '1'),
        ('two', '2'),
        ('three', '3'),
    ])

    @api.onchange('part_category')
    def _onchange_car_brand(self):
        self.part_brand = False

    def button_search_part(self):
        self.part_brand_id = self.part_brand.epc_brand_id
        self.code = self.part_brand.code
        self.epc_category_id = self.part_brand.epc_category_id
        part_data = self.get_part()
        a=[]

        for key in part_data.keys():
            a.append((key, part_data[key], False))
        self.env['epc.name.wizard'].search([]).unlink()

        part_line = ((0, 0, {
            # 'code': self.code,
            'part' : i[0],
            'part_name': i[1]['配件名称'],
            'brand_manu_name': i[1]['品牌名称'],
            'part_model': i[1]['规格型号'],
            'epc_pn': i[1]['配件编码'],
            'psn': i[1]['系统编码'],
            'category_name': i[1]['直属分类名称'],
            'series': i[1]['等级、系列'],
            'pmanu_name': i[1]['生产厂商'],
            'pmanu_code': i[1]['出厂编码'],
            'pmanu_addr': i[1]['产地'],
            'is_on_check': i[2],
        })for i in a if not self.env['goods'].search([('hq_pn', '=', i[1]['配件编码'])]))

        self.write({
            'level': 'three',
            'name_ids': part_line,
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'epc.wizard',
            'name': u'产品类别选择',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
            }
        }

    @api.multi
    def button_insert(self):
        insert_data = []
        for name_line in self.name_ids:
            if name_line.is_on_check == True :
                insert_data.append(name_line)
        insert_line = ((0, 0, {
            'part_name': i.part_name,
            'epc_category_id': self.epc_category_id,
            'part_brand_id': self.part_brand_id,
            'brand_manu_name': i.brand_manu_name,
            'part_model': i.part_model,
            'epc_pn': i.epc_pn,
            'code': self.code,
            'psn': i.psn,
            'category_name': i.category_name,
            'series': i.series,
            'pmanu_name': i.pmanu_name,
            'pmanu_code': i.pmanu_code,
            'pmanu_addr': i.pmanu_addr,
        }) for i in insert_data)
        obj = self.env['epc.product'].create(
                {
                    'part_category': self.part_brand.category_name,
                    'part_brand': self.part_brand.brand_name,
                    'insert_line': insert_line,
                }
            )

        brand_obj = self.env['core.value'].search([('name', '=', self.part_brand.brand_name)])
        if self.env['uom'].search([('name', '=', '个')]):
            uom_obj = self.env['uom'].search([('name', '=', '个')])
        else:
            uom_obj = self.env['uom'].create({
                'name', '=', '个'
            })

        for i in insert_data:
            level_objs = self.env['goods.class'].search([('name', '=', self.part_brand.category_name)], limit=1)
            categ_id = level_objs.id
            parent_category = level_objs.parent_name

            creat_data = self.env['goods'].create({
                'name': i.part_name,
                'uom_id': uom_obj.id,
                'goods_class_id': categ_id,
                'category_id': 5,
                'brand':brand_obj.id,
                'part_model': i.part_model,
                'epc_pn': i.psn,
                'hq_pn': i.epc_pn,
                'category_name': i.category_name,
                'parent_category': parent_category,
                'code': self.code,
                'series': i.series,
                'pmanu_name': i.pmanu_name,
                'pmanu_code': i.pmanu_code,
                'pmanu_addr': i.pmanu_addr,
            })

    def get_part(self):
        try:
            obj_conf = self.env['product.config.settings'].search([], order='id desc', limit=1)
            client_id = obj_conf.client_id
            secret_key = obj_conf.secret_key

            url = "http://api.epc.heqiauto.com/groups/4/category-virtual/{}/parts?client_id={}&secret_key={}&brand_id={}".format(
                self.epc_category_id, client_id,  secret_key, self.part_brand_id)
            response = requests.request("GET", url).text
            json_data = json.loads(response)
            page = json_data['result']['pageCount']
            part_data = {}
            for i in range(page):
                url = "http://api.epc.heqiauto.com/groups/4/category-virtual/{}/parts?client_id={}&secret_key={}&brand_id={}&page={}".format(
                    self.epc_category_id, client_id, secret_key,  self.part_brand_id, i + 1)
                response = requests.request("GET", url).text
                json_data = json.loads(response)
                target_data = json_data['result']['items']
                for i in range(len(target_data)):
                    data = {}
                    data['系统编码'] = target_data[i]['psn']
                    data['配件编码'] = target_data[i]['pn']
                    data['规格型号'] = target_data[i]['part_model']
                    data['配件名称'] = target_data[i]['part_name']
                    data['品牌名称'] = target_data[i]['brand_manu_name']
                    data['直属分类名称'] = target_data[i]['category_name']
                    data['等级、系列'] = target_data[i]['series']
                    data['生产厂商'] = target_data[i]['pmanu_name']
                    data['出厂编码'] = target_data[i]['pmanu_code']
                    data['产地'] = target_data[i]['pmanu_addr']
                    part_data[target_data[i]['pmanu_code']] = data
            return part_data
        except Exception:
            raise ValueError(u'请求数据失败 请查看EPC参数配置是否符合要求')


class EpcNameWizard(models.TransientModel):
    _name = 'epc.name.wizard'
    _description = u'向导明细名称表'

    wizard_id = fields.Many2one('epc.wizard')
    part = fields.Char(string=u"产品名称")
    part_Name_id = fields.Char(string=u'产品名称id')
    psn = fields.Char(string=u'系统编码')
    epc_pn = fields.Char(string=u'配件编码')
    part_model = fields.Char(string=u'规格型号')
    part_name = fields.Char(string=u'配件名称')
    brand_manu_name = fields.Char(string=u'品牌名称')
    category_name = fields.Char(string=u'直属分类名称')
    series = fields.Char(string=u'等级、系列')
    pmanu_name = fields.Char(string=u'生产厂商')
    code = fields.Char(string=u'品牌编码')
    pmanu_code = fields.Char(string=u'出厂编码')
    pmanu_addr = fields.Char(string=u'产地')
    is_on_check = fields.Boolean(string=u'是否被选中', default=False)


class EpcLineProduct(models.Model):
    _name = 'epc.line.product'
    _description = u'明细行'

    order_id = fields.Many2one('epc.product')
    part = fields.Char(string=u"产品名称")
    part_Name_id = fields.Char(string=u'产品名称id')
    epc_category_id = fields.Char(string=u"产品类别id")
    part_brand_id = fields.Char(string=u'产品品牌id')
    psn = fields.Char(string=u'系统编码')
    epc_pn = fields.Char(string=u'配件编码')
    code = fields.Char(string=u'品牌编码')
    is_exist = fields.Char(string=u'存在状态')
    part_model = fields.Char(string=u'规格型号')
    part_name = fields.Char(string=u'配件名称')
    brand_manu_name = fields.Char(string=u'品牌名称')
    category_name = fields.Char(string=u'直属分类名称')
    series = fields.Char(string=u'等级、系列')
    pmanu_name = fields.Char(string=u'生产厂商')
    pmanu_code = fields.Char(string=u'出厂编码')
    pmanu_addr = fields.Char(string=u'产地')
    is_on_check = fields.Boolean(string=u'是否被选中', default=False)


class product_template(models.Model):
    _inherit = 'goods'

    psn = fields.Char(string=u'系统编码')
    parent_category = fields.Char(string=u"产品类别父类")
    brand_manu_name = fields.Char(string=u'品牌名称')
    code = fields.Char(string=u'品牌编码')
    part_model = fields.Char(string=u'规格型号')
    category_name = fields.Char(string=u'直属分类名称')
    series = fields.Char(string=u'等级、系列')
    pmanu_name = fields.Char(string=u'生产厂商')
    pmanu_code = fields.Char(string=u'出厂编码')
    pmanu_addr = fields.Char(string=u'产地')
    hq_pn = fields.Char(string=u'配件编码')

