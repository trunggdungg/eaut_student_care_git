# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EautBaseStudent(models.Model):
    _inherit = 'eaut.base.student'

    # Trạng thái sinh viên - danh mục do quản trị viên tự tạo/cấu hình
    state_id = fields.Many2one(
        'eaut.student.care.state',
        string='Trạng thái',
        tracking=True,
    )

    classroom_id = fields.Many2one(
        'eaut.student.care.classroom',
        string='Lớp',
        tracking=True,
    )
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    ], string='Giới tính')

    grade_ids = fields.One2many('eaut.student.care.grade', 'student_id', string='Bảng điểm')
    timetable_ids = fields.One2many('eaut.student.care.timetable', 'student_id', string='Thời khóa biểu')
    conduct_ids = fields.One2many('eaut.student.care.conduct', 'student_id', string='Điểm rèn luyện')

    grade_count = fields.Integer(string='Số môn đã có điểm', compute='_compute_grade_count')
    debt_course_count = fields.Integer(string='Số môn đang nợ', compute='_compute_grade_count')
    timetable_count = fields.Integer(string='Số buổi học', compute='_compute_timetable_count')
    conduct_count = fields.Integer(string='Số kỳ có điểm rèn luyện', compute='_compute_conduct_count')
    helpdesk_ticket_count = fields.Integer(string='Số phiếu hỗ trợ', compute='_compute_helpdesk_ticket_count')

    def _compute_grade_count(self):
        Grade = self.env['eaut.student.care.grade']
        for student in self:
            student.grade_count = Grade.search_count([('student_id', '=', student.id)])
            student.debt_course_count = Grade.search_count([
                ('student_id', '=', student.id),
                ('result', '=', 'failed'),
            ])

    def _compute_timetable_count(self):
        Timetable = self.env['eaut.student.care.timetable']
        for student in self:
            student.timetable_count = Timetable.search_count([('student_id', '=', student.id)])

    def _compute_conduct_count(self):
        Conduct = self.env['eaut.student.care.conduct']
        for student in self:
            student.conduct_count = Conduct.search_count([('student_id', '=', student.id)])

    def _compute_helpdesk_ticket_count(self):
        Ticket = self.env['helpdesk.ticket']
        for student in self:
            student.helpdesk_ticket_count = Ticket.search_count(student._helpdesk_ticket_domain())

    def _helpdesk_ticket_domain(self):
        """Phiếu hỗ trợ (eaut_helpdesk) không có quan hệ trực tiếp tới sinh viên,
        nên đối chiếu theo mã sinh viên / email / số điện thoại."""
        self.ensure_one()
        matches = []
        if self.code:
            matches.append(('student_code', '=', self.code))
        if self.email:
            matches.append(('partner_email', '=', self.email))
        if self.phone:
            matches.append(('partner_phone', '=', self.phone))
        if not matches:
            return [('id', '=', 0)]
        # Domain OR theo ký pháp tiền tố: n điều kiện cần (n-1) toán tử '|'.
        return ['|'] * (len(matches) - 1) + matches

    def action_view_grades(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Bảng điểm'),
            'res_model': 'eaut.student.care.grade',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_view_debt_courses(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Môn đang nợ'),
            'res_model': 'eaut.student.care.grade',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id), ('result', '=', 'failed')],
            'context': {'default_student_id': self.id},
        }

    def action_view_timetable(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Thời khóa biểu'),
            'res_model': 'eaut.student.care.timetable',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_view_conduct(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Điểm rèn luyện'),
            'res_model': 'eaut.student.care.conduct',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_sync_data(self):
        """Đồng bộ điểm, chuyên cần, rèn luyện, TKB... từ hệ thống đào tạo bên ngoài.

        Việc kết nối API thực tế sẽ được cấu hình sau; hiện tại đây chỉ là
        điểm vào (nút bấm / action hàng loạt) để khi có thông tin API sẽ
        cắm logic gọi API + upsert dữ liệu vào đây mà không cần đổi giao diện.
        """
        raise UserError(_(
            'Chưa cấu hình kết nối tới hệ thống dữ liệu bên ngoài. '
            'Vui lòng liên hệ quản trị viên để thiết lập trước khi đồng bộ.'
        ))

    def generate_demo_data(self):
        State = self.env['eaut.student.care.state']
        Semester = self.env['eaut.student.care.semester']
        Course = self.env['eaut.student.care.course']
        Classroom = self.env['eaut.student.care.classroom']
        Grade = self.env['eaut.student.care.grade']
        Conduct = self.env['eaut.student.care.conduct']
        Major = self.env['eaut.base.major']

        def get_or_create(Model, domain, values):
            return Model.search(domain, limit=1) or Model.create(values)

        for name in ('Đang học', 'Bảo lưu', 'Thôi học'):
            get_or_create(State, [('name', '=', name)], {'name': name})

        semesters = [
            get_or_create(Semester, [('name', '=', name)], {
                'name': name, 'date_start': date_start, 'date_end': date_end,
            })
            for name, date_start, date_end in (
                ('Học kỳ 1 - 2025-2026', '2025-09-01', '2026-01-15'),
                ('Học kỳ 2 - 2025-2026', '2026-02-01', '2026-06-15'),
            )
        ]

        courses = [
            get_or_create(Course, [('code', '=', code)], {
                'code': code, 'name': name, 'credit': credit,
            })
            for code, name, credit in (
                ('LTC001', 'Lập trình C', 3),
                ('CSDL001', 'Cơ sở dữ liệu', 3),
                ('GT001', 'Giải tích 1', 2),
            )
        ]

        major = Major.search([], limit=1)
        classroom = get_or_create(Classroom, [('name', '=', 'Lớp demo')], {
            'name': 'Lớp demo', 'major_id': major.id if major else False,
        })

        students = self.search([], limit=20)
        if not students:
            raise UserError(_(
                'Chưa có sinh viên nào trong hệ thống. '
                'Vui lòng tạo ít nhất 1 sinh viên trước khi tạo dữ liệu mẫu.'
            ))

        sample_scores = [8.5, 7.0, 9.0, 5.5]
        grade_created = 0
        conduct_created = 0
        for student in students:
            if not student.classroom_id:
                student.classroom_id = classroom.id
            for s_index, semester in enumerate(semesters):
                if not Conduct.search_count([
                    ('student_id', '=', student.id), ('semester_id', '=', semester.id),
                ]):
                    Conduct.create({
                        'student_id': student.id,
                        'semester_id': semester.id,
                        'score': 85 - s_index * 5,
                        'classification': 'Tốt',
                    })
                    conduct_created += 1
                for c_index, course in enumerate(courses):
                    if Grade.search_count([
                        ('student_id', '=', student.id),
                        ('semester_id', '=', semester.id),
                        ('course_id', '=', course.id),
                    ]):
                        continue
                    score = sample_scores[(s_index + c_index) % len(sample_scores)]
                    Grade.create({
                        'student_id': student.id,
                        'semester_id': semester.id,
                        'course_id': course.id,
                        'score_10': score,
                        'score_4': round(score / 2.5, 1),
                        'score_letter': 'A' if score >= 8.5 else ('B' if score >= 7 else 'C'),
                        'result': 'passed' if score >= 4 else 'failed',
                    })
                    grade_created += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Đã tạo dữ liệu mẫu'),
                'message': _('%s dòng điểm, %s dòng điểm rèn luyện cho %s sinh viên.') % (
                    grade_created, conduct_created, len(students)),
                'type': 'success',
                'sticky': False,
            },
        }

    def action_view_helpdesk_tickets(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Phiếu hỗ trợ'),
            'res_model': 'helpdesk.ticket',
            'view_mode': 'list,form',
            'domain': self._helpdesk_ticket_domain(),
        }
