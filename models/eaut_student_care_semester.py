# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EautStudentCareSemester(models.Model):
    _name = 'eaut.student.care.semester'
    _description = 'Học kỳ'
    _order = 'date_start desc, sequence'

    name = fields.Char(string='Tên học kỳ', required=True)
    sequence = fields.Integer(string='Thứ tự', default=10)
    date_start = fields.Date(string='Ngày bắt đầu')
    date_end = fields.Date(string='Ngày kết thúc')
    active = fields.Boolean(default=True)

    grade_ids = fields.One2many('eaut.student.care.grade', 'semester_id', string='Bảng điểm')
    timetable_ids = fields.One2many('eaut.student.care.timetable', 'semester_id', string='Thời khóa biểu')

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_start > rec.date_end:
                raise ValidationError(_('Ngày bắt đầu không được sau ngày kết thúc.'))
