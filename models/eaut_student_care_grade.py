# -*- coding: utf-8 -*-

from odoo import fields, models


class EautStudentCareGrade(models.Model):
    _name = 'eaut.student.care.grade'
    _description = 'Bảng điểm'
    _order = 'semester_id desc, course_id, lan_hoc, lan_thi'

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
    course_id = fields.Many2one(
        'eaut.student.care.course',
        string='Môn học',
        required=True,
    )

    lan_hoc = fields.Integer(string='Lần học', default=1)
    lan_thi = fields.Integer(string='Lần thi', default=1)

    score_cc = fields.Float(string='Điểm chuyên cần (CC)')
    score_gk = fields.Float(string='Điểm giữa kỳ (GK)')
    score_thi = fields.Float(string='Điểm thi (THI)')

    score_10 = fields.Float(string='Điểm hệ 10')
    score_4 = fields.Float(string='Điểm hệ 4')
    score_letter = fields.Char(string='Điểm chữ')

    result = fields.Selection([
        ('passed', 'Đạt'),
        ('failed', 'Không đạt'),
    ], string='Đánh giá')

    note = fields.Char(string='Ghi chú')

    external_id = fields.Char(string='Mã đồng bộ', readonly=True, copy=False)
    last_synced_at = fields.Datetime(string='Đồng bộ lần cuối', readonly=True, copy=False)

    _sql_constraints = [
        ('student_semester_course_attempt_unique',
         'unique(student_id, semester_id, course_id, lan_hoc, lan_thi)',
         'Sinh viên đã có điểm môn học này (cùng lần học/lần thi) trong học kỳ này!'),
    ]
