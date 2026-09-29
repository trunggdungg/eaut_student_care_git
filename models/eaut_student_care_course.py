# -*- coding: utf-8 -*-

from odoo import fields, models


class EautStudentCareCourse(models.Model):
    _name = 'eaut.student.care.course'
    _description = 'Môn học'
    _order = 'name'

    name = fields.Char(string='Tên môn học', required=True)
    code = fields.Char(string='Mã môn học')
    credit = fields.Float(string='Số tín chỉ')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('course_code_unique', 'unique(code)', 'Mã môn học đã tồn tại!'),
    ]
