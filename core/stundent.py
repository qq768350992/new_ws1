#! coding:utf-8
from core import timer_queue, assist_tools
import random

class Student:
    def __init__(self):
        self.time = timer_queue.TimerQueue()
        self.tool = assist_tools.AssistTools()
        self.within = {"出勤":"出勤", "缺勤":"迟到", "迟到":"迟到", "早退":"迟到", "null":"出勤"}
        self.without = {"出勤": "迟到", "缺勤": "缺勤", "迟到": "早退", "早退": "早退", "null": "迟到"}
    def get_limitValueTime(self):
        return 60

    def feature_submit(self):
        if random.randrange(2) != 0:
            print("认证成功")
            return "D://"
        else:
            print("认证失败，请重新提交")

    def Result_calculate(self, keys, type, args):
        if type == "detail":
            if self.time.is_valueTime_Detail(keys[1], self.get_limitValueTime()):
                return "出勤"
            else:
                return "迟到"
        else:
            C_R = self.tool.getCheckinResult("detail", args, keys[0])[0]
            if self.time.is_valueTime_Ramdom(keys[1], self.get_limitValueTime()):
                return self.within.get(C_R)
            else:
                return self.without.get(C_R)

    # 根据时间窗口判断是否可考勤
    # 确认提交特征信息
    # if input("请提交您的特征信息（输入0退出）: ") == "0": return False
    # 是否lea.csv   detail.csv random.csv有自己的数据（考勤状态不为空或不存在）
    # 若random.csv无自己
    # 若提交成功，则判断是否是在有效时间范围内，若是：出勤  否则：迟到   若提交失败，则Isscuss为False其余不变。
    # 若random.csv有自己
    # 若提交成功，先从detail中提取detailCheckinResult， 根据detailCheckinResult 则判断是否是在有效时间范围内
    # 将考勤结果写入detail.csv 或着 random.csv , random.csv优先（若其中有自己）
    def attendCheckin(self, wechat_id):
        Sid = self.tool.get_stuid(wechat_id)
        Cid = [row for row in self.tool.get_courseid_stu(wechat_id) if self.time.isexist_courseid(row)]
        if Cid:
            SeqID = self.tool.get_seqid(Cid[0])
            args = [self.tool.get_teaid_incourseid(Cid[0])[0], Cid[0], SeqID]
            keys = [Sid[0], Cid[0], SeqID]
            if self.tool.getCheckinResult("lea", None, keys):
                print("无法继续，您已请假")
                return False
            if not self.attend(args[0:-1], keys, "randomdetail"):
                self.attend(args, keys, "random")

    def attend(self, args, keys, type):
        _RamR = self.tool.getCheckinResult(type, args, keys[0])
        if _RamR:
            if _RamR[0] == "null":
                ProofPath = self.feature_submit()
                if not ProofPath:
                    self.tool.alterItem(type, args, keys[0], ["False", 4])
                else:
                    checkin_result = self.Result_calculate(keys[0], type, args)
                    print("参与抽点考勤成功: " + checkin_result)
                    row = [keys[0], self.tool.format_time(), ProofPath, "auto", "True", checkin_result]
                    self.tool.alterCheckinLine(keys, row, type, args)
            else:
                if type == "randomdetail":
                    print("无法继续，您已参与过抽点考勤")
                else:
                    print("无法继续，您已参与过自助考勤")
            return True

    def lea(self, wechat_id):
        ProofPath = self.feature_submit()
        if ProofPath:
            Cid = [row for row in self.tool.get_courseid_stu(wechat_id) if self.time.isexist_courseid(row)]
            if Cid:
                self.tool.update_lea([self.tool.get_stuid(wechat_id)[0], Cid[0], self.tool.get_seqid(Cid[0]), self.tool.format_time(), ProofPath])

    def show_now(self):
        # 根据时间窗口判断是否可考勤
        # 从优先级为lea.csv > random.csv > detail.csv
        pass

    def show_recent(self, course_id):
        # 根据seq.csv中获取此课程的考了几次
        # 依次遍历，从优先级为lea.csv > random.csv > detail.csv
        pass

if __name__ == "__main__":
    t = Student()
    #t.attendCheckin("wfsf_105")
    # t.lea()
    #print(t.update_seq("51610055"))
