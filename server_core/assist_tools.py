# coding:utf-8
import re
import csv
import time
import ConfigParser


class AssistTools:
    def __init__(self):
        pass

    def get_local_time(self):
        return time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]

    def get_over_time(self, start_time):
        cf = ConfigParser.ConfigParser()
        cf.read('../interior/settings.ini')
        info = map((lambda x: re.split('-|:', x[1])), cf.items('sectime'))
        Time_info = map((lambda x: [int(x[0]) * 3600 + int(x[1]) * 60, int(x[2]) * 3600 + int(x[3]) * 60]), info)
        first_time = Time_info[0]
        last_time = Time_info[len(Time_info)-1]
        for row in Time_info:
            if start_time > row[0] and start_time < row[1]:
                return row[1]
        if start_time < first_time[0] or start_time > last_time[0]:
            return first_time[1]
        return False

    def get_end_time(self):
        cf = ConfigParser.ConfigParser()
        cf.read('../interior/settings.ini')
        time_limit = int(cf.get('time', 'timewindow')) * 60
        local_time = time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
        return time_limit + local_time
##########################时间 ##############################

    def get_teacher_id(self, course_id):
        tem = [row[2] for row in csv.reader(open('../interior/courseInfo.csv'))]
        tem.pop(0)
        data = [[row[0], row[2]] for row in csv.reader(open('../interior/courseInfo.csv'))]
        data.pop(0)
        for row in list(set(tem)):  # set集合 优点不重复 以教工号为主
            for d in data:
                if row == d[1] and course_id == d[0]:
                    return d[1]

    def get_student_name(self, student_id):
        tem = [[row[0], row[1]] for row in csv.reader(open('../interior/studentinfo.csv'))]
        tem.pop(0)
        for row in tem:  # set集合 优点不重复 以教工号为主
            if student_id == row[0]:
                return row[1]
    # def get_all_teacher(self):
    #     tem = [row[2] for row in csv.reader(open('../interior/courseInfo.csv'))]
    #     tem.pop(0)
    #     teacher_list = []
    #     for row in list(set(tem)):
    #         teacher_list.append(row)
    #     return teacher_list
    def get_course_name(self, course_id):
        tem = [[row[0],row[1]]for row in csv.reader(open('../interior/courseInfo.csv'))]
        tem.pop(0)
        for row in tem:
            if course_id == row[0]:
                return row[1]

    def get_all_course(self):
        tem = [row[0] for row in csv.reader(open('../interior/courseInfo.csv'))]
        tem.pop(0)
        course_list = []
        for row in list(set(tem)):
            course_list.append(row)
        return course_list

    def get_true_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def get_seq_id(self, course_id):
        data = [row for row in csv.reader(open('../data/sum/%s_%s_sum.csv' % (self.get_teacher_id(course_id), course_id)))]
        if not data:
            return 1
        return len(data)

    def get_stu_wechat_list(self, course_id):
        course = []
        stu_wechat_list = []
        for row in [row for row in csv.DictReader(open('../interior/courseInfo.csv'))]:
            if row['TeacherID'] == self.get_teacher_id(course_id) and row['CourseID'] == course_id:
                course.append(row['ClassName'])
        for row in [row for row in csv.DictReader(open('../interior/studentinfo.csv'))]:
            if course.count(row['ClassID']) != 0:
                stu_wechat_list.append(row['WeChatID'])
        return stu_wechat_list

    def get_stu_list(self, course_id):
        course = []
        stu_list = []
        for row in [row for row in csv.DictReader(open('../interior/courseInfo.csv'))]:
            if row['TeacherID'] == self.get_teacher_id(course_id) and row['CourseID'] == course_id:
                course.append(row['ClassName'])
        for row in [row for row in csv.DictReader(open('../interior/studentinfo.csv'))]:
            if course.count(row['ClassID']) != 0:
                stu_list.append(row['StuID'])
        return stu_list
        
    def get_own_course(self, teacher_id):
        data = [[row[0], row[2]] for row in csv.reader(open('../interior/courseInfo.csv'))]
        data.pop(0)
        course_list = []
        for row in data:
            if not course_list:
                if teacher_id == row[1]:
                    course_list.append(row[0])
            else:
                if teacher_id == row[1] and course_list.count(row[0]) == 0:
                    course_list.append(row[0])
        return course_list

    def get_stu_course(self, student_id):
        tem = []
        course = []
        for row in [row for row in csv.DictReader(open('../interior/studentinfo.csv'))]:
            if row['StuID'] == str(student_id):
                tem.append(row['ClassID'])
        for row in [row for row in csv.DictReader(open('../interior/courseInfo.csv'))]:
            for d in tem:
                if row['ClassName'] == d:
                    course.append(row['CourseID'])
        return course

if __name__ == '__main__':
    t = AssistTools()
    print t.get_stu_list('51610166')


