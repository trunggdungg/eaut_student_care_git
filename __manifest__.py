# -*- coding: utf-8 -*-
{
    'name': 'Chăm sóc sinh viên git',
    'version': '19.0.1.0.0',
    'summary': 'Quản lý điểm, thời khóa biểu và tình trạng học tập của sinh viên',
    'description': """
Chăm sóc sinh viên:
- Quản lý sinh viên, khoa, ngành, khóa (kế thừa từ eaut_base).
- Quản lý bảng điểm sinh viên theo từng học kỳ, môn học.
- Theo dõi môn học sinh viên đang nợ (chưa đạt).
- Quản lý thời khóa biểu sinh viên.
- Trạng thái sinh viên (danh mục do quản trị viên tự cấu hình).
- Smart button liên kết Phiếu hỗ trợ (eaut_helpdesk) theo mã sinh viên / email / số điện thoại.
""",
    'category': 'EAUT',
    'author': 'EAUT',
    'website': '',
    'depends': [
        'base',
        'mail',
        'eaut_base',
        'eaut_helpdesk',
    ],
    'data': [
        'security/eaut_student_care_security.xml',
        'security/ir.model.access.csv',

        'views/eaut_student_care_state_views.xml',
        'views/eaut_student_care_semester_views.xml',
        'views/eaut_student_care_course_views.xml',
        'views/eaut_student_care_grade_views.xml',
        'views/eaut_student_care_timetable_views.xml',
        'views/eaut_base_student_views.xml',
        'views/eaut_student_care_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
