# -*- coding: utf-8 -*-

from odoo import fields, models


class EautStudentCareMajorCourse(models.Model):
    _name = 'eaut.student.care.major.course'
    _description = 'Khung chương trình đào tạo'
    _order = 'major_id, semester_order, sequence'

    major_id = fields.Many2one(
        'eaut.base.major',
        string='Ngành',
        required=True,
        ondelete='cascade',
        index=True,
    )
    course_id = fields.Many2one(
        'eaut.student.care.course',
        string='Môn học',
        required=True,
        ondelete='cascade',
    )
    credit = fields.Float(related='course_id.credit', string='Số tín chỉ', readonly=True)
    is_required = fields.Boolean(string='Bắt buộc', default=True)
    semester_order = fields.Integer(string='Học kỳ (chuẩn)')
    sequence = fields.Integer(string='Thứ tự', default=10)

    external_id = fields.Char(string='Mã đồng bộ', readonly=True, copy=False)
    last_synced_at = fields.Datetime(string='Đồng bộ lần cuối', readonly=True, copy=False)

    _sql_constraints = [
        ('major_course_unique', 'unique(major_id, course_id)',
         'Môn học này đã có trong khung chương trình của ngành!'),
    ]
