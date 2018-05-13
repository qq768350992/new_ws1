#! coding:utf-8
import csv
from core import format_check
'''
' import_data: 1.导入 2.去重(分布，联合) 3.拆分班级区间 
' format_check主要检查列的个数和列名以及数据的完整性：
'			  1.格式化检验 2.错误日志 3.第一行是否丢失 
'                                              '''

class ImportData:
    def __init__(self):
        pass

    def import_file(self, url):
        error_msg = [["File:'" + url[0] + "'"]]
        try:
            data = [row for row in csv.reader(open(url[0], encoding='utf-8'))]
            if not format_check.file_header(data[0], error_msg):
                print(url[0] + ": 格式出现致命错误，缺少关键的头信息"); return
            header = data.pop(0)
            if url[1] == "teacherInfo.csv":
                format_check.tea_check(data, error_msg)         # 格式化检验
                temp = self.dis_del_repeat(data, 0)  # TeacherID去重
                aim = self.dis_del_repeat(temp, 2)       # WeChatID去重
                aim.insert(0, header)
            elif url[1] == "courseProgress.csv":
                format_check.course_check(data, error_msg)          # 格式化检验
                temp = self.col_del_repeat(data)        # CourseID&ClassNums去重
                aim = self.opt_class_nums(temp)         # 拆分班级区间 ClassName
                aim.insert(0, ["CourseID", "CourseName", "TeacherID", "ClassName"])
                url[1] = "courseInfo.csv"
            else:
                format_check.stu_check(data[1:] , error_msg)        # 格式化检验
                temp = self.dis_del_repeat(data, 0)     # StuID去重
                aim = self.dis_del_repeat(temp, 3)      # WeChatID去重
                aim.insert(0, header)
        except IOError:
            print(url + " 文件打开失败或不存在"); return
        csv.writer(open("../interior/" + url[1], 'w+', newline='')).writerows(aim)
        if len(error_msg) > 1:
            print(url[1] + ": 写入成功, found "+ str(len(error_msg)-1) + " format error, "+"please to check the log file ")
            csv.writer(open('../log/log.csv', 'a+', newline='')).writerows(error_msg)
        else:
            print(url[1] + ": 写入成功")
    '''
    '    opt_split: 将ClassNums划分成数据项，并将其组织成list ：若有-，则展开；若有"，",拆开    接口是ClassNums
    '    opt_class_nums: 逐个提取data中的ClassNums，调用opt_split(ClassName), 得到数据项列表, 添加剩余信息即可。
    '                    重复上述操作，知道将ClassNums处理完。                                           '''
    def opt_class_nums(self, data):  # data 不含 header
        t1 = []; temp = []; i = 0  # t1 = temp = [] 会出错
        for row in data:
            t1.append([row[8]])
        for row in t1:
            for opt in self.opt_split(row):
                tt = data[i]
                if opt[0]:  # 排除空
                    temp.append([tt[2], tt[3], tt[0], opt[0]])
            i += 1
        return temp

    def opt_split(self, opt):  # opt = ["软件工程1601-软件工程1603,计科1601"]]
        data = list(str(opt[0]).split("，")); temp = []
        for row in data:
            if not row.count("-"):
                temp.append([row])
            else:
                k = int(len(row)/2)
                for i in range(int(row[k-4:k]), int(row[-4:])+1):
                    temp.append([str(row[:k-4]) + str(i)])
        return temp
    '''
    '	dis_del_repeat: 针对学生、教师文件的去重 主键是: ["ID"] , ["WeChatID"]  
    '	col_del_repeat:	针对课程文件的去重	   主键是: ["CourseID", "ClassNums"]  
    '																	'''
    def dis_del_repeat(self, data, key): # 调用了两次
        t1 = set(); temp = []
        for row in data:
            t1.add(row[key])  # list
        for row in list(t1):  # list
            for hh in data:
                if hh[key] == row:
                    temp.append(hh)
                    break
        return temp

    def col_del_repeat(self, data):
        t1 = set(); temp = []
        for row in data:
            t1.add(str([row[2], row[8]]))  # str
        for row in t1:  # str
            for hh in data:
                if str([hh[2], hh[8]]) == row:
                    temp.append(hh)
                    break
        return temp