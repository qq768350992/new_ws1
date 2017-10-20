# coding:utf-8
import assist_tools
import manage_timer


class StudentCore:
    def __init__(self, student_id):
        self.student_id = student_id
        self.tool = assist_tools.AssistTools()
        self.manager = manage_timer.ManageTimer()

    def stu_check_in(self, list):
        if self.manager.is_timer_exist(self.student_id, list) == 0: # 检测自己的课头是否存在
            return 0
        if self.manager.is_alter(self.student_id, 1, list) == 0: # 检测是否请过假
            return 0
        proof_path = raw_input('请提交样本文件：')
        issucc = True
        if self.manager.stu_start_checkin(self.student_id, list, [self.tool.get_true_time(), proof_path, 'auto', issucc, ' ']) == 0:
            return 0

    def stu_lea(self, list):
        if self.manager.is_timer_exist(self.student_id, list) == 0: # 检测自己的课头是否存在
            return 0
        if self.manager.is_alter(self.student_id, 2, list) == 0: # 检测是否考过勤
            return 0
        proof_path = raw_input('请提交样本文件：')
        if self.manager.stu_start_checkin(self.student_id, list, [self.tool.get_true_time(), proof_path, 'auto', ' ', '请假']) == 0:
            return 0

    def show_current_atd(self, list): # for stu
        if self.manager.is_timer_exist(self.student_id, list) == 0: # 检测自己的课头是否存在
            return 0
        self.manager.get_current_atd(self.student_id, list)
