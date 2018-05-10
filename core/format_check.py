#! coding:utf-8
import re
''' 
'   有错误 写入log文件中    url = ../log/error.log
'   接口 data  和  error_msg
'   StuID,StuName,ClassID,WeChatID,(FeaturePath)
'   "| ERROR: Id Format Error : 3 line, teacherInfo.csv"
'   | ERROR: Name Format Error : 1 line teacherInfo.csv
'   当” “ 出现在log文件中时，说明 在string中加入 了 逗号 ”,"
'
'   data 存放了信息文件的所有信息，需要注意的一点是其不包括 header，即各列数据项的类型或命名格式
'   error 用于存放错误日志                                                          '''


def stu_check(data, error_msg):     # 最后更新error_msg 减少i/o
    for row in data:
        check_id(row[0], 12, error_msg, str(data.index(row)+2))
        check_name(row[1], error_msg, str(data.index(row)+2))
        check_class(row[2], error_msg, str(data.index(row)+2))  # ClassName
        check_wechat(row[3], error_msg, str(data.index(row)+2))


def tea_check(data, error_msg):
    for row in data:
        check_id(row[0], 7, error_msg, str(data.index(row)+2))
        check_name(row[1], error_msg, str(data.index(row)+2))
        check_wechat(row[2], error_msg, str(data.index(row)+2))


def course_check(data, error_msg):
    for row in data:
        check_id(row[0], 7, error_msg, str(data.index(row)+2))
        check_name(row[1], error_msg, str(data.index(row)+2))
        check_id(row[2], 7, error_msg, str(data.index(row)+2), 1)
        check_class_nums(row[8], error_msg, str(data.index(row)+2))


def file_header(header, error_msg):
    for row in header:
        if re.findall('^([a-zA-Z])$', row):
            error_msg.append(["    致命错误: 缺少关键的头信息"])
            return False
    return True


def check_id(element, num, error_msg, line, b=0):
    if not re.findall("^[\d]{"+str(num)+"}$", element):
        if b == 0:
            error_msg.append(["    Format:ID  "+"Line:"+line ])
        else:
            error_msg.append(["    Format:CourseID  "+"Line:"+line ])


def check_name(element, error_msg, line):
    if not re.findall('^([a-zA-Z\u4e00-\u9fa5\·]{2,10})$', element):
        error_msg.append(["    Format:Name  "+"Line:"+line ])


def check_class(element, error_msg, line):
    if not re.findall('^[\u4e00-\u9fa5]+\d{4}$', element):
        error_msg.append(["    Format:ClassName  "+"Line:"+line])


def check_wechat(element, error_msg, line):
    if not re.findall('^[a-zA-Z0-9_]+$', element):
        error_msg.append(["    Format:WeChat  "+"Line:"+line])


def check_class_nums(element, error_msg, line):
    if not re.findall('^([0-9\u4e00-\u9fa5\，\-]{5,100})$', element):
        error_msg.append(["    Format:ClassNums  "+"Line: "+line])