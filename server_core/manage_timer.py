# coding:utf-8
import os
import csv
import threading
import assist_tools
import ConfigParser


class ManageTimer:
    def __init__(self):
        self.tool = assist_tools.AssistTools()

    def has_tea_wechat(self, tem_list, list):
        for row in list:
            if row[4] == tem_list[4]:
                if row[2] <= row[3]:
                    return True
                elif self.tool.get_local_time() > row[3]:
                    return row[0]
        return False

    def has_course(self, tem_list, list):
        for row in list:
            if tem_list[0] == row[0]:
                if row[2] <= row[3]:
                    return True
                elif self.tool.get_local_time() > row[3]:
                    return row[0]
        return False

    def has_stu_wechat(self, tem_list, list):
        stu_data = self.tool.get_stu_wechat_list(tem_list[0])
        for row in list:
            stu_tem = self.tool.get_stu_wechat_list(row[0])
            for d in stu_data:
                if stu_tem.count(d) != 0:
                    if row[2] <= row[3]:
                        return True
                    elif self.tool.get_local_time() > row[3]:
                        return row[0]
        return False

    def can_add(self, tem_list, list):
        if list:
            if type(self.has_course(tem_list, list)) != bool:
                return self.has_course(tem_list, list)
            if type(self.has_tea_wechat(tem_list, list)) != bool:
                return self.has_tea_wechat(tem_list, list)
            if type(self.has_stu_wechat(tem_list, list)) != bool:
                return self.has_stu_wechat(tem_list, list)
            if self.has_tea_wechat(tem_list, list) == True:
                if self.has_course(tem_list, list) == True:
                    print '此课程的时间窗口已被你开启过,且仍在运行'
                    return False
                else:
                    print '你有其它课程的时间窗口仍在运行'
                    return False
            else:
                if self.has_course(tem_list, list) != False:
                    print '此课程的时间窗口被其它老师占用'
                    return False
                elif self.has_stu_wechat(tem_list, list) != False:
                    print '此课程的部分学生在上课'
                    return False
                else:
                    return True
        else:
            return True

    def list_add(self, tem_list, list):
        s = self.can_add(tem_list, list)
        if s == True:
            list.append(tem_list)
            return list
        elif s == False:
            return False
        else:
            tem = []
            for row in list:
                tem.append(row)
                if row[0] == s or row[4] == tem_list[4]:
                    tem.pop()
                    tem.append(tem_list)
                    self.write_sum(row[4], row[0])
            return tem

    def set_r(self, r, list, teacher_id, random_list):
        tem = []
        for row in list:
            tem.append(row)
            if row[4] == teacher_id:
                tem.pop(); d = row; d[1] = r
                if random_list != []:
                    d[5] = random_list
                tem.append(d)
        return tem

    def has_r(self, list, teacher_id):
        if not list:
            return 0
        for row in list:
            if teacher_id == row[4]:
                return row[0] # 有
        return 0 # 没有

    def leave_list(self, list, teacher_id):
        tem = []
        for row in list:
            tem.append(row)
            if teacher_id == row[4]:
                tem.pop()
                self.write_sum(row[4], row[0])
                print '%s的时间窗口已结束' % row[0]
        return tem

    def write_sum(self, teacher_id, course_id):
        sum_data = [row for row in csv.reader(open('../data/sum/%s_%s_sum.csv' % (teacher_id, course_id)))]
        if not sum_data:
            sum_data = [stu_id for stu_id in self.tool.get_stu_list(course_id)]
            sum_data.insert(0, ['StuID'])
        seq_id = self.tool.get_seq_id(course_id)
        with open('../data/%s_%s_%s_checkinDetail.csv' % (teacher_id, course_id, seq_id)) as csvfile:
            reader = csv.DictReader(csvfile)
            sumdata = [[stu['StuID'], stu['checkinResult']] for stu in reader]
            sum_data[0].append('checkin%d' % seq_id)
        j = 0
        for id in sum_data:
            for stu in sumdata:
                if stu[0] == id[0]:
                    sum_data[j].append(stu[1])
                    continue
            j += 1
        csv.writer(open('../data/sum/%s_%s_sum.csv' % (tem_list[4], tem_list[0]), 'wb')).writerows(sum_data)

    def stu_start_checkin(self, student_id, list, detail_data):
        s = self.is_timer_exist(student_id, list)  # 直接给值, 开始之前已经检测
        for row in [row for row in csv.reader(open('../data/%s_%s_%s_checkinDetail.csv' % (s[2], s[0], self.tool.get_seq_id(s[0]))))]:
            if student_id == row[0]:
                new_status = self.stu_status(s, row[5], detail_data[3])
                if new_status == 0:
                    return 0
                detail_data[4] = new_status
        self.alter_detail([s[2], s[0], self.tool.get_seq_id(s[0]), student_id], detail_data)
        # detail_data = [ time, proofpath, checkintype, issucc, checkinresult ]

    def get_current_atd(self, student_id, list):
        s = self.is_timer_exist(student_id, list)  # 直接给值, 开始之前已经检测
        for row in [row for row in csv.reader(open('../data/%s_%s_%s_checkinDetail.csv' % (s[2], s[0], self.tool.get_seq_id(s[0]))))]:
            if student_id == row[0]:
                if row[1] == ' ' or row[2] == ' ':
                    print '状态：未进行考勤或请假'
                elif row[5] == '缺勤' and row[2] == ' ':
                    print '状态：考勤认证失败'
                elif row[5] == '请假' and row[4] == ' ':
                    print '状态：请假待审批'
                else:
                    print '状态：%s' % row[5]

    def get_history_atd(self, student_id):
        for row in self.tool.get_stu_course(student_id):
                course_id = row[0]
                print '%s :' % self.tool.get_course_name(course_id)
                data = [row for row in csv.reader(open('../data/sum/%s_%s_sum.csv' % (self.tool.get_teacher_id(course_id), course_id)))]
                if not data:
                    print '空'
                    continue
                for row in data:
                    if row[0] == student_id:
                        row.pop(0)
                        i = 1
                        for line in row:
                            if line == ' ':
                                print "%s : 假条还未审批"
                            else:
                                print "%s：%s" % (i, line)
                            i += 1

    def stu_status(self, s, status, is_success):
        r = s[1]
        if status == '缺勤' or status == ' ':
            if is_success == True:
                if r == 1:
                    return '出勤'
                else:
                    return '迟到'
            else:
                return '缺勤'
        elif status == '出勤':
            if is_success == True:
                return '出勤'
            else:
                return '早退'
        elif status == '早退' or status == '迟到':
            if is_success == True:
                return '迟到'
            else:
                return '早退'
        else:
            print '你申请了请假,无法签到'
            return 0

    def is_alter(self, student_id, id, list): # 假设student_id 已经存在list中
        for row in list:
            if self.tool.get_stu_course(student_id).count(row[0]):
                course_id = row[0]
                for row in [row for row in csv.reader(open('../data/%s_%s_%s_checkinDetail.csv' % (self.tool.get_teacher_id(course_id), course_id, self.tool.get_seq_id(course_id))))]:
                    if row[0] == student_id:
                        if row[5] == '请假':
                            a = 2
                        else:
                            a = 1
                        if a != id:
                            if a == 2:
                                choose = raw_input('你已请过假,是否继续考勤: y/n')
                            else:
                                choose = raw_input('你已考过勤,是否继续请假: y/n')
                            if choose != 'y':
                                return 0
                return 1

    def is_timer_exist(self, student_id, list):
        s = 0
        for row in list:
            if self.tool.get_stu_course(student_id).count(row[0]):
                if row[1] == 0:
                    s = 0
                elif row[1] == 3 and row[5].count(student_id) == 0:
                    s = [row[0], 2, row[4]]
                elif row[1] == 3 and row[5].count(student_id) != 0:
                    s = [row[0], 3, row[4]]
                else:
                    s = [row[0], row[1], row[4]]
        if s == 0:
            print '考勤还未开始'
            return 0
        return s

        # sum_data = [row for row in csv.reader(open('../data/sum/%s_%s_sum.csv' % (data[0], data[1])))]
        # for row in sum_data:
        #     if student_id == row[0]:
        #         sum_status = row[int(self.tool.get_seq_id(s[0]))]
    ################################################################################3

    def course_check(self, teacher_id, course_id):
        own_course = self.tool.get_own_course(teacher_id)
        all_course = self.tool.get_all_course()
        if own_course.count(course_id) != 0:
            return 1
        elif all_course.count(course_id) == 0:
            print '课程号不存在'
            return 0
        else:
            print '此课程号不属于你'
            return 0

    def get_lea_list(self, teacher_id, p = 1):
        data = []
        for parent,dirnames,filenames in os.walk('../data/sum'):
            j = 0
            for filename in filenames:
                if filename[:7] == teacher_id:
                    flag = j
                    if p == 1:
                        print '%s:'%self.tool.get_course_name(filename[8:16])
                    path = os.path.join(parent,filename)
                    tem = [row for row in csv.reader(open(path))]
                    if not tem:
                        if p == 1:
                            print '空'
                        continue
                    tem.pop(0)
                    for row in tem:
                        i = 0
                        for d in row:
                            i += 1
                            if d == ' ':
                                j += 1
                                if p == 1:
                                    print '  %s  %s %s:在第%s节课向你请假' % (j, self.tool.get_student_name(row[0]),row[0], i-1)
                                data.append([teacher_id, filename[8:16], i-1, row[0]])
                    if flag == j and p == 1:
                        print '空'
        return data

    def exe_lea(self, teacher_id):
        while 1:
            tem = self.get_lea_list(teacher_id)
            if not tem:
                print '没有可审批的了'
                return 0
            num = raw_input('输入序号进行审批，输入其它退出:')
            if num <= '0':
                return 0
            try:
                lea_data = tem[int(num)-1]
            except:
                return 0
            choose = raw_input('是否批准请假y/n，0退出')
            if choose == 'y':
                detail_data = [None, None, 'man', 'True', '请假' ]
                # detail_data = [ time, proofpath, checkintype, issucc, checkinresult ]
                self.alter_detail(lea_data, detail_data)
                self.alter_sum(lea_data, '请假')
            elif choose == 'n':
                self.alter_sum(lea_data, self.get_detail_status(lea_data))
            else:
                continue

    def seq_id_check(self, seq_id, course_id):
        seq_max = self.tool.get_seq_id(course_id)
        tem = []
        i = 1
        for row in range(1, seq_max + 1):
            tem.append(i)
            i += 1
        try:
            if tem.count(int(seq_id)) == 0:
                print '考勤次序号不存在'
                return 0
        except:
            print '考勤次序号不存在'
            return 0
        return 1

    def get_detail_status(self, data):
        detail_data = [row for row in csv.reader(open('../data/%s_%s_%s_checkinDetail.csv' % (data[0], data[1], data[2])))]
        if not detail_data:
            return 0
        for row in detail_data:
            if row[0] == data[3]:
                return row[5]

    def random_change_detail(self, teacher_id, list, random_list):
        course_id = None
        for row in list:
            if teacher_id == row[4]:
                course_id = row[0]
        data = [row for row in csv.reader(open('../data/%s_%s_%s_checkinDetail.csv' % (teacher_id, course_id, self.tool.get_seq_id(course_id))))]
        random_stu = {}
        for row in data:
            if random_list.count(row[0]) != 0:
                random_stu[row[0]] = row[5]
        tem = []
        for row in data:
            if random_list.count(row[0]):
                old = random_stu[row[0]]
                if old == '出勤' or old == '早退' or old == '迟到':
                    row[5] = '早退'
            tem.append(row)
        csv.writer(open('../data/%s_%s_%s_checkinDetail.csv' % (teacher_id, course_id, self.tool.get_seq_id(course_id)), 'wb')).writerows(tem)

    def alter_detail(self, data, detail_data):
        # data =   [ teacher_id, course_id, seq_id, student_id]
        # detail_data = [ time, proofpath, checkintype, issucc, checkinresult ]
        tem = [row for row in csv.reader(open('../data/%s_%s_%s_checkinDetail.csv' % (data[0], data[1], data[2])))]
        if not tem:
            return 0
        tem_detail = []
        for row in tem:
            tem_detail.append(row)
            if row[0] == data[3]:
                tem_detail.pop()
                d = row
                if detail_data[0] != None:d[1] = detail_data[0]
                if detail_data[1] != None:d[2] = detail_data[1]
                if detail_data[2] != None:d[3] = detail_data[2]
                if detail_data[3] != None:d[4] = detail_data[3]
                if detail_data[4] != None:d[5] = detail_data[4]
                tem_detail.append(d)
        csv.writer(open('../data/%s_%s_%s_checkinDetail.csv' % (data[0], data[1], data[2]), 'wb')).writerows(tem_detail)

    def alter_sum(self, data, check_status):
        sum_data = [row for row in csv.reader(open('../data/sum/%s_%s_sum.csv' % (data[0], data[1])))]
        if not sum_data:
            return 0
        tem_sum = []
        for row in sum_data:
            tem_sum.append(row)
            if row[0] == data[3]:
                tem_sum.pop()
                d = row; d[int(data[2])] = check_status
                tem_sum.append(d)
        csv.writer(open('../data/sum/%s_%s_sum.csv' % (data[0], data[1]), 'wb')).writerows(tem_sum)

    def start_init(self, tem_list, list):
        detail_data = []
        normal_time = 20 # 默认20分钟
        config = ConfigParser.ConfigParser()
        config.read('../interior/settings.ini')
        time_limit = int(config.get('time', 'timewindow'))  # 自主考勤最大持续时间
        seq_id = self.tool.get_seq_id(tem_list[0])
        print '%s的第%s次考勤' % (self.tool.get_course_name(tem_list[0]), seq_id)
        for row in [row for row in csv.reader(open('../interior/time.csv'))]:
            if tem_list[4] == row[0]:
                normal_time = row[1]
        detail_data.append(['StuID', 'checkinTime', 'ProofPath', 'checkinType', 'IsSucc', 'checkinResult'])
        for stu_id in self.tool.get_stu_list(tem_list[0]):
            detail_data.append([stu_id, ' ', ' ', ' ', ' ', '缺勤'])
        csv.writer(open('../data/%s_%s_%s_checkinDetail.csv' % (tem_list[4], tem_list[0], seq_id), 'wb')).writerows(detail_data)
        _t = threading.Timer(float(normal_time) * 60.0, self.set_r(2, list, tem_list[4], []))
        _t.start()
        t = threading.Timer((time_limit - float(normal_time)) * 60.0, self.leave_list(list, tem_list[4]))  # 定时器
        t.start()

    def write_seq(self, teacher_id, course_id):
        seq_data = [row for row in csv.reader(open('../data/seq.csv'))]
        if seq_data == []:
            seq_data.append(['TeacherID', 'self.CourseID', 'SeqID', 'StartTime'])
        seq_data.append([teacher_id, course_id, self.tool.get_seq_id(course_id), self.tool.get_true_time()])
        csv.writer(open('../data/seq.csv', 'wb')).writerows(seq_data)

    def init_data(self, course_id):
        tem = []
        tem.append(['StuID', 'checkinTime', 'ProofPath', 'checkinType', 'IsSucc', 'checkinResult'])
        stu_list = self.tool.get_stu_list(course_id)
        if stu_list:
            stu_list.pop()
        print '考勤状态序号：1:出勤 2:缺勤 3:请假 4:迟到 5:早退'
        for row in stu_list:
            choose = raw_input('学号' + row + '为其输入考勤状态序号')
            d = [row, ' ', ' ', ' ', type, 'False']
            status = {'1': '出勤', '2': '缺勤', '3': '请假', '4': '迟到', '5': '早退'}
            if choose in list('12345'):
                d[4] = status[choose]
            else:
                print '输入非法选项默认此学生是缺勤!'
                d[4] = status['2']
            d[3] = 'man'
            print '%s的考勤状态设定完毕-->%s' % (self.tool.get_student_name(row), d[4])
            tem.append(d)
        csv.writer(open('../data/%s_%s_%s_checkinDetail.csv' % (self.tool.get_teacher_id(course_id), course_id, self.tool.get_seq_id(course_id)), 'wb')).writerows(tem)

    def can_random(self, list, teacher_id):
        for row in list:
            if teacher_id == row[4]:
                if self.tool.get_local_time()+5*60 <= row[2]:
                    return True
        return 0

    def get_recent_atd(self, list, teacher_id):  # for tea
        a = [row for row in csv.reader(open('../data/seq.csv'))]
        a.reverse()
        for row in a:
            if teacher_id == row[0]:
                i = 0
                for line in [row for row in csv.reader(open('../data/%s_%s_%s_checkinDetail.csv' % (row[0], row[1], row[2])))]:
                    if line[5] == '缺勤':
                        print line[0],self.tool.get_student_name(line[0]),line[5]
                    if line[5] == '请假':
                        i += 1

                break

if __name__ == '__main__':
    t = ManageTimer()
    t.get_recent_atd([], '2004355')
