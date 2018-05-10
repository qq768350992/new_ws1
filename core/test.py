#! coding:utf-8
import import_data, os


t = import_data.ImportData()

key = 0 # 管理员身份

# data = input()


'''
'	data = " sv.txt+ studentInfo.csv studentInfo.csv  courseProgress.csv  wsw j 软件工程1401.csv  666 "
'	t.man_import_input(data, 0)
'	print("-------------------以上是手动输入文件名---------------------------------")
'	print("-----------------------------------------------------")                                 '''


print("-------------------自动导入路径下所有csv文件---------------------------")
postion = r"C:\Users\Ivar\Desktop\软件工程\Source\exterior"




def aotu_import_input(url, key):  # 手动导入  固定的文件路径
    data = []
    for parent, fff, filenames in os.walk(url):
        for filename in filenames:
            if not filename[:-1].endswith(".csv"):
                data.append([os.path.join(parent, filename), filename])
    for url in data:
        t.import_file(url)

aotu_import_input(postion, 0)
# if key:  # 只保留.csv
    # return False


# def man_import_input(self, data, key):  # key = 0 管理员 固定文件目录下：
#     if key:
#         return False
#     temp = ImportData.get_file(data)  # data 为字符串类型 input()的返回值
#     no_repeat = list(set(temp))  # 去重
#     for url in no_repeat:
#         self.import_file(url)


# def get_file(self, data):  # data = "   course.csv    www.csv     软件工程1401.csv    "
#     temp = list(data);
#     sum_str = [];
#     st = ""
#     for i in temp:
#         if i != " ":
#             st += str(i)
#         elif (i == " ") and st != "":
#             sum_str.append(st)
#             st = ""
#     if st:
#         sum_str.append(st)
#     return sum_str