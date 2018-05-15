#! coding:utf-8
from core import check_util, assist_tools, timer_queue
import threading

class TeacherFun:
    def __init__(self):
        self.check = check_util.CheckTools()
        self.tool = assist_tools.AssistTools()
        self.timer = timer_queue.TimerQueue()

    #  2.0 查看我的course_id (wechat_id)
    def show_allcourseid(self, wechat_id):
        if self.check.wechat_tea_check(wechat_id):
            self.tool.get_courseid_tea(wechat_id)

    #  2.1 自助考勤（wechat_id，course_id，timer_list）
    def checkin_auto(self, wechat_id, course_id):
        if self.check.wechat_tea_check(wechat_id) and self.check.courseid_check(wechat_id, course_id):
            print("auto: " + wechat_id + " 已经自助考勤")
            self.timer.enter_qeque(wechat_id, course_id)
            self.tool.init_detailcsv(course_id, ["auto", " "])
            self.tool.updata_seq(course_id)

    #  2.2 抽点（wechat_id, timer_list)
    def checkin_random(self, wechat_id):
        if self.check.wechat_tea_check(wechat_id) and self.timer.isexist_wechat(wechat_id) \
           and self.tool.get_localtime() < self.timer.get_endtime(wechat_id)-5*60:
            print("random: "+wechat_id+" 可以抽点")
            nums = int(input("请输入抽点人数:"))
            self.check.numsrandom_check(nums)
            course_id = self.timer.get_courseid(wechat_id)
            random_list = self.tool.generate_random(course_id, nums)
            self.tool.init_randomdetailcsv(course_id, random_list)
            self.tool.updata_seq(course_id)

    #  2.3 手工（wechat_id，course_id）
    def checkin_man(self, wechat_id, course_id):
        if self.check.wechat_tea_check(wechat_id) and self.check.courseid_check(wechat_id, course_id) \
           and not self.timer.isexist_wechat(wechat_id):
            # 初始化所有的学生为缺勤
            # bug ： 教师退出，一会再手工受理，可以选择修改学状态

            self.tool.init_detailcsv(course_id, ["man", "出勤"])
            self.tool.updata_seq(course_id)
            print()


    #  2.4 修改（wechat_id，course_id，seq_id）
    def checkin_alter(self,wechat_id, course_id, seq_id):
        if self.check.wechat_tea_check(wechat_id) and self.check.courseid_check(wechat_id, course_id) \
           and self.check.isseqexist_check(seq_id)and not self.timer.isexist_wechat(wechat_id):
            while(1):
                stu_id = input("请输入学号（输入0退出）:")
                if stu_id == "0": break
                self.check.courseid_stu_check(stu_id)
                checkin_result = input("请设置考勤状态（输入0退出）:")
                if stu_id == "0": break
                self.check.checkinresult_check(checkin_result)
                #  更新detail.csv    ###################################################################
                pass

    #  2.5 汇总 (wechat_id, course_id)
    def checkin_sumup(self, wechat_id, course_id):
        if self.check.wechat_tea_check(wechat_id) and not self.timer.isexist_wechat(wechat_id):
            self.tool.calculateResult(course_id)
            self.tool.sumup_format(course_id)

    #  2.6  查看最近 (wechat_id)
    def checkin_recentshow(self, wechat_id):
        if self.check.wechat_tea_check(wechat_id): pass
        #  直接seq中的信息，获取相关url得到detail
        #  统计：出勤率，缺勤率等


if __name__ == "__main__":
    t = TeacherFun()
    t.checkin_auto("wechat1", "555")
    t.checkin_alter("wechat1", "555","1")
