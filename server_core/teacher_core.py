# coding:utf-8
import random
import assist_tools
import manage_timer
import textwrap

class TeacherCore:
    def __init__(self, teacher_id):
        self.teacher_id = teacher_id
        self.tool = assist_tools.AssistTools()
        self.manager = manage_timer.ManageTimer()

    def check_in(self, list):
        course_id = raw_input('输入课程号：')
        random_list = []  # 抽点名单
        if self.manager.course_check(self.teacher_id, course_id) == 0:
            return 0


        tem_list = [course_id, 1, self.tool.get_end_time(), self.tool.get_over_time(self.tool.get_local_time()), self.teacher_id, random_list]
        self.manager.write_seq(self.teacher_id, course_id)
        self.manager.start_init(tem_list, list)
        return self.manager.list_add(tem_list, list)

    def random_check_in(self, list):
        # 时间窗口是否开启 现在时间是否在时间窗口结束五分钟之前
        if self.manager.has_r(list, self.teacher_id) == 0:
            print '你还没有开启考勤'
            return 0
        if self.manager.can_random(list, self.teacher_id) == 0:
            print '剩余时间不足,无法开启'
            return 0
        self.manager.write_seq(self.teacher_id, self.manager.has_r(list, self.teacher_id))
        try:
            nums = int(raw_input('请您输入要抽取的人数：'))
            if nums <= 0:
                print '输入异常'
                return 0
            random_list = []
            for row in list:
                if row[4] == self.teacher_id:
                    stu = [row for row in self.tool.get_stu_list(row[0], 1)]
                    random_list = random.sample(stu, nums)
                    break
        except:
            print '输入异常'
            return 0
        print '开启成功,如下:'
        print(textwrap.fill(str(random_list), width=40))
        self.manager.random_change_detail(self.teacher_id, list, random_list)
        return self.manager.set_r(3, list, self.teacher_id, random_list) # 未完成

    def exe_lea(self, list):
        if self.manager.has_r(list, self.teacher_id) != 0:
            print '你还有正在进行的考勤,无法进行请假审批'
            return 0
        self.manager.exe_lea(self.teacher_id)

    def maintain(self, list):  # 修改学生记录
        if self.manager.has_r(list, self.teacher_id) != 0:
            print '你还有正在进行的考勤,无法使用此功能'
            return 0
        if self.manager.get_lea_list(self.teacher_id):
            print '你有未处理的假条,无法维护考勤记录'
            return 0
        course_id = raw_input('输入课程号：')
        if self.tool.get_own_course(self.teacher_id).count(course_id) == 0:
            print '此课程号不在你处理的范围内'
            return 0
        seq_id = raw_input('输入考勤次序号：')
        if self.manager.seq_id_check(seq_id, course_id) == 0:
            return 0
        student_id = raw_input('输入学号：')
        if self.tool.get_stu_list(course_id, 1).count(student_id) == 0:
            print '该课程无此学号'
            return 0
        data = [self.teacher_id, course_id, seq_id, student_id]
        print '%s考勤的状态是：%s' % (self.tool.get_student_name(student_id), self.manager.get_detail_status(data))
        choose = raw_input('你要修改成？ 1,出勤 2,缺勤 3,请假 4,迟到 5,早退 输入其它退出')
        dict = {'1':'出勤', '2':'缺勤', '3':'请假', '4':'迟到', '5':'早退'}
        if choose <= '0':
            return 0
        try:
            detail = [None, None, 'man', True, dict[choose]]
        except:
            return 0
        self.manager.alter_detail(data, detail)
        self.manager.alter_sum(data, detail)
        print '修改成功'

    def man_check_in(self, list): # 批量增加 下课
        if self.manager.has_r(list, self.teacher_id) != 0:
            return 0
        course_id = raw_input('输入课程号：')
        if self.manager.course_check(self.teacher_id, course_id) == 0:
            return 0
        self.manager.init_data(course_id)
        self.manager.write_seq(self.teacher_id, course_id)

    def show_recent_atd(self):  # for tea
        self.manager.get_recent_atd(self.teacher_id)

    def show_sum_adt(self):
        course_id = raw_input('输入课程号：')
        self.manager.get_sum_atd(self.teacher_id, course_id)


if __name__ == '__main__':
    t = TeacherCore('2004355')
    list = t.maintain([])
