#! coding:utf-8

class CheckTools:
    def __init__(self):
        pass

    # 1.1课程号检验（wechat_id，course_id）
    def courseid_check(self, wechat_id, course_id): return True

    # 1.2抽点人数检验(num)
    def numsrandom_check(self, num): return True

    # 1.3考勤状态检验（type）
    def checkinresult_check(self, type): return True

    # 1.4考勤次序号检验（seq）  是否存在
    def isseqexist_check(self, seq_id): return True

    # 1.5课程号学号检验（stu_id）
    def courseid_stu_check(self, student_id): return True

    # 1.6教师微信号检验(wechat_id)
    def wechat_tea_check(self, wechat_id): return True

    # 1.7学生微信号检验(wechat_id)
    def wechat_stu_check(self, wechat_id): return True

    # 1.8学生是否可进行考勤(wechat_id)
    def stucheckin_check(self, wechat_id): return True
