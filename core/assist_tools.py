#! coding:utf-8
import time, configparser
from databaseoperation import opt

class AssistTools:
    def __init__(self):
        self.opt = opt.Opt()

    #  0.1.1 获取本次考勤次序号(course_id）
    def get_seqid(self, course_id):
        data = self.opt.readfile("seq")
        if data:
            return len([row[2] for row in data if row[1] == course_id])
        self.opt.newfile("seq")
        return -1

    #  0.1.2获取teacher_id(wechat_id)
    def get_teaid_inwechat(self, wechat_id):
        return [row[0] for row in self.opt.readfile("teacherInfo") if row[2] == wechat_id]#[0]

    # 检查wechat_id是否存在
    #  0.1.3获取teacher_id(course_id)
    def get_teaid_incourseid(self, course_id):
        return [row[2] for row in self.opt.readfile("courseInfo") if row[0] == course_id]#[0]

    #  0.1.4获取student_id(wechat_id)
    def get_stuid(self, wechat_id):
        return [row[0] for row in self.opt.readfile("studentInfo") if row[3] == wechat_id]#[0]

    #  0.1.5获取学生全部的课程号(wechat_id)
    def get_courseid_stu(self, wechat_id):
        return [row[0] for row in self.opt.readfile("courseInfo") if [row[2] for row in self.opt.readfile("studentInfo") if row[0] == self.get_stuid(wechat_id)[0]].count(row[3])>=1]

    #  0.1.6获取教师所有课程号(wechat_id)
    def get_courseid_tea(self, wechat_id):
        return list(set([row[0] for row in self.opt.readfile("courseInfo") if row[2] == self.get_teaid_inwechat(wechat_id)[0]]))

    #  0.1.7获取班级名列表（course_id）
    def get_classnamelist(self, course_id):
        return [row[3] for row in self.opt.readfile("courseInfo") if row[0] == course_id]#[0]

    #  0.1.8 获取timewindow(url)
    def get_timerwindow(self):
        config = configparser.ConfigParser()
        config.read(self.opt.url.get("setting"))
        return float(config.get('time', 'timewindow'))*60

    #  0.1.9 获取某课程的所有学生学号(course_id)
    def get_allstuID(self, course_id):
        return [row[0] for row in self.opt.readfile("studentInfo") if self.get_classnamelist(course_id).count(row[2]) >= 1]

    #  0.1.10获取当前时间()
    def get_localtime(self):
        return time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]

    #  0.2 初始化detail.csv(course_id)  seqid++
    def init_detailcsv(self, course_id):
        tea_id = self.get_teaid_incourseid(course_id)
        if tea_id:
            self.opt.newfile("detail", (tea_id[0], course_id, self.get_seqid(course_id)+1))
            return [row[0] for row in self.opt.readfile("studentInfo") if self.get_classnamelist(course_id).count(row[2])>=1]
        # 未完成
        # 未完成
        # 未完成
        # 未完成
        # 未完成

    #  0.3 初始化randomdetail.csv(course_id, random_list)
    def init_randomdetailcsv(self, course_id, random_list):
        tea_id = self.get_teaid_incourseid(course_id)
        if tea_id:
            self.opt.newfile("randomdetail", (tea_id[0], course_id, self.get_seqid(course_id)+1))

    #  0.4 空太多（course_id） 当前seqid
    def is_resultEffective(self, course_id):
        tea_id = self.get_teaid_incourseid(course_id)
        print(tea_id)
        if tea_id:
            data =  [row[-1] for row in self.opt.readfile("detail", (tea_id[0], course_id, self.get_seqid(course_id)))]
            if data.count(" ") >= len(data)*0.8 or data.count("缺勤") >= len(data)*0.8:
                return False
        return True

    #  0.6 计算考勤结果（course_id）
    def calculateResult(self, course_id): pass

    #  0.7 合并考勤结果(course_id)
    def mergeResult(self, course_id): pass

    #  0.8 生成random列表(nums)
    def generate_random(self, nums): pass

    #  0.9 格式化统计结果(course_id) ,打印出此课程对应每个人的考勤状况，每节课出勤率，平均出勤率
    def sumup_format(self, course_id):
        pass

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
                    if stu[0] == row[0] and len(stu[-1])<=4:
                        Smsg[j].append(stu[-1])
                        continue
                j+=1
        self.opt.writefile(Smsg, "sum", args)

if __name__ == "__main__":
    t = AssistTools()
    print(t.update_sumfile("51610189"))

