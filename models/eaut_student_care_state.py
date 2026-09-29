# -*- coding: utf-8 -*-

from odoo import fields, models


class EautStudentCareState(models.Model):
    _name = 'eaut.student.care.state'
    _description = 'Trạng thái sinh viên'
    _order = 'sequence, id'

    name = fields.Char(string='Tên', required=True)
    sequence = fields.Integer(string='Thứ tự', default=10)
    color = fields.Integer(string='Màu sắc')
    description = fields.Text(string='Mô tả')
    active = fields.Boolean(default=True)
