# !coding:utf-8
import csv,os

class Opt:
    def __init__(self):
        self.url = {
            "sum"          :  "../data/sum/0_1_sum.csv",
            "detail"       :  "../data/detail/0_1_2_checkinDetail.csv",
            "randomdetail" :  "../data/random_detail/0_1_2_randomcheckinDetail.csv",
            "seq"          :  "../data/seq.csv",
            "setting"      :  "../interior/settings.ini",
            "courseInfo"   :  "../interior/courseInfo.csv",
            "teacherInfo"  :  "../interior/teacherInfo.csv",
            "studentInfo"  :  "../interior/studentInfo.csv",
        }
        self.header = {
            "sum": ["stuid"],
            "detail": ["StuID","checkinTime","ProofPath","checkinType","IsSucc","checkinResult"],
            "randomdetail": ["StuID","checkinTime","ProofPath","checkinType","IsSucc","checkinResult"],
            "seq": ["TeacherID","CourseID","SeqID","StartTime"],
        }

    def newfile(self, filename, args=None):
        url = self.url.get(str(filename))
        if url:
            if args:
                if len(args) == 2:
                    url = url.replace("1", str(args[1]),1).replace("0", str(args[0]),1)
                elif len(args) == 3:
                    url = url.replace("2", str(args[2]),1).replace("1", str(args[1]),1).replace("0", str(args[0]),1)
            if not os.path.isfile(url):
                csv.writer(open(url, 'w+', newline='')).writerow(self.header.get(filename))

    def readfile(self, filename, args=None):
        url = self.url.get(str(filename))
        if url:
            if args :
                if len(args) == 2:
                    url = url.replace("1", str(args[1]),1).replace("0", str(args[0]),1)
                elif len(args) == 3:
                    url = url.replace("2", str(args[2]),1).replace("1", str(args[1]),1).replace("0", str(args[0]),1)
            try:
                # return [row for row in csv.reader(open(url), encoding='utf-8')]
                return [row for row in csv.reader(open(url))]
            except IOError:
                return []

    def writefile(self, data, filename, args=None, type="w"):
        url = self.url.get(str(filename))
        print(url)

        if url:
            if args:
                if len(args) == 2:
                    url = url.replace("1", str(args[1]),1).replace("0", str(args[0]),1)
                elif len(args) == 3:
                    url = url.replace("2", str(args[2]),1).replace("1", str(args[1]),1).replace("0", str(args[0]),1)
            if type == "w" or type == "w+":
                csv.writer(open(url, 'w+', newline='')).writerows(data)
            elif type == "a" or type == "a+":
                csv.writer(open(url, 'a+', newline='')).writerows(data)

    def delfile(self, filename, args=None):
        url = self.url.get(str(filename))
        if url:
            if args:
                if len(args) == 2:
                    url = url.replace("1", str(args[1]), 1).replace("0", str(args[0]), 1)
                elif len(args) == 3:
                    url = url.replace("2", str(args[2]), 1).replace("1", str(args[1]), 1).replace("0", str(args[0]), 1)
            try:
                os.remove(url)
            except:
                print("无法删除"+filename+".csv")

if __name__ == "__main__":
    t = Opt()
    t.delfile("seq")
