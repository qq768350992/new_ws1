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
        # r_lock = threading.RLock()     # mutex互斥
        # with r_lock:
        if self.check.wechat_tea_check(wechat_id) and self.check.courseid_check(wechat_id, course_id):
            self.timer.enter_qeque(wechat_id, course_id)
            print("auto: " + wechat_id + " 可以自助考勤")
        #  删除random文件
        pass
        #  维护 detail.csv   ###################################################################################
        pass
        #  维护 seq.csv   不是我该做的，我不做  ###################################################################
        pass

    #  2.2 抽点（wechat_id, timer_list)
    def checkin_random(self, wechat_id):
        if self.check.wechat_tea_check(wechat_id) and self.timer.isexist_wechat(wechat_id) \
           and self.tool.get_localtime() < self.timer.get_endtime(wechat_id)-5*60:
            print("random: "+wechat_id+" 可以抽点")
            nums = int(input("请输入抽点人数:"))
            # 检查
            # 检查
            # 检查
            random_list = self.tool.generate_random(self.timer.get_courseid(wechat_id), nums)
            self.tool.init_randomdetailcsv(self.timer.get_courseid(wechat_id), random_list)
            #  维护 seq.csv   不是我该做的，我不做  ###################################################################
            pass

    #  2.3 手工（wechat_id，course_id）
    def checkin_man(self, wechat_id, course_id):
        if self.check.wechat_tea_check(wechat_id) and self.check.courseid_check(wechat_id, course_id) \
           and not self.timer.isexist_wechat(wechat_id):
            while(1):
                stu_id = input("请输入学号（输入0退出）:")
                if stu_id == "0": break
                self.check.courseid_stu_check(stu_id)
                checkin_result = input("请设置考勤状态（输入0退出）:")
                if checkin_result == "0": break
                self.check.checkinresult_check(checkin_result)
                #  更新detail         ###################################################################
                pass
                #  自动获取seq 调用0.1 ###################################################################
                pass
                #  维护seq.csv       ###################################################################
                pass

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
