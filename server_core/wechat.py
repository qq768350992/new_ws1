# coding:utf-8


class Run:
    def __init__(self):
        self.list = []

    def student(self, student_id):
        import student_core
        s = student_core.StudentCore(student_id)
        while 1:
            print '--------学生--------'
            print '--1.考勤------------'
            print '--2.请假------------'
            print '--3.查看当前考勤-----'
            print '--4.查看历史考勤-----'
            print '--0.退出------------'
            choose = raw_input('请输入:')
            if choose == '1':
                s.stu_check_in(self.list)
            elif choose == '2':
                s.stu_lea(self.list)
            elif choose == '3':
                s.show_current_atd(self.list)
            elif choose == '4':
                s.show_history_atd()
            else:
                print '无此选项'

    def teacher(self, teacher_id):
        import teacher_core
        t = teacher_core.TeacherCore(teacher_id)
        while 1:
            print '--------教师--------'
            print '--1.开启考勤---------'
            print '--2.开启抽点考勤------'
            print '--3.请假审批---------'
            print '--4.维护考勤记录------'
            print '--5.批量增加考勤记录--'
            print '--6.查看最近考勤------'
            print '--7.查看出勤统计表----'
            print '--8.设置出勤限制时间--'
            print '--9.维护学生信息------'
            choose = raw_input('请输入:')
            if choose == '1':
                self.list = t.check_in(self.list)
            elif choose == '2':
                self.list = t.random_check_in(self.list)
            elif choose == '3':
                t.exe_lea(self.list)
            elif choose == '4':
                t.maintain(self.list)
            elif choose == '5':
                t.man_check_in(self.list)
            elif choose == '6':
                t.show_recent_atd()
            elif choose == '7':
                t.show_sum_adt()
            elif choose == '8':
                t.set_time()
            elif choose == '9':
                pass
            else:
                print '无此选项'
