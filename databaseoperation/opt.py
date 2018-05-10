# !coding:utf-8
import csv

class Opt:
    def __init__(self):
        self.url = {
            "sum": "../data/sum/0_1_sum.csv",
            "detail": "../data/detail/0_1_2_checkinDetail.csv",
            "randomdetail": "../data/random_detail/0_1_2_randomcheckinDetail.csv",
            "seq": "../data/seq.csv",
            "setting": "../interior/settings.ini",
            "courseInfo": "../interior/courseInfo.csv",
            "teacherInfo": "../interior/teacherInfo.csv",
            "studentInfo": "../interior/studentInfo.csv",
        }

    def readfile(self, filename, args=None):
        url = self.url.get(str(filename))
        if url:
            if args :
                if len(args)==2:
                    url = url.replace("0", str(args[0])).replace("1", str(args[1]))
                elif len(args)==3:
                    url = url.replace("0", str(args[0])).replace("1", str(args[1])).replace("2", str(args[2]))
            try:
                return [row for row in csv.reader(open(url), encoding='utf-8')]
            except IOError:
                print("读取失败或不存在")
                return False
        else:print("文件格式错误")

    def writefile(self, data, filename, args=None, type="w"):
        url = self.url.get(str(filename))
        if url:
            if args:
                if len(args)==2:
                    url = url.replace("0", str(args[0])).replace("1", str(args[1]))
                elif len(args)==3:
                    url = url.replace("0", str(args[0])).replace("1", str(args[1])).replace("2", str(args[2]))
            if type == "w" or type == "w+":
                csv.writer(open(url, 'w+', newline='')).writerows(data)
            elif type == "a" or type == "a+":
                csv.writer(open(url, 'a+', newline='')).writerows(data)
        else:print("文件格式错误")


if __name__ == "__main__":
    t = Opt()
    t.readfile("seq")
    t.readfile("randomdetail")
