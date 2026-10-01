# -*- coding: utf-8 -*-

from odoo import fields, models


class EautStudentCareClassroom(models.Model):
    _name = 'eaut.student.care.classroom'
    _description = 'Lớp'
    _order = 'name'

    name = fields.Char(string='Tên lớp', required=True)
    major_id = fields.Many2one('eaut.base.major', string='Ngành')
    active = fields.Boolean(default=True)

    external_id = fields.Char(string='Mã đồng bộ', readonly=True, copy=False)
    last_synced_at = fields.Datetime(string='Đồng bộ lần cuối', readonly=True, copy=False)

    _sql_constraints = [
        ('classroom_name_unique', 'unique(name)', 'Tên lớp đã tồn tại!'),
    ]