#! coding:utf-8
from databaseoperation import opt
from core import assist_tools
import re

class CheckTools:
    def __init__(self):
        self.opt = opt.Opt()
        self.tool = assist_tools.AssistTools()

    # 1.1课程号检验（wechat_id，course_id）
    def courseid_check(self, wechat_id, course_id):
        if self.wechat_tea_check(wechat_id):
            tea_id = self.tool.get_teaid_inwechat(wechat_id)
            return [1 for row in self.opt.readfile("courseInfo") if tea_id[0] == row[2] and course_id == row[0]]

    # 1.2抽点人数检验(num)
    def numsrandom_check(self, num, course_id):
        temp = self.tool.get_classnamelist(course_id)
        if re.findall('^([0-9]{1,3})$', str(num)):
            return len([1 for row in self.opt.readfile("studentInfo") if temp.count(row[2])]) >= int(num) and num != 0

    # 1.3考勤状态检验（type）
    def checkinresult_check(self, type):
        return ["出勤","缺勤","早退","迟到","请假"].count(type)

    # 1.4 seq是否吹界限
    def seq_check(self, seq_id, course_id):
        return self.tool.get_seqid(course_id) >= int(seq_id)

    # 1.5课程号学号检验（stu_id）
    def courseid_stu_check(self, student_id):
        return [1 for row in self.opt.readfile("studentInfo") if row[0] == student_id]

    # 1.6教师微信号检验(wechat_id)
    def wechat_tea_check(self, wechat_id):
        return [1 for row in self.opt.readfile("teacherInfo") if row[2]==wechat_id]

    # 1.7学生微信号检验(wechat_id)1
    def wechat_stu_check(self, wechat_id):
        return [1 for row in self.opt.readfile("studentInfo") if row[3] == wechat_id]

if __name__ == "__main__":
    t = CheckTools()
    # print(t.checkinresult_check("缺勤"))
    # print(t.numsrandom_check("002", "51610189"))
    # print(t.courseid_check("wonka80","51610189"))
    print(t.seq_check("2", "51610189"))