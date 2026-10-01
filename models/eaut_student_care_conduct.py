# -*- coding: utf-8 -*-

from odoo import fields, models


class EautStudentCareConduct(models.Model):
    _name = 'eaut.student.care.conduct'
    _description = 'Điểm rèn luyện'
    _order = 'semester_id desc'

    student_id = fields.Many2one(
        'eaut.base.student',
        string='Sinh viên',
        required=True,
        ondelete='cascade',
        index=True,
    )
    semester_id = fields.Many2one(
        'eaut.student.care.semester',
        string='Học kỳ',
        required=True,
        index=True,
    )
    score = fields.Float(string='Điểm rèn luyện')
    classification = fields.Char(string='Xếp loại')
    note = fields.Char(string='Ghi chú')

    external_id = fields.Char(string='Mã đồng bộ', readonly=True, copy=False)
    last_synced_at = fields.Datetime(string='Đồng bộ lần cuối', readonly=True, copy=False)

    _sql_constraints = [
        ('student_semester_unique', 'unique(student_id, semester_id)',
         'Sinh viên đã có điểm rèn luyện cho học kỳ này!'),
    ]