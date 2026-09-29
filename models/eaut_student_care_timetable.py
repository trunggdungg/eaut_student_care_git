# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EautStudentCareTimetable(models.Model):
    _name = 'eaut.student.care.timetable'
    _description = 'Thời khóa biểu'
    _order = 'semester_id desc, weekday, time_start'

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
    weekday = fields.Selection([
        ('0', 'Thứ 2'),
        ('1', 'Thứ 3'),
        ('2', 'Thứ 4'),
        ('3', 'Thứ 5'),
        ('4', 'Thứ 6'),
        ('5', 'Thứ 7'),
        ('6', 'Chủ nhật'),
    ], string='Ngày trong tuần', required=True)
    time_start = fields.Float(string='Giờ bắt đầu')
    time_end = fields.Float(string='Giờ kết thúc')
    room = fields.Char(string='Phòng học')
    teacher = fields.Char(string='Giảng viên')
    note = fields.Char(string='Ghi chú')

    @api.constrains('time_start', 'time_end')
    def _check_time(self):
        for rec in self:
            if rec.time_start and rec.time_end and rec.time_start >= rec.time_end:
                raise ValidationError(_('Giờ bắt đầu phải trước giờ kết thúc.'))
