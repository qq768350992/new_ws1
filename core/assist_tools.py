#! coding:utf-8
import time, configparser, re
from databaseoperation import opt
import random

class AssistTools:
    def __init__(self):
        self.opt = opt.Opt()

    #  0.1.1 获取本次考勤次序号(course_id）
    def get_seqid(self, course_id):
        data = self.opt.readfile("seq")
        if data:
            return len([row[2] for row in data if row[1] == course_id])
        self.opt.newfile("seq")
        return 0

    #  0.1.2获取teacher_id(wechat_id)
    def get_teaid_inwechat(self, wechat_id):
        return [row[0] for row in self.opt.readfile("teacherInfo") if row[2] == wechat_id]

    #  0.1.3获取teacher_id(course_id)
    def get_teaid_incourseid(self, course_id):
        return [row[2] for row in self.opt.readfile("courseInfo") if row[0] == course_id]

    #  0.1.4获取student_id(wechat_id)
    def get_stuid(self, wechat_id):
        return [row[0] for row in self.opt.readfile("studentInfo") if row[3] == wechat_id]

    # #  0.1.5获取学生全部的课程号(wechat_id)
    # def get_courseid_stu(self, wechat_id):
    #     return [row[0] for row in self.opt.readfile("courseInfo") if [row[2] for row in self.opt.readfile("studentInfo") if row[0] == self.get_stuid(wechat_id)[0]].count(row[3])>=1]

    #  0.1.6获取教师所有课程号(wechat_id)
    def get_courseid_tea(self, wechat_id):
        return list(set([row[0] for row in self.opt.readfile("courseInfo") if row[2] == self.get_teaid_inwechat(wechat_id)[0]]))

    #  0.1.7获取班级名列表（course_id）
    def get_classnamelist(self, course_id):
        return [row[3] for row in self.opt.readfile("courseInfo") if row[0] == course_id]

    #  0.1.9 获取某课程的所有学生学号(course_id)
    def get_allstuID(self, course_id):
        return [row[0] for row in self.opt.readfile("studentInfo") if self.get_classnamelist(course_id).count(row[2]) >= 1]

    #  0.1.10获取当前时间()
    def get_localtime(self):
        return time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]

    #  0.1.8 获取timewindow(url)
    def get_timerwindow(self):
        config = configparser.ConfigParser()
        config.read(self.opt.url.get("setting"))
        return float(config.get('time', 'timewindow'))*60

    #  0.2 初始化detail.csv(course_id)  seqid++
    def init_detailcsv(self, course_id, detail=None):
        # Type = ["auto", "出勤"]
        tea_id = self.get_teaid_incourseid(course_id)
        if tea_id:
            args = (tea_id[0], course_id, self.get_seqid(course_id))
            self.opt.newfile("detail", args)
            Dmsg = self.opt.readfile("detail", args)
            if len(Dmsg) < 2:
                for row in self.get_allstuID(course_id):
                    Dmsg.append([row, " ", " ", detail[0], " ", detail[1]])
            self.opt.writefile(Dmsg, "detail", args)

    #  0.3 初始化randomdetail.csv(course_id, random_list)
    def init_randomdetailcsv(self, course_id, random_list):
        tea_id = self.get_teaid_incourseid(course_id)
        if tea_id and random_list:
            args = (tea_id[0], course_id, self.get_seqid(course_id))
            self.opt.newfile("randomdetail", args)
            header = [self.opt.header.get("randomdetail")]
            for row in random_list:
                header.append([row, " ", " ", "auto", " ", " "])
            self.opt.writefile(header, "randomdetail", args)

    #  0.4 考勤是否有效（course_id） 当前seqid
    def is_resultEffective(self, course_id):
        tea_id = self.get_teaid_incourseid(course_id)
        if tea_id:
            data =  [row[-1] for row in self.opt.readfile("detail", (tea_id[0], course_id, self.get_seqid(course_id)))]
            if data.count(" ") >= len(data)*0.8 or data.count("缺勤") >= len(data)*0.8:
                return False
        return True

    #  0.6 计算考勤结果（course_id）
    def calculateResult(self, course_id):
        tea_id = self.get_teaid_incourseid(course_id)
        seq_id = self.get_seqid(course_id)
        self.opt.newfile("lea")
        LMsg = self.opt.readfile("lea")
        from core import timer_queue
        if tea_id and seq_id>0 and not timer_queue.TimerQueue().isexist_courseid(course_id) and len(LMsg)>1:
            for row in LMsg:
                if self.get_allstuID(course_id).count(row[0])>0 and row[1]==course_id:
                    args = (tea_id[0], course_id, self.get_seqid(course_id))
                    op = input("是否给予"+row[0]+"批假 (1:是 2:忽略 3:查看假条与请假时间信息 0:退出)")
                    if op == "1":
                        self.opt.delline("lea", None, (0, row[0]))
                        self.opt.alteritem("detail", args, (0, row[0], -1, "请假"))
                    elif op == "2":
                        self.opt.alteritem("sum", args[0:-1], (0, row[0], args[-1], " "))
                    elif op == "3":
                        print("seq: "+row[2]+"\ntime: "+row[3]+"\nProof: "+row[4])
                        continue
                    break
        for seq in range(1, seq_id+1):
            for row in self.opt.readfile("detail", (tea_id[0], course_id, seq)):
                if not row[-1]:
                    self.opt.alteritem("sum", (tea_id[0], course_id), (0, row[0], seq, row[-1]))

    #  0.7 合并考勤结果(course_id)
    #  问题 ： 是直接合并，以random为依据    还是根据有效时间划分，配合random的数据为依据
    #  分析： 前者， 因为后者学生考勤时已经完成了相应计算与判定
    def mergeResult(self, course_id):
        tea_id = self.get_teaid_incourseid(course_id)
        if tea_id:
            args = (tea_id[0], course_id, self.get_seqid(course_id))
            Rmsg = self.opt.readfile("randomdetail", args[0:-1])
            print(Rmsg)
            if len(Rmsg)>1:
                for row in self.opt.readfile("detail", args):
                    for msg in Rmsg:
                        if row[0] == msg[0] and len(row[-1])<5:
                            self.opt.alteritem("detail", args, (0, msg[0], -1, msg[-1]))
                            print("抽点数据合并成功")

    #  0.8 生成random列表(nums)
    def generate_random(self, course_id, nums):
        return random.sample(list(set(self.get_allstuID(course_id))-set([row[0] for row in self.opt.readfile("lea") if row[1] == course_id and row[2] == self.get_seqid(course_id)])), int(nums))

    #  0.9 格式化统计结果(course_id) ,打印出此课程对应每个人的考勤状况，每节课出勤率，平均出勤率
    def sumup_format(self, course_id): pass

    #  0.10 更新sum.csv
    def update_sumfile(self, course_id):
        args = (self.get_teaid_incourseid(course_id)[0], course_id)
        self.opt.newfile("sum", args)
        Smsg = self.opt.readfile("sum", args)
        Dmsg = self.opt.readfile("detail", (self.get_teaid_incourseid(course_id)[0], course_id, self.get_seqid(course_id)))
        if Smsg and len(Smsg) <= 5:
            Smsg[0].append('checkin%d' % (self.get_seqid(course_id)))
            for row in self.get_allstuID(course_id):
                Smsg.append([row])
            j=0
            for row in Smsg:
                for stu in Dmsg:
                    if stu[0] == row[0] and len(stu[-1])<2:
                        Smsg[j].append(stu[-1])
                        continue
                j+=1
        self.opt.writefile(Smsg, "sum", args)

    # 0.11 更新seq.csv
    def updata_seq(self, course_id):
        self.opt.writefile([[self.get_teaid_incourseid(course_id)[0], course_id, self.get_seqid(course_id) + 1, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]] ,"seq", None, "a")


if __name__ == "__main__":
    t = AssistTools()
    #print(t.updata_seq("51610055"))


