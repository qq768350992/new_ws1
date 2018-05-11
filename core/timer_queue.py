#! coding:utf-8
import re, configparser, threading
from core import assist_tools
from databaseoperation import opt

class TimerQueue:
    def __init__(self):
        self.opt = opt.Opt()
        self.tool = assist_tools.AssistTools()
        self.timer_list = [   ["wechat1", "123", [52200, 57900],["软件1601","软件1602"]],
                              ["wonka80", "51610189", [52200, 57900],["软件1603","软件1604"]], ]
    def init_tcb(self, wechat_id, course_id):
        return [wechat_id, course_id, self.get_sectime(self.tool.get_localtime()), self.tool.get_classnamelist(course_id)]

    #  4.1 获取sectime(url) 上课区间包括开始和结束
    def get_sectime(self,start_time):
        cf = configparser.ConfigParser()
        cf.read('../interior/settings.ini')  ###########################################################################################################3
        info = [[row[0],row[1]] for row in map((lambda x: [int(x[0])*3600+int(x[1])*60, int(x[2])*3600+int(x[3])*60]),
                                               map((lambda x: re.split('-|:', x[1])), cf.items('sectime')))]
        if start_time < info[0][0] or int(start_time) > info[-1][0]:
            return info[0]
        for row in info:
            if start_time >= row[0] and start_time < row[1]:
                return row
            elif start_time >= row[1] and start_time < info[1+info.index(row)][0]:
                return info[1+info.index(row)]

    #  4.4 进队检测与处理（wechat_id, course_id）
    def enter_check(self, course_id):
        if not self.timer_list: return True
        for row in self.timer_list:
            if set(row[3]) & set(self.tool.get_classnamelist(course_id)):
                if self.get_sectime(self.tool.get_localtime()) == row[2]:
                    print("error: 被"+ row[0] +"占用，无法开启")
                    return False
                else:
                    self.depart_queque(row[0])
                    print("已将"+row[0]+"踢出")
                    return True
        return True

    #  4.5 进队（wechat_id, course_id）
    def enter_qeque(self, wechat_id, course_id):
        if self.enter_check(course_id):
            self.timer_list.append(self.init_tcb(wechat_id, course_id))
            t = threading.Timer(self.tool.get_timerwindow(), self.depart_queque, (wechat_id,)).start()

    #  4.6 出队（wechat_id, timer_list）
    def depart_queque(self, wechat_id):
        if self.timer_list:
            for row in self.timer_list:
                if wechat_id == row[0]:
                    del (self.timer_list[self.timer_list.index(row)])

    #  4.7 根据wechat检测是否在队列 (wechat_id)
    def isexist_wechat(self, wechat_id):
        if self.timer_list and [row for row in self.timer_list if row[0]==wechat_id]:
            return True
        return False

    #  4.8 获取sectime中的endtime (wechat_id)
    def get_endtime(self, wechat_id):
        if self.timer_list:
            return int([row[2][1] for row in self.timer_list if wechat_id == row[0]][0])
        return -1

    #  4.9 根据course_id检测是否在队列（course_id）
    def isexist_courseid(self, course_id):
        if self.timer_list and [row for row in self.timer_list if row[1]==course_id]:
            return True
        return False

    #  4.10 获取教师课程号
    def get_courseid(self, wechat_id):
        if self.timer_list:
            return [row[1] for row in self.timer_list if row[0]==wechat_id]

    #  4.11 TMER计算考勤结果（wechat_id, course_id）
    def calculate_Timer(self, wechat_id, course_id):
        if self.isexist_wechat(wechat_id):
            if not self.tool.is_resultEffective(course_id):
                args = (self.tool.get_teaid_inwechat(wechat_id)[0], course_id, self.tool.get_seqid(course_id))
                self.opt.delfile("detail", args)
                self.opt.delfile("randomdetail", args)
                return False
            else:
                self.tool.mergeResult(course_id)
                self.tool.update_sumfile(course_id)
if __name__ == "__main__":
    t = TimerQueue()
    t.calculate_Timer("wonka80", "51610189")

