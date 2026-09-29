# -*- coding: utf-8 -*-

from odoo import api, fields, models

# Ngưỡng điểm đạt môn (thang điểm 10). Có thể tách thành field cấu hình sau này
# nếu từng môn/chương trình cần ngưỡng khác nhau.
PASS_SCORE = 4.0


class EautStudentCareGrade(models.Model):
    _name = 'eaut.student.care.grade'
    _description = 'Bảng điểm'
    _order = 'semester_id desc, course_id'

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
    score = fields.Float(string='Điểm (hệ 10)')
    note = fields.Char(string='Ghi chú')

    result = fields.Selection([
        ('passed', 'Đạt'),
        ('failed', 'Nợ môn'),
    ], string='Kết quả', compute='_compute_result', store=True)

    _sql_constraints = [
        ('student_semester_course_unique', 'unique(student_id, semester_id, course_id)',
         'Sinh viên đã có điểm môn học này trong học kỳ này!'),
    ]

    @api.depends('score')
    def _compute_result(self):
        for rec in self:
            rec.result = 'passed' if rec.score >= PASS_SCORE else 'failed'
