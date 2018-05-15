#! coding:utf-8
import re, configparser, threading, operator
from functools import reduce
from core import assist_tools
from databaseoperation import opt

class TimerQueue:
    def __init__(self):
        self.opt = opt.Opt()
        self.tool = assist_tools.AssistTools()
        self.timer_list = [   ["Tp_rt55", "51610041", [52200, 57900], ["软件工程1601","软件工程1602"], "32000","-1"],
                              ["wonka80", "51610189", [52200, 57900], ["软件工程1603","软件工程1604"],"32001","88888"]
                        ]
    def init_tcb(self, wechat_id, course_id):
        return [wechat_id, course_id, self.get_sectime(self.tool.get_localtime()), self.tool.get_classnamelist(course_id), self.tool.get_localtime(), "-1"]

    #  4.1 获取sectime(url) 上课区间包括开始和结束
    def get_sectime(self,start_time):
        cf = configparser.ConfigParser()
        cf.read(self.opt.url.get("setting"))
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
                    print("被"+ row[0] +"占用，无法开启")
                    return False
                else:
                    self.depart_queque(row[0], row[1], 1) # 1代表直接抢占  其他情况是Timer做的
                    self.tool.mergeResult(row[1])
                    self.opt.init_clear("randomdetail",(self.tool.get_teaid_inwechat(row[0])[0], row[1]))
                    print("已将"+row[0]+"踢出")
                    return True
        return True

    #  4.5 进队（wechat_id, course_id）
    def enter_qeque(self, wechat_id, course_id):
        if self.enter_check(course_id):
            self.timer_list.append(self.init_tcb(wechat_id, course_id))
            t = threading.Timer(self.tool.get_timerwindow()+5, self.depart_queque, (wechat_id, course_id)).start()

    #  4.6 出队（wechat_id, timer_list）
    def depart_queque(self, wechat_id, course_id, args=None): # 默认Timer方式出队
        # bug 当正常出队时，出不去
        # 如果现在时间的 - 被出队的TCB的开启时间 >= 时间窗口的时间
        if args==1 or (int(self.tool.get_localtime()) - int([row[4] for row in self.timer_list][0])) > int(self.tool.get_timerwindow())\
           or self.timer_list and not set(reduce(operator.add, [row[3] for row in self.timer_list])) & set(self.tool.get_classnamelist(course_id)):
            for row in self.timer_list:
                if wechat_id == row[0]:
                    del (self.timer_list[self.timer_list.index(row)])
                    self.tool.mergeResult(row[1])
                    self.opt.init_clear("randomdetail",(self.tool.get_teaid_inwechat(row[0])[0],row[1]))
                    print(wechat_id+" : "+course_id+"被您抢占")

    #  4.7 根据wechat检测是否在队列 (wechat_id)
    def isexist_wechat(self, wechat_id):
        if self.timer_list and [row for row in self.timer_list if row[0]==wechat_id]:
            return True
        return False

    #  4.8 获取sectime中的endtime (wechat_id)
    def get_endtime(self, wechat_id):
        if self.timer_list:
            return int([row[2][1] for row in self.timer_list if wechat_id == row[0]][0])
        return 0

    #  4.9 根据course_id检测是否在队列（course_id）
    def isexist_courseid(self, course_id):
        if self.timer_list:
            return [row for row in self.timer_list if row[1]==course_id]

    #  4.10 获取教师课程号
    def get_courseid(self, wechat_id):
        if self.timer_list:
            return [row[1] for row in self.timer_list if row[0]==wechat_id]

    #  4.11 TMER计算考勤结果（wechat_id, course_id）
    # def calculate_Timer(self, wechat_id, course_id):
    #     if self.isexist_wechat(wechat_id):
    #         if not self.tool.is_resultEffective(course_id):
    #             self.opt.delfile("detail", (self.tool.get_teaid_inwechat(wechat_id)[0], course_id, self.tool.get_seqid(course_id)))
    #             return False
    #         else:
    #             self.tool.mergeResult(course_id)
    #             self.tool.update_sumfile(course_id)

    # 4.12 is_valueTime（ ）
    def is_valueTime_Detail(self, course_id, timelimit):
        return int(self.tool.get_localtime()) - int([row[4] for row in self.timer_list if row[1] == course_id][0]) < int(timelimit)

    # 4.13
    def is_valueTime_Ramdom(self, course_id, timelimit):
        return int(self.tool.get_localtime()) - int([row[5] for row in self.timer_list if row[1] == course_id][0]) < int(timelimit)

    # 4.14 初始化ramdomtimer
    def initRamdomTimer(self, course_id):
        for row in self.timer_list:
            if row[1] == course_id:
                self.timer_list[self.timer_list.index(row)] = [row[0:-1], self.tool.get_localtime()]

if __name__ == "__main__":
    t = TimerQueue()
    #t.enter_qeque("wonka80", '51610189')
    #t.depart_queque("wonka80", '51610189')
    #print(t.is_valueTime_Detail('51610189', 50))
    #t.calculate_Timer("wonka80", "51610189")

