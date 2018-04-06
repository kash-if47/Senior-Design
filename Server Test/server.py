import socket
import threading
import glob #   currently not being used .. ???
import shutil
import os
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QThread
import pymysql
import datetime

filename = ""
searchStaffStatus = 0
searchStudentStatus = 0

#   function connects to the DB using pymysql module
#   returns the establish connection to make various queries on DB
def connectDB():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='rfid1234', db='rfid')
    # cur = conn.cursor()
    return conn

#   Encoding strings in best format for pyqt4
#
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class System(object):
    studentList = []
    staffList = []
    logList = []
    TagNamePicList = []
    # keeps track of what student we are editting
    editstudentid = -1
    # keeps track of what staff we are editting
    editstaffid = -1
    editstaffemail = ""
    listL = []
    listR = []

    #System Functions
    def __init__(self):
        try:
            conn = connectDB()
            cur = conn.cursor()

            #   Fetching initial data from Student table on the DB and appending to a list self.studentList
            cur.execute("SELECT * FROM student")
            data = cur.fetchall()
            for i in range(0, len(data)):
                Name = data[i][0]
                tagId = data[i][1]
                studentId = data[i][2]
                guardian = data[i][3]
                grade = data[i][4]
                pic = data[i][5]
                #student = Student(Name, studentId, tagId, guardian, pic,grade)
                #self.studentList.append(student)
                self.studentList.append(Student(Name, studentId, tagId, guardian, pic,grade))

            #   Fetching initial data from Staff table on the DB and appending to a list self.staffList
            cur.execute("SELECT * FROM staff")
            data2 = cur.fetchall()
            for i in range(0, len(data2)):
                fName = data2[i][0]
                Email = data2[i][1]
                password = data2[i][2]
                staffId = data2[i][3]
                isAdmin = data2[i][4]
                #staff = Staff(staffId, fName, Email, password, isAdmin)
                #self.staffList.append(staff)
                self.staffList.append(Staff(staffId, fName, Email, password, isAdmin))

        #   Fetching all the data from LOG on the DB and appending to a list off the self.logList
        #   Pulls all log data from DB and inputs to a list, Does the list update
        #   with new log information after list has appended? From initial append ????
            cur.execute("SELECT * FROM LOG")
            data = cur.fetchall()
            for i in range(0, len(data2)):
                staffid = data2[i][0]
                studentid = data2[i][1]
                date = data2[i][2]
                time = data2[i][3]
                self.logList.append(Log(staffid,studentid,date,time))


        except:
            print("db error HEHE")

    #   Adds new student from the editStudent on the gui left, provides no checking of invalid or duplicate responses
    #   inputs the data to the Database for the newly created student
    def addnewStudent(self,name,id,rfid,gname,pic,grade):
        conn = connectDB()
        cur = conn.cursor()
        query = "INSERT INTO STUDENT (Name, TagId, StudentID, GuardianName, grade, pic) VALUES (%s,%s,%s,%s,%s,%s);"
        queryval = (name,rfid,id,gname,grade,pic)
        cur.execute(query,queryval)
        conn.commit()
        conn.close()

    #   Adds new staff from the editStaff on the gui middle, provides no checking of invalid or duplicate responses
    #   inputs the data to the Database for the newly created staff
    def addnewStaff(self,name,id,Email,password,is_admin):
        conn = connectDB()
        cur = conn.cursor()
        query = "INSERT INTO STAFF (Fname, Email, Password, StaffID, isAdmin) VALUES (%s,%s,%s,%s,%s);"
        queryval = (name, Email, password, id, is_admin)
        cur.execute(query,queryval)
        conn.commit()
        conn.close()

    #   Function goes through the entire list of currently available students in self.studentList
    #   checking each STUDENT id (function name makes no distinction of STAFF) for duplicates in studentID
    #   returns bool False if no id match the studentList, True if a current student has that identical ID
    def checkDuplicateID(self,id):
        result = False
        for i in range(0, len(self.studentList)):
            idval = self.studentList[i].studentId
            if int(id) == idval:
                #print("found " + id)
                result = True

        return result

    #   Function goes through the entire list of currently available staff in self.staffList
    #   checking each STAFF id for duplicates in staffID
    #   returns bool False if no id match the staffList, True if a current staff member has identical ID
    def checkDuplicateIDStaff(self,id):
        result = False
        for i in range(0, len(self.staffList)):
            idval = self.staffList[i].staffId
            if int(id) == idval:
                #print("found " + id)
                result = True
        return result

    #   Function takes email address as parameter, goes through the entire list of self.staffList
    #   if there is a staff with a matching email then return that staff's ID number
    #   returns Staff's ID number or -1/False if no staff have that maching email
    def emailToId(self, email):
        for i in range (0, len(self.staffList)):
            if email == self.staffList[i].Email:
                return self.staffList[i].staffId
        return -1

    #   Function takes parameters needed to add/edit a student, connects to the DB and updates the student table
    #   found in edit student gui left, once pressed list of available students will appear. Selecting student in question
    #   then pressing editstudent will allow the admin to edit all fields of the currently selected student. (student id should not be allowed to be modified )
    #   Creates new empty studentList and then repopulates all data from DB into newly created list.
    def editStudent(self,id,grade,rfid,name,gname,pic):
        conn = connectDB()
        cur = conn.cursor()
        if (pic == ""):
            pic = Sys.getPicFromID()
        cur.execute ("""   UPDATE student   SET Name=%s, TagId=%s, StudentID=%s ,GuardianName=%s, grade=%s ,pic=%s  WHERE StudentID=%s""", (name, rfid, id, gname, grade, pic, Sys.editstudentid))
        conn.commit()
        cur.execute("SELECT * FROM student")
        data = cur.fetchall()
        self.studentList = []
        for i in range(0, len(data)):
            Name = data[i][0]
            tagId = data[i][1]
            studentId = data[i][2]
            guardian = data[i][3]
            grade = data[i][4]
            pic = data[i][5]
            student = Student(Name, studentId, tagId, guardian, pic, grade)
            self.studentList.append(student)
        #   Add notes about sys.editstudentid, confused about it's function
        Sys.editstudentid = -1
        conn.close()

    #   Function takes parameters needed to add/edit a staff, connects to the DB and updates the staff table
    #   found in edit staff gui middle, once pressed list of available staff will appear. Selecting staff in question
    #   then pressing editstaff will allow the admin to edit all fields of the currently selected student. (staff id should not be allowed to be modified )
    #   Creates new empty staffList and then repopulates all data from DB into newly created list.
    def editStaff(self,name,Email,password,id):

        conn = connectDB()
        cur = conn.cursor()
        cur.execute ("""   UPDATE staff  SET Fname=%s, Email=%s, Password=%s, StaffID=%s  WHERE StaffID=%s""", (name, Email, password, id, self.editstaffid))
        conn.commit()
        temp = cur.execute("SELECT * FROM staff")
        print(str(temp) + " This is temp" )
        data = cur.fetchall()
        self.staffList = []
        for i in range(0, len(data)):
            fName = data[i][0]
            Email = data[i][1]
            password = data[i][2]
            staffId = data[i][3]
            isAdmin = data[i][4]
            staff = Staff(staffId, fName, Email, password, isAdmin)
            self.staffList.append(staff)
        self.editstaffid = -1
        self.editstaffemail = ""
        conn.close()

    #   Function returns list of studentNames found in the most current list of self.studentList and returns list to calling function
    def getStudentNames(self):
        result = []
        for i in range(0, len(self.studentList)):
            name = self.studentList[i].Name
            result.append(name)
        return result

    #   Function returns list of staffNames found in the most current list of self.staffList and returns list to calling function
    def getStaffNames(self):
        result = []
        for i in range(0, len(self.staffList)):
            name = self.staffList[i].Name
            result.append(name)
        return result

    #   Function returns image from a STUDENT where the current id the function is comparing itself to is from the selected student's ID in the GUI
    def getPicFromID(self):
        for i in range(0, len(self.studentList)):
            if self.studentList[i].studentId == Sys.editstudentid:
                return self.studentList[i].image

    #   Function returns Student Name based on the parameter, id, by going through all students in self.studentList
    def getStudentNameById(self, id):
        for i in range(0, len(self.studentList)):
            if self.studentList[i].studentId == id:
                return self.studentList[i].Name
        return -1

    #   Function returns Staff Name based on the parameter, id, by going through all staff in self.staffList
    def getStaffNameById(self, id):
        for i in range(0, len(self.staffList)):
            if self.staffList[i].staffId == id:
                return self.staffList[i].Name
        return -1

    #   Function adds new log entry, inserts into the DB log table with the staffID and StudentID of the GLOBAL currentUser
    #   Log table automatically adds the date time in the table
    def logEntry(self, studentId):
        print("Log Entry Funct with input: " + str(studentId))
        staffId = self.emailToId(currentUser)
        conn = connectDB()
        cur = conn.cursor()
        query = "INSERT INTO LOG (StaffID, StudentID) VALUES (%s,%s);"
        queryval = (staffId, studentId)
        cur.execute(query, queryval)
        conn.commit()
        conn.close()

    #   Function takes the rfid Tag as parameter to look up a STUDENT
    #   if a student has the matching rfid tag in question, that student(name, tagid, studentID, gName, etc) is returned to the calling function
    def lookUpRfid(self, rfid):
        for i in range(0, len(self.studentList)):
            if self.studentList[i].tagId == rfid:
                # self.logEntry(self.studentList[i].studentId)
                return self.studentList[i]
        return -1

    #   Function is used to promote a Staff member as an admin, its parameter ID, goes through the entire
    #   staffList and finds the machine staff, checks to see if isAdmin is True/False returns bool
    def promoteStaff(self,id):
        for i in range(0, len(self.staffList)):
            idval = self.staffList[i].staffId
            if int(id) == int(idval):
                if (self.staffList[i].isAdmin):
                    print("Already Admin")
                    return True
                else:
                    print("Not Admin")
                    return False

    #   Function does not makes any sense, uses searchbyname function with parameter (empty str)
    def redraw(self):
        self.searchByName("")

    #   function takes id as parameter and goes through all students in studentList, if the student is found. they are deleted from the list
    #   Problems can occur because this is only superficial. The student is not actually deleted from the DB and will appear again if
    #   a function repopulates the studentList
    def removeStudent(self,id):
        for i in range(0, len(self.studentList)):
            idval = self.studentList[i].studentId
            print(idval)
            if int(id) == int(idval):
                #print("found " + id)
                del self.studentList[i]     #Needs to be deleted from the DB for this to work correctly
                break

    #   function takes id, user as parameter and goes through all staff in staffList, if the staff is found. they are deleted from the list
    #   Problems can occur because this is only superficial. The staff is not actually deleted from the DB and will appear again if
    #   a function repopulates the staffList. CHECKS IF STAFF HAS EMAIL, doesn't make sense why removal would be denied
    def removeStaff(self,id,user):
        for i in range(0, len(self.staffList)):
            idval = self.staffList[i].staffId
            print(idval)
            if int(id) == int(idval):
                #print("found " + id)
                if(user == self.staffList[i].Email):    #why? checking if staff has email?
                    print("Removal Denied")
                    return 0
                else:
                    del self.staffList[i]       #superficial, needs to delete from DB
                    print("Staff Removed")
                    return 1

    #   Function takes string name as parameter, (prints the length of studentlist as string, why????)
    #   name parameter is lowerCased, then searches the entire studentList
    #   No return error if the name in question is not found in the studentList
    def searchByName(self, name):
        print(str(len(self.studentList)))
        result = []
        name = name.lower()

        for i in range(0, len(self.studentList)):   #for each name in StudentList
            fullName = self.studentList[i].Name     #name is saved into fullName variable and lowerCased
            fullName = fullName.lower()

            if name in fullName:    #   if the name we are searching for is found in the studentList(if name == fullname: ????)
                #print("found " + fullName)
                result.append(self.studentList[i])      #   append the student to result list and return
        return result

    #   Function takes string name as parameter,
    #   name parameter is lowerCased, then searches the entire studentList
    #   No return error if the name in question is not found in the studentList
    def searchByNameStaff(self, name):
        print("search staff name")
        searchStaffStatus=1
        result = []
        name = name.lower()
        for i in range(0, len(self.staffList)):
            fullName = self.staffList[i].Name
            fullName = fullName.lower()
            if name in fullName:
                #print("found " + fullName)
                result.append(self.staffList[i])
        return result

    #   Function searches STUDENT id from StudentList, if found, returns the Student in question
    def searchByID(self, id):

        result = []
        for i in range(0, len(self.studentList)):
            idval = self.studentList[i].studentId
            if int(id) == int(idval) :
                #print("found " + id)
                result.append(self.studentList[i])
        #   else return -1 ??? (wouldn't this work here?)
        if(len(result) == 0):
            print("not found")
            return -1   #why two return statements back to back? 1 should suffice
        return result

    #   Function searches Staff id from staffList if the id matches we return 1 (This must be a temporary function as I see the old one below)
    def searchStaffIdNew(self, id):
        for i in range(0, len(self.staffList)):
            if id == self.staffList[i].staffId:
                return 1        # why return 1? each staff has ID 1?
        return -1

    #   Function searches Staff id from STaffList, if found returns result list
    def searchByIdStaff(self, id):
        result = []
        print("search staff id")
        print(searchStaffStatus)
        for i in range(0, len(self.staffList)):
            idval = self.staffList[i].staffId
            if int(id) == int(idval) :
                #print("found " + id)
                result.append(self.staffList[i])
                #return result
            #else return -1
        if(len(result) == 0):
            print("not found")
        return result

    # Used in RedrawTables(), ShowStudentLogFunc()
    def showLogData(self):
        conn = connectDB()
        cur = conn.cursor()
        cur.execute("SELECT * FROM LOG")
        dataMain = cur.fetchall()
        ui.LogListWidget_Staff.clear()
        ui.LogListWidget_Student.clear()

        sDate = ui.StartDateEdit.date()
        eDate = ui.EndDateEdit.date()

        sDate = sDate.toPyDate()
        eDate = eDate.toPyDate()

        data = {'Student ID': [], 'Student Name': [], 'Staff ID': [], 'Staff Name': [], 'Date': [], 'Time': []}
        count = 0
        for i in range(0, len(dataMain)):
            logDate = str(dataMain[i][2]).split(" ")[0]
            logDate = datetime.datetime.strptime(logDate, '%Y-%m-%d').date()
            difference = eDate - sDate
            print(difference)
            logdiff = logDate - sDate
            if ((logdiff <= difference) and (logdiff >= datetime.timedelta(days=0))):
                count = count + 1
                data['Student ID'].append(str(dataMain[i][1]))
                data['Staff ID'].append(str(dataMain[i][0]))
                data['Student Name'].append(Sys.getStudentNameById(dataMain[i][1]))
                data['Staff Name'].append(Sys.getStaffNameById(dataMain[i][0]))
                data['Date'].append(str(dataMain[i][2]).split(" ")[0])
                data['Time'].append(str(dataMain[i][2]).split(" ")[1])
            ui.LogTableView_Generic.setColumnCount(6)
            ui.LogTableView_Generic.setRowCount(count)
        horHeaders = []
        for n, key in enumerate(sorted(data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                ui.LogTableView_Generic.setItem(m, n, newitem)
            ui.LogTableView_Generic.setHorizontalHeaderLabels(horHeaders)
            ui.LogTableView_Generic.show()

        result = Sys.getStudentNames()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i])
            ui.LogListWidget_Student.addItem(item)

        result = Sys.getStaffNames()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i])
            ui.LogListWidget_Staff.addItem(item)
        print(result)

    # Not used in any other location, just defined below
    def showStudentReport(self):
        result = Sys.getStudentNames()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i])
            ui.LogListWidget_Student.addItem(item)

    # Not used in any other location, just defined below
    def showStaffReport(self):
        result = Sys.getStaffNames()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i])
            ui.LogListWidget_Staff.addItem(item)

    def searchByEmail(self, email):
        for i in range(0, len(self.staffList)):
            tempEmail = self.staffList[i].Email
            tempId = self.staffList[i].staffId
            if(tempEmail == email) and (Sys.editstaffid != tempId):
                return True
        return False

class Student(object):
    studentId = 0
    tagId = ""
    Name = ""
    guardian = ""
    image = ""
    grade = 0

    # The class "constructor" - It's actually an initializer
    def __init__(self, Name, studentId, tagId, guardian, image, grade):
        self.studentId = studentId
        self.Name = Name
        self.guardian = guardian
        self.tagId = tagId
        self.image = image
        self.grade = grade

class Staff(object):
    staffId = 0
    Name = ""
    Email = ""
    password = ""
    isAdmin = 0

    def __init__(self, staffId, Name, Email, password, isAdmin):
        self.staffId = staffId
        self.Name = Name
        self.Email = Email
        self.password = password
        self.isAdmin = isAdmin

class Log(object):
    staffID = 0
    studentID = 0
    date = ""
    timestamp = ""

    def __init__(self,staffID,studentID,date,time):
        self.staffID = staffID
        self.studentID = studentID
        self.date = date
        self.timestamp = time

class Ui_MainWindow(object):
    # UI Functions
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1200, 900)

        #Double list page
        ThickFont = QtGui.QFont()
        ThickFont.setPointSize(11)
        ThickFont.setBold(True)
        ThickFont.setWeight(75)
        TitleFont = ThickFont
        TitleFont.setPointSize(12)

        self.LeftList = QtGui.QListWidget(MainWindow)
        self.LeftList.setGeometry(QtCore.QRect(20, 240, 310, 380))
        self.LeftList.setFont(ThickFont)
        self.LeftList.setObjectName(_fromUtf8("LeftList"))
        self.LeftList.itemClicked.connect(self.updateLeftPicture)

        self.RightList = QtGui.QListWidget(MainWindow)
        self.RightList.setGeometry(QtCore.QRect(480, 240, 310, 380))
        self.RightList.setFont(ThickFont)
        self.RightList.setObjectName(_fromUtf8("RightList"))
        self.RightList.itemClicked.connect(self.updateRightPicture)

        self.LeftListTitle = QtGui.QLabel(MainWindow)
        self.LeftListTitle.setGeometry(QtCore.QRect(160, 10, 100, 40))
        self.LeftListTitle.setFont(TitleFont)
        self.LeftListTitle.setObjectName(_fromUtf8("LeftListTitle"))

        self.RightListTitle = QtGui.QLabel(MainWindow)
        self.RightListTitle.setGeometry(QtCore.QRect(620, 10, 100, 40))
        self.RightListTitle.setFont(TitleFont)
        self.RightListTitle.setObjectName(_fromUtf8("RightListTitle"))

        self.LeftClear = QtGui.QPushButton(MainWindow)
        self.LeftClear.setGeometry(QtCore.QRect(350, 360, 70, 25))
        self.LeftClear.setObjectName(_fromUtf8("LeftClear"))
        self.LeftClear.clicked.connect(self.handleClearLeft)

        self.RightClear = QtGui.QPushButton(MainWindow)
        self.RightClear.setGeometry(QtCore.QRect(820, 360, 70, 25))
        self.RightClear.setObjectName(_fromUtf8("RightClear"))
        self.RightClear.clicked.connect(self.handleClearRight)

        self.LeftStudentPicture = QtGui.QLabel(MainWindow)
        self.LeftStudentPicture.setGeometry(QtCore.QRect(150, 50, 180, 170))
        self.LeftStudentPicture.setObjectName(_fromUtf8("LeftStudentPicture"))

        self.RightStudentPicture = QtGui.QLabel(MainWindow)
        self.RightStudentPicture.setGeometry(QtCore.QRect(610, 50, 180, 170))
        self.RightStudentPicture.setObjectName(_fromUtf8("RightStudentPicture"))

        self.SplittingLine = QtGui.QFrame(MainWindow)
        self.SplittingLine.setGeometry(QtCore.QRect(450, 0, 20, 650))
        self.SplittingLine.setFrameShape(QtGui.QFrame.VLine)
        self.SplittingLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.SplittingLine.setObjectName(_fromUtf8("SplittingLine"))

        MainWindow.keyPressEvent = self.newOnKeyPressEvent
        #=======================================================
        #login Page
        self.Username = QtGui.QLabel(MainWindow)
        self.Username.setGeometry(QtCore.QRect(220, 180, 191, 101))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Username.setFont(font)
        self.Username.setObjectName(_fromUtf8("Username"))

        self.Password = QtGui.QLabel(MainWindow)
        self.Password.setGeometry(QtCore.QRect(220, 260, 191, 101))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Password.setFont(font)
        self.Password.setObjectName(_fromUtf8("Password"))

        self.Login_uname = QtGui.QLineEdit(MainWindow)
        self.Login_uname.setGeometry(QtCore.QRect(430, 210, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.Login_uname.setFont(font)
        self.Login_uname.setObjectName(_fromUtf8("Login_uname"))

        self.Login_password = QtGui.QLineEdit(MainWindow)
        self.Login_password.setEchoMode(QtGui.QLineEdit.Password)
        self.Login_password.setGeometry(QtCore.QRect(430, 290, 271, 41))
        self.Login_password.setObjectName(_fromUtf8("Login_password"))

        self.LoginButton = QtGui.QPushButton(MainWindow)
        self.LoginButton.setGeometry(QtCore.QRect(520, 450, 211, 61))
        self.LoginButton.setObjectName(_fromUtf8("LoginButton"))
        self.LoginButton.clicked.connect(self.MainAdminfunc)

        self.LoginTitle = QtGui.QLabel(MainWindow)
        self.LoginTitle.setGeometry(QtCore.QRect(450, 90, 421, 80))
        self.LoginTitle.setObjectName(_fromUtf8("LoginTitle"))
        self.LoginTitle.setText("Login")
        BigRedFont = QtGui.QFont()
        BigRedFont.setPointSize(50)
        self.LoginTitle.setFont(BigRedFont)
        self.LoginTitle.setStyleSheet('color: red')

        self.LogOffStaff = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffStaff.setGeometry(QtCore.QRect(790, 780, 187, 41))
        self.LogOffStaff.setObjectName(_fromUtf8("LogOffStaff"))
        self.LogOffStaff.clicked.connect(self.LogOffStafffunc)

        #=======================================================
        # main admin page need to fix by adding log and pushing buttons to menu
        self.LogOffAdmin1 = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffAdmin1.setGeometry(QtCore.QRect(990, 10, 187, 41))
        self.LogOffAdmin1.setObjectName(_fromUtf8("LogOffAdmin1"))
        self.LogOffAdmin1.clicked.connect(self.LogOffAdminfunc)

        self.verticalLayoutWidget = QtGui.QWidget(MainWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 169, 1071, 271))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.EditStudent = QtGui.QPushButton(self.verticalLayoutWidget)
        self.EditStudent.setObjectName(_fromUtf8("EditStudent"))
        self.EditStudent.clicked.connect(self.ShowAdminFunc)
        self.horizontalLayout.addWidget(self.EditStudent)

        self.EditStaff = QtGui.QPushButton(self.verticalLayoutWidget)
        self.EditStaff.setObjectName(_fromUtf8("EditStaff"))
        self.EditStaff.clicked.connect(self.ShowStaffWindonFunc)
        self.horizontalLayout.addWidget(self.EditStaff)

        self.StudentLog = QtGui.QPushButton(self.verticalLayoutWidget)
        self.StudentLog.setObjectName(_fromUtf8("StudentLog"))
        self.StudentLog.clicked.connect(self.ShowStudentLogFunc)

        self.horizontalLayout.addWidget(self.StudentLog)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)

        self.StudentCheckout = QtGui.QPushButton(self.verticalLayoutWidget)
        self.StudentCheckout.setObjectName(_fromUtf8("StudentCheckout"))
        self.horizontalLayout_2.addWidget(self.StudentCheckout)
        self.StudentCheckout.clicked.connect(self.showMain)

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.adminlabel_welcome = QtGui.QLabel(MainWindow)
        self.adminlabel_welcome.setGeometry(QtCore.QRect(30, 10, 981, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.adminlabel_welcome.setFont(font)
        self.adminlabel_welcome.setObjectName(_fromUtf8("adminlabel_welcome"))

        self.adminlabel_student = QtGui.QLabel(MainWindow)
        self.adminlabel_student.setGeometry(QtCore.QRect(120, 270, 141, 20))
        self.adminlabel_student.setObjectName(_fromUtf8("adminlabel_student"))

        self.adminlabel_staff = QtGui.QLabel(MainWindow)
        self.adminlabel_staff.setGeometry(QtCore.QRect(490, 250, 201, 61))
        self.adminlabel_staff.setObjectName(_fromUtf8("adminlabel_staff"))

        self.adminlabel_log = QtGui.QLabel(MainWindow)
        self.adminlabel_log.setGeometry(QtCore.QRect(850, 270, 171, 16))
        self.adminlabel_log.setObjectName(_fromUtf8("adminlabel_log"))

        self.adminlabel_checkout = QtGui.QLabel(MainWindow)
        self.adminlabel_checkout.setGeometry(QtCore.QRect(480, 410, 191, 16))
        self.adminlabel_checkout.setObjectName(_fromUtf8("adminlabel_checkout"))

        #=======================================================
        #Log page
        today = QtCore.QDate.currentDate()
        mindate = today.addMonths(-1)

        self.DismissWidget = QtGui.QTabWidget(MainWindow)
        self.DismissWidget.setGeometry(QtCore.QRect(10, 90, 900, 440))
        self.DismissWidget.setMaximumSize(QtCore.QSize(1200, 900))
        self.DismissWidget.setObjectName(_fromUtf8("DismissWidget"))

        self.GenericTab = QtGui.QWidget()
        self.GenericTab.setObjectName(_fromUtf8("GenericTab"))
        self.DismissWidget.addTab(self.GenericTab, _fromUtf8(""))

        self.StudentTab = QtGui.QWidget()
        self.StudentTab.setObjectName(_fromUtf8("StudentTab"))
        self.DismissWidget.addTab(self.StudentTab, _fromUtf8(""))

        self.StaffTab = QtGui.QWidget()
        self.StaffTab.setObjectName(_fromUtf8("StaffTab"))
        self.DismissWidget.addTab(self.StaffTab, _fromUtf8(""))

        #Log Labels
        logFont = QtGui.QFont()
        logFont.setPointSize(24)

        self.LogLabel_Title = QtGui.QLabel(MainWindow)
        self.LogLabel_Title.setGeometry(QtCore.QRect(310, 20, 251, 51))
        self.LogLabel_Title.setMaximumSize(QtCore.QSize(1200, 900))
        self.LogLabel_Title.setFont(logFont)
        self.LogLabel_Title.setObjectName(_fromUtf8("LogLabel_Title"))

        self.LogLabel_Start = QtGui.QLabel(MainWindow)
        self.LogLabel_Start.setGeometry(QtCore.QRect(20, 540, 61, 21))
        self.LogLabel_Start.setMaximumSize(QtCore.QSize(1200, 900))
        self.LogLabel_Start.setObjectName(_fromUtf8("LogLabel_Start"))

        self.LogLabel_End = QtGui.QLabel(MainWindow)
        self.LogLabel_End.setGeometry(QtCore.QRect(190, 540, 61, 21))
        self.LogLabel_End.setMaximumSize(QtCore.QSize(1200, 900))
        self.LogLabel_End.setObjectName(_fromUtf8("LogLabel_End"))

        self.LogStudentLabel_SearchName = QtGui.QLabel(self.StudentTab)
        self.LogStudentLabel_SearchName.setGeometry(QtCore.QRect(0, 360, 101, 16))
        self.LogStudentLabel_SearchName.setObjectName(_fromUtf8("LogStudentLabel_SearchName"))

        self.LogStudentLogLabel_SearchID = QtGui.QLabel(self.StudentTab)
        self.LogStudentLogLabel_SearchID.setGeometry(QtCore.QRect(220, 360, 61, 16))
        self.LogStudentLogLabel_SearchID.setObjectName(_fromUtf8("LogStudentLogLabel_SearchID"))

        self.LogStaffLabel_SearchName = QtGui.QLabel(self.StaffTab)
        self.LogStaffLabel_SearchName.setGeometry(QtCore.QRect(0, 360, 101, 16))
        self.LogStaffLabel_SearchName.setObjectName(_fromUtf8("LogStaffLabel_SearchName"))

        self.LogStaffLabel_SearchID = QtGui.QLabel(self.StaffTab)
        self.LogStaffLabel_SearchID.setGeometry(QtCore.QRect(220, 360, 61, 16))
        self.LogStaffLabel_SearchID.setObjectName(_fromUtf8("LogStaffLabel_SearchID"))

        #Log Textfields
        self.LogStudentText_SearchName = QtGui.QLineEdit(self.StudentTab)
        self.LogStudentText_SearchName.setGeometry(QtCore.QRect(0, 390, 211, 31))
        self.LogStudentText_SearchName.setObjectName(_fromUtf8("LogStudentText_SearchName"))

        self.LogStudentText_SearchID = QtGui.QLineEdit(self.StudentTab)
        self.LogStudentText_SearchID.setGeometry(QtCore.QRect(220, 390, 181, 31))
        self.LogStudentText_SearchID.setObjectName(_fromUtf8("LogStudentText_SearchID"))

        self.LogStaffText_SearchName = QtGui.QLineEdit(self.StaffTab)
        self.LogStaffText_SearchName.setGeometry(QtCore.QRect(0, 390, 211, 31))
        self.LogStaffText_SearchName.setObjectName(_fromUtf8("LogStaffText_SearchName"))

        self.LogStaffText_SearchID = QtGui.QLineEdit(self.StaffTab)
        self.LogStaffText_SearchID.setGeometry(QtCore.QRect(220, 390, 181, 31))
        self.LogStaffText_SearchID.setObjectName(_fromUtf8("LogStaffText_SearchID"))

        #Log DateEdits
        self.StartDateEdit = QtGui.QDateEdit(MainWindow)
        self.StartDateEdit.setGeometry(QtCore.QRect(10, 560, 110, 22))
        self.StartDateEdit.setMaximumSize(QtCore.QSize(1200, 900))
        self.StartDateEdit.setObjectName(_fromUtf8("StartDateEdit"))
        self.StartDateEdit.setDate(mindate)

        self.EndDateEdit = QtGui.QDateEdit(MainWindow)
        self.EndDateEdit.setGeometry(QtCore.QRect(180, 560, 110, 22))
        self.EndDateEdit.setMaximumSize(QtCore.QSize(1200, 900))
        self.EndDateEdit.setObjectName(_fromUtf8("EndDateEdit"))
        self.EndDateEdit.setDate(today)

        #Log Buttons
        self.LogOffAdmin2 = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffAdmin2.setGeometry(QtCore.QRect(700, 10, 187, 41))
        self.LogOffAdmin2.setMaximumSize(QtCore.QSize(1200, 900))
        self.LogOffAdmin2.setObjectName(_fromUtf8("LogOffAdmin2"))

        self.LogButton_Generate = QtGui.QPushButton(MainWindow)
        self.LogButton_Generate.setGeometry(QtCore.QRect(360, 560, 75, 23))
        self.LogButton_Generate.setMaximumSize(QtCore.QSize(1200, 900))
        self.LogButton_Generate.setObjectName(_fromUtf8("LogButton_Generate"))
        self.LogButton_Generate.clicked.connect(self.redrawTables)\

        self.LogButton_Print = QtGui.QPushButton(MainWindow)
        self.LogButton_Print.setGeometry(QtCore.QRect(450, 560, 75, 23))
        self.LogButton_Print.setMaximumSize(QtCore.QSize(1200, 900))
        self.LogButton_Print.setObjectName(_fromUtf8("LogButton_PrintPDF"))
        self.LogButton_Print.clicked.connect(self.PrintPDF)

        self.LogButton_Exit = QtGui.QPushButton(MainWindow)
        self.LogButton_Exit.setGeometry(QtCore.QRect(710, 560, 75, 23))
        self.LogButton_Exit.setMaximumSize(QtCore.QSize(1200, 900))
        self.LogButton_Exit.setObjectName(_fromUtf8("LogButton_Exit"))
        self.LogButton_Exit.clicked.connect(self.CancelActionfunc)

        self.LogStudentButton_SearchName = QtGui.QPushButton(self.StudentTab)
        self.LogStudentButton_SearchName.setGeometry(QtCore.QRect(130, 360, 75, 23))
        self.LogStudentButton_SearchName.setObjectName(_fromUtf8("LogStudentButton_SearchName"))
        self.LogStudentButton_SearchName.clicked.connect(self.searchNameStudentLog)

        self.LogStudentButton_SearchID = QtGui.QPushButton(self.StudentTab)
        self.LogStudentButton_SearchID.setGeometry(QtCore.QRect(320, 360, 75, 23))
        self.LogStudentButton_SearchID.setObjectName(_fromUtf8("LogStudentButton_SearchID"))
        self.LogStudentButton_SearchID.clicked.connect(self.searchIDStudentLog)

        self.LogStaffButton_SearchName = QtGui.QPushButton(self.StaffTab)
        self.LogStaffButton_SearchName.setGeometry(QtCore.QRect(130, 360, 75, 23))
        self.LogStaffButton_SearchName.setObjectName(_fromUtf8("LogStaffButton_SearchName"))
        self.LogStaffButton_SearchName.clicked.connect(self.searchNameStaffLog)

        self.LogStaffButton_SearchID = QtGui.QPushButton(self.StaffTab)
        self.LogStaffButton_SearchID.setGeometry(QtCore.QRect(320, 360, 75, 23))
        self.LogStaffButton_SearchID.setObjectName(_fromUtf8("LogStaffButton_SearchId"))
        self.LogStaffButton_SearchID.clicked.connect(self.searchIDStaffLog)

        #Log Lists
        self.LogListWidget_Student = QtGui.QListWidget(self.StudentTab)
        self.LogListWidget_Student.setGeometry(QtCore.QRect(0, 0, 400, 361))
        self.LogListWidget_Student.setObjectName(_fromUtf8("LogListWidget_Student"))
        self.LogListWidget_Student.itemClicked.connect(self.handleviewLogStudent)

        self.LogListWidget_Staff = QtGui.QListWidget(self.StaffTab)
        self.LogListWidget_Staff.setGeometry(QtCore.QRect(0, 0, 400, 361))
        self.LogListWidget_Staff.setObjectName(_fromUtf8("LogListWidget_Staff"))
        self.LogListWidget_Staff.itemClicked.connect(self.handleviewLogStaff)

        #Log Tables
        self.LogTableView_Generic = QtGui.QTableWidget(self.GenericTab)
        self.LogTableView_Generic.setGeometry(QtCore.QRect(0, 0, 900, 415))
        self.LogTableView_Generic.setObjectName(_fromUtf8("LogTableView_Generic"))

        self.LogTableView_Student = QtGui.QTableWidget(self.StudentTab)
        self.LogTableView_Student.setGeometry(QtCore.QRect(398, 0, 500, 421))
        self.LogTableView_Student.setObjectName(_fromUtf8("LogTableView_Student"))

        self.LogTableView_Staff = QtGui.QTableWidget(self.StaffTab)
        self.LogTableView_Staff.setGeometry(QtCore.QRect(398, 0, 500, 420))
        self.LogTableView_Staff.setObjectName(_fromUtf8("LogTableView_Staff"))

        #function added at end of log being created to prevent errors
        self.DismissWidget.currentChanged.connect(self.tabControl)
        #=======================================================
        #student window
        #generic font
        font = QtGui.QFont()
        font.setPointSize(12)
        #validators
        intvalidator = QtGui.QIntValidator()
        regex = QtCore.QRegExp("[a-z-A-Z _]+")
        azvalidator = QtGui.QRegExpValidator(regex)
        #Student Labels
        self.StudentLabel_Name = QtGui.QLabel(MainWindow)
        self.StudentLabel_Name.setGeometry(QtCore.QRect(530, 60, 81, 31))
        self.StudentLabel_Name.setFont(font)
        self.StudentLabel_Name.setObjectName(_fromUtf8("StudentLabel_Name"))

        self.StudentLabel_ID = QtGui.QLabel(MainWindow)
        self.StudentLabel_ID.setGeometry(QtCore.QRect(530, 130, 81, 31))
        self.StudentLabel_ID.setFont(font)
        self.StudentLabel_ID.setObjectName(_fromUtf8("StudentLabel_ID"))

        self.StudentLabel_Grade = QtGui.QLabel(MainWindow)
        self.StudentLabel_Grade.setGeometry(QtCore.QRect(530, 200, 121, 31))
        self.StudentLabel_Grade.setFont(font)
        self.StudentLabel_Grade.setObjectName(_fromUtf8("StudentLabel_Grade"))

        self.StudentLabel_GName = QtGui.QLabel(MainWindow)
        self.StudentLabel_GName.setGeometry(QtCore.QRect(530, 270, 81, 31))
        self.StudentLabel_GName.setFont(font)
        self.StudentLabel_GName.setObjectName(_fromUtf8("StudentLabel_GName"))

        self.StudentLabel_RFID = QtGui.QLabel(MainWindow)
        self.StudentLabel_RFID.setGeometry(QtCore.QRect(530, 340, 81, 31))
        self.StudentLabel_RFID.setFont(font)
        self.StudentLabel_RFID.setObjectName(_fromUtf8("StudentLabel_RFID"))

        self.StudentLabel_Picture = QtGui.QLabel(MainWindow)
        self.StudentLabel_Picture.setGeometry(QtCore.QRect(530, 410, 81, 31))
        self.StudentLabel_Picture.setFont(font)
        self.StudentLabel_Picture.setObjectName(_fromUtf8("StudentLabel_Picture"))

        self.StudentLabel_Picture_2 = QtGui.QLabel(MainWindow)
        self.StudentLabel_Picture_2.setGeometry(QtCore.QRect(530, 460, 361, 271))
        self.StudentLabel_Picture_2.setFont(font)
        self.StudentLabel_Picture_2.setObjectName(_fromUtf8("StudentLabel_Picture_2"))

        self.StudentLabel_SearchName = QtGui.QLabel(MainWindow)
        self.StudentLabel_SearchName.setGeometry(QtCore.QRect(10, 680, 91, 16))
        self.StudentLabel_SearchName.setObjectName(_fromUtf8("StudentLabel_SearchName"))

        self.StudentLabel_SearchID = QtGui.QLabel(MainWindow)
        self.StudentLabel_SearchID.setGeometry(QtCore.QRect(310, 680, 91, 16))
        self.StudentLabel_SearchID.setObjectName(_fromUtf8("StudentLabel_SearchID"))

        #Student Textfields
        self.StudentText_Name = QtGui.QLineEdit(MainWindow)
        self.StudentText_Name.setEnabled(False)
        self.StudentText_Name.setGeometry(QtCore.QRect(650, 60, 241, 31))
        self.StudentText_Name.setFont(font)
        self.StudentText_Name.setObjectName(_fromUtf8("StudentText_Name"))
        self.StudentText_Name.setValidator(azvalidator)

        self.StudentText_ID = QtGui.QLineEdit(MainWindow)
        self.StudentText_ID.setGeometry(QtCore.QRect(650, 130, 241, 31))
        self.StudentText_ID.setEnabled(False)
        self.StudentText_ID.setValidator(intvalidator)
        self.StudentText_ID.setFont(font)
        self.StudentText_ID.setObjectName(_fromUtf8("StudentText_ID"))

        self.StudentText_Grade = QtGui.QLineEdit(MainWindow)
        self.StudentText_Grade.setEnabled(False)
        self.StudentText_Grade.setGeometry(QtCore.QRect(650, 200, 241, 31))
        self.StudentText_Grade.setFont(font)
        self.StudentText_Grade.setObjectName(_fromUtf8("StudentText_Grade"))
        self.StudentText_Grade.setValidator(intvalidator)

        self.StudentText_GName = QtGui.QLineEdit(MainWindow)
        self.StudentText_GName.setGeometry(QtCore.QRect(650, 270, 241, 31))
        self.StudentText_GName.setEnabled(False)
        self.StudentText_GName.setFont(font)
        self.StudentText_GName.setObjectName(_fromUtf8("StudentText_GName"))
        self.StudentText_GName.setValidator(azvalidator)

        self.StudentText_RFID = QtGui.QLineEdit(MainWindow)
        self.StudentText_RFID.setGeometry(QtCore.QRect(650, 340, 241, 31))
        self.StudentText_RFID.setEnabled(False)
        self.StudentText_RFID.setFont(font)
        self.StudentText_RFID.setObjectName(_fromUtf8("StudentText_RFID"))

        self.StudentText_Picture = QtGui.QLineEdit(MainWindow)
        self.StudentText_Picture.setGeometry(QtCore.QRect(650, 410, 241, 31))
        self.StudentText_Picture.setFont(font)
        self.StudentText_Picture.setObjectName(_fromUtf8("StudentText_Picture"))

        #Student Buttons
        self.StudentButton_Remove = QtGui.QPushButton(MainWindow)
        self.StudentButton_Remove.setGeometry(QtCore.QRect(330, 830, 111, 23))
        self.StudentButton_Remove.setObjectName(_fromUtf8("StudentButton_Remove"))
        self.StudentButton_Remove.clicked.connect(self.RemoveStudentfunc)

        self.StudentButton_Exit = QtGui.QPushButton(MainWindow)
        self.StudentButton_Exit.setGeometry(QtCore.QRect(790, 780, 75, 23))
        self.StudentButton_Exit.setObjectName(_fromUtf8("StudentButton_Exit"))
        self.StudentButton_Exit.clicked.connect(self.CancelActionfunc)

        self.StudentButton_SaveAdd = QtGui.QPushButton(MainWindow)
        self.StudentButton_SaveAdd.setGeometry(QtCore.QRect(1000, 130, 75, 23))
        self.StudentButton_SaveAdd.setObjectName(_fromUtf8("StudentButton_SaveAdd"))
        self.StudentButton_SaveAdd.clicked.connect(self.handleAddSave)

        self.StudentButton_Picture = QtGui.QPushButton(MainWindow)
        self.StudentButton_Picture.setGeometry(QtCore.QRect(700, 410, 81, 31))
        self.StudentButton_Picture.setObjectName(_fromUtf8("StudentButton_Picture"))
        self.StudentButton_Picture.setText(_translate("MainWindow", "Browse", None))
        self.StudentButton_Picture.clicked.connect(self.handleBrowse)

        self.StudentButton_SaveEdit = QtGui.QPushButton(MainWindow)
        self.StudentButton_SaveEdit.setGeometry(QtCore.QRect(1000, 130, 75, 23))
        self.StudentButton_SaveEdit.setObjectName(_fromUtf8("StudentButton_SaveEdit"))
        self.StudentButton_SaveEdit.clicked.connect(self.confirmsavestudent)

        self.StudentButton_Cancel = QtGui.QPushButton(MainWindow)
        self.StudentButton_Cancel.setGeometry(QtCore.QRect(1000, 200, 75, 23))
        self.StudentButton_Cancel.setObjectName(_fromUtf8("StudentButton_Cancel"))
        self.StudentButton_Cancel.clicked.connect(self.handleAddCancel)

        self.StudentButton_Edit = QtGui.QPushButton(MainWindow)
        self.StudentButton_Edit.setGeometry(QtCore.QRect(170, 830, 101, 23))
        self.StudentButton_Edit.setObjectName(_fromUtf8("StudentButton_Edit"))
        self.StudentButton_Edit.clicked.connect(self.editStudentfunc)

        self.StudentButton_Add = QtGui.QPushButton(MainWindow)
        self.StudentButton_Add.setGeometry(QtCore.QRect(30, 830, 91, 23))
        self.StudentButton_Add.setObjectName(_fromUtf8("StudentButton_Add"))
        self.StudentButton_Add.clicked.connect(self.addStudentfunc)

        self.StudentButton_SearchName = QtGui.QPushButton(MainWindow)
        self.StudentButton_SearchName.setGeometry(QtCore.QRect(10, 740, 121, 27))
        self.StudentButton_SearchName.setObjectName(_fromUtf8("StudentButton_SearchName"))

        self.StudentButton_SearchID = QtGui.QPushButton(MainWindow)
        self.StudentButton_SearchID.setGeometry(QtCore.QRect(310, 740, 121, 27))
        self.StudentButton_SearchID.setObjectName(_fromUtf8("StudentButton_SearchID"))

        #Student Searchfield
        self.StudentSearch_ID = QtGui.QLineEdit(MainWindow)
        self.StudentSearch_ID.setGeometry(QtCore.QRect(310, 700, 161, 31))
        self.StudentSearch_ID.setObjectName(_fromUtf8("StudentSearch_ID"))
        self.StudentSearch_ID.setValidator(intvalidator)

        self.StudentSearch_Name = QtGui.QLineEdit(MainWindow)
        self.StudentSearch_Name.setGeometry(QtCore.QRect(10, 700, 281, 31))
        self.StudentSearch_Name.setObjectName(_fromUtf8("StudentSearch_Name"))
        self.StudentSearch_Name.setValidator(azvalidator)

        #Logoff Button
        self.LogOffAdmin = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffAdmin.setGeometry(QtCore.QRect(1100, 10, 187, 41))
        self.LogOffAdmin.setObjectName(_fromUtf8("LogOffAdmin"))
        self.LogOffAdmin.clicked.connect(self.LogOffAdminfunc)

        #Student List
        self.StudentView = QtGui.QListWidget(MainWindow)
        self.StudentView.setGeometry(QtCore.QRect(10, 60, 450, 550))
        self.StudentView.setObjectName(_fromUtf8("StudentView"))
        self.StudentView.itemClicked.connect(self.handleViewDetail)

        #=================================================
        #Staff Window
        #Staff Labels
        self.StaffLabel_Name = QtGui.QLabel(MainWindow)
        self.StaffLabel_Name.setGeometry(QtCore.QRect(550, 60, 81, 31))
        self.StaffLabel_Name.setFont(font)
        self.StaffLabel_Name.setObjectName(_fromUtf8("StaffLabel_Name"))

        self.StaffLabel_ID = QtGui.QLabel(MainWindow)
        self.StaffLabel_ID.setGeometry(QtCore.QRect(550, 130, 81, 31))
        self.StaffLabel_ID.setFont(font)
        self.StaffLabel_ID.setObjectName(_fromUtf8("StaffLabel_ID"))

        self.StaffLabel_Email = QtGui.QLabel(MainWindow)
        self.StaffLabel_Email.setGeometry(QtCore.QRect(550, 200, 121, 31))
        self.StaffLabel_Email.setFont(font)
        self.StaffLabel_Email.setObjectName(_fromUtf8("StaffLabel_Email"))

        self.StaffLabel_Password = QtGui.QLabel(MainWindow)
        self.StaffLabel_Password.setGeometry(QtCore.QRect(550, 270, 81, 31))
        self.StaffLabel_Password.setFont(font)
        self.StaffLabel_Password.setObjectName(_fromUtf8("StaffLabel_Password"))

        self.StaffLabel_CPassword = QtGui.QLabel(MainWindow)
        self.StaffLabel_CPassword.setGeometry(QtCore.QRect(550, 340, 81, 31))
        self.StaffLabel_CPassword.setFont(font)
        self.StaffLabel_CPassword.setObjectName(_fromUtf8("StaffLabel_CPassword"))

        self.StaffLabel_SearchName = QtGui.QLabel(MainWindow)
        self.StaffLabel_SearchName.setGeometry(QtCore.QRect(10, 680, 91, 16))
        self.StaffLabel_SearchName.setObjectName(_fromUtf8("StaffLabel_SearchName"))
        self.StaffLabel_SearchName.setText(_translate("MainWindow", "Search Name", None))

        self.StaffLabel_SearchID = QtGui.QLabel(MainWindow)
        self.StaffLabel_SearchID.setGeometry(QtCore.QRect(310, 680, 91, 16))
        self.StaffLabel_SearchID.setObjectName(_fromUtf8("StaffLabel_SearchID"))
        self.StaffLabel_SearchID.setText(_translate("MainWindow", "Search ID", None))

        #Textfields
        self.StaffText_Name = QtGui.QLineEdit(MainWindow)
        self.StaffText_Name.setGeometry(QtCore.QRect(670, 60, 241, 31))
        self.StaffText_Name.setFont(font)
        self.StaffText_Name.setObjectName(_fromUtf8("StaffText_Name"))
        self.StaffText_Name.setValidator(azvalidator)

        self.StaffText_ID = QtGui.QLineEdit(MainWindow)
        self.StaffText_ID.setGeometry(QtCore.QRect(670, 130, 241, 31))
        self.StaffText_ID.setFont(font)
        self.StaffText_ID.setObjectName(_fromUtf8("StaffText_ID"))
        self.StaffText_ID.setValidator(intvalidator)

        self.StaffText_Email = QtGui.QLineEdit(MainWindow)
        self.StaffText_Email.setGeometry(QtCore.QRect(670, 200, 241, 31))
        self.StaffText_Email.setFont(font)
        self.StaffText_Email.setObjectName(_fromUtf8("StaffText_Email"))

        self.StaffText_Pass = QtGui.QLineEdit(MainWindow)
        self.StaffText_Pass.setGeometry(QtCore.QRect(670, 270, 241, 31))
        self.StaffText_Pass.setEchoMode(QtGui.QLineEdit.Password)
        self.StaffText_Pass.setFont(font)
        self.StaffText_Pass.setObjectName(_fromUtf8("StaffText_Pass"))

        self.StaffText_CPass = QtGui.QLineEdit(MainWindow)
        self.StaffText_CPass.setGeometry(QtCore.QRect(670, 340, 241, 31))
        self.StaffText_CPass.setEchoMode(QtGui.QLineEdit.Password)
        self.StaffText_CPass.setFont(font)
        self.StaffText_CPass.setObjectName(_fromUtf8("StaffText_CPass"))

        #Buttons
        self.StaffButton_Add = QtGui.QPushButton(MainWindow)
        self.StaffButton_Add.setGeometry(QtCore.QRect(120, 780, 91, 23))
        self.StaffButton_Add.setObjectName(_fromUtf8("StaffButton_Add"))
        self.StaffButton_Add.clicked.connect(self.AddStaffFunc)

        self.StaffButton_Edit = QtGui.QPushButton(MainWindow)
        self.StaffButton_Edit.setGeometry(QtCore.QRect(250, 780, 91, 23))
        self.StaffButton_Edit.setObjectName(_fromUtf8("StaffButton_Edit"))
        self.StaffButton_Edit.clicked.connect(self.EditstaffFunc)

        self.StaffButton_Remove = QtGui.QPushButton(MainWindow)
        self.StaffButton_Remove.setGeometry(QtCore.QRect(380, 780, 101, 23))
        self.StaffButton_Remove.setObjectName(_fromUtf8("StaffButton_Remove"))
        self.StaffButton_Remove.clicked.connect(self.RemoveStafffunc)

        self.StaffButton_Promote = QtGui.QPushButton(MainWindow)
        self.StaffButton_Promote.setGeometry(QtCore.QRect(520, 780, 101, 23))
        self.StaffButton_Promote.setObjectName(_fromUtf8("StaffButton_Promote"))
        self.StaffButton_Promote.clicked.connect(self.PromoteFunction)

        self.StaffButton_Exit = QtGui.QPushButton(MainWindow)
        self.StaffButton_Exit.setGeometry(QtCore.QRect(790, 780, 75, 23))
        self.StaffButton_Exit.setObjectName(_fromUtf8("StaffButton_Exit"))
        self.StaffButton_Exit.clicked.connect(self.CancelActionfunc)

        self.StaffButton_SaveAdd = QtGui.QPushButton(MainWindow)
        self.StaffButton_SaveAdd.setGeometry(QtCore.QRect(1000, 130, 75, 23))
        self.StaffButton_SaveAdd.setObjectName(_fromUtf8("StaffButton_SaveAdd"))
        self.StaffButton_SaveAdd.setText(_translate("MainWindow", "Save", None))
        self.StaffButton_SaveAdd.clicked.connect(self.handleAddStaffSave)

        self.StaffButton_SaveEdit = QtGui.QPushButton(MainWindow)
        self.StaffButton_SaveEdit.setGeometry(QtCore.QRect(1000, 130, 75, 23))
        self.StaffButton_SaveEdit.setObjectName(_fromUtf8("StaffButton_SaveEdit"))
        self.StaffButton_SaveEdit.setText(_translate("MainWindow", "Save", None))
        self.StaffButton_SaveEdit.clicked.connect(self.confirmsavestaff)

        self.StaffButton_Cancel = QtGui.QPushButton(MainWindow)
        self.StaffButton_Cancel.setGeometry(QtCore.QRect(1000, 200, 75, 23))
        self.StaffButton_Cancel.setObjectName(_fromUtf8("StaffButton_Cancel"))
        self.StaffButton_Cancel.setText(_translate("MainWindow", "Cancel", None))
        self.StaffButton_Cancel.clicked.connect(self.handleStaffCancel)

        #Searchfields
        self.StaffSearch_Name = QtGui.QLineEdit(MainWindow)
        self.StaffSearch_Name.setGeometry(QtCore.QRect(10, 700, 281, 31))
        self.StaffSearch_Name.setObjectName(_fromUtf8("StaffSearch_Name"))
        self.StaffSearch_Name.setValidator(azvalidator)

        self.StaffSearch_ID = QtGui.QLineEdit(MainWindow)
        self.StaffSearch_ID.setGeometry(QtCore.QRect(310, 700, 161, 31))
        self.StaffSearch_ID.setObjectName(_fromUtf8("StaffSearch_ID"))
        self.StaffSearch_ID.setValidator(intvalidator)

        self.StaffButton_SearchName = QtGui.QPushButton(MainWindow)
        self.StaffButton_SearchName.setGeometry(QtCore.QRect(10, 740, 121, 27))
        self.StaffButton_SearchName.setObjectName(_fromUtf8("StaffButton_SearchName"))
        self.StaffButton_SearchName.setText(_translate("MainWindow", "Search Name", None))

        self.StaffButton_SearchID = QtGui.QPushButton(MainWindow)
        self.StaffButton_SearchID.setGeometry(QtCore.QRect(310, 740, 121, 27))
        self.StaffButton_SearchID.setObjectName(_fromUtf8("StaffButton_SearchID"))
        self.StaffButton_SearchID.setText(_translate("MainWindow", "Search by ID", None))

        #stafflist
        self.StaffView = QtGui.QListWidget(MainWindow)
        self.StaffView.setGeometry(QtCore.QRect(10, 60, 450, 550))
        self.StaffView.setObjectName(_fromUtf8("StaffView"))
        self.StaffView.itemClicked.connect(self.handleViewDetailStaff)

        #logoffbutton
        self.LogOffAdmin_Staff = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffAdmin_Staff.setGeometry(QtCore.QRect(1100, 10, 187, 41))
        self.LogOffAdmin_Staff.setObjectName(_fromUtf8("LogOffAdmin_Staff"))
        self.LogOffAdmin_Staff.clicked.connect(self.LogOffAdminfunc)

        # =================================================
        self.workerThread = WorkerThread()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.workerThread.start()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

        #Double List View
        self.LeftListTitle.setText(_translate("MainWindow", "Lane 1", None))
        self.RightListTitle.setText(_translate("MainWindow", "Lane 2", None))
        self.LeftClear.setText(_translate("MainWindow", "Clear", None))
        self.RightClear.setText(_translate("MainWindow", "Clear", None))
        self.LeftStudentPicture.setText(_translate("MainWindow", "Picture Here", None))
        self.RightStudentPicture.setText(_translate("MainWindow", "Picture Here", None))

        #Login
        self.Username.setText(_translate("MainWindow", "Username", None))
        self.Password.setText(_translate("MainWindow", "Password", None))
        self.LoginButton.setText(_translate("MainWindow", "Login", None))
        self.LogOffAdmin1.setText(_translate("MainWindow", "Log Off Admin 1", None))
        self.LogOffStaff.setText(_translate("MainWindow", "Log Off Staff", None))

        #Log
        self.LogButton_Exit.setText(_translate("MainWindow", "Exit", None))
        self.LogButton_Generate.setText(_translate("Dismissal", "Generate", None))
        self.LogButton_Print.setText(_translate("Dismissal", "Print PDF", None))
        self.LogButton_Exit.setText(_translate("Dismissal", "Exit", None))
        self.LogLabel_Title.setText(_translate("Dismissal", "Dismissal Log", None))
        self.LogLabel_Start.setText(_translate("Dismissal", "Start Date", None))
        self.LogLabel_End.setText(_translate("Dismissal", "End Date", None))
        self.LogOffAdmin2.setText(_translate("Dismissal", "Log Off Admin 2", None))
        self.DismissWidget.setTabText(self.DismissWidget.indexOf(self.GenericTab), _translate("Dismissal", "Generic Report", None))
        self.LogStudentLabel_SearchName.setText(_translate("Dismissal", "Search Name:", None))
        self.LogStudentLogLabel_SearchID.setText(_translate("Dismissal", "Search ID:", None))
        self.LogStudentButton_SearchName.setText(_translate("Dismissal", "Search", None))
        self.LogStudentButton_SearchID.setText(_translate("Dismissal", "Search", None))
        self.DismissWidget.setTabText(self.DismissWidget.indexOf(self.StudentTab), _translate("Dismissal", "Student Report", None))
        self.LogStaffLabel_SearchName.setText(_translate("Dismissal", "Search Name:", None))
        self.LogStaffLabel_SearchID.setText(_translate("Dismissal", "Search ID:", None))
        self.LogStaffButton_SearchName.setText(_translate("Dismissal", "Search", None))
        self.LogStaffButton_SearchID.setText(_translate("Dismissal", "Search", None))
        self.DismissWidget.setTabText(self.DismissWidget.indexOf(self.StaffTab), _translate("Dismissal", "Staff Report", None))

        #mainadmin
        self.EditStudent.setText(_translate("MainWindow", "Edit Student", None))
        self.EditStaff.setText(_translate("MainWindow", "Edit Staff", None))
        self.StudentLog.setText(_translate("MainWindow", "Student Log", None))
        self.StudentCheckout.setText(_translate("MainWindow", "Student Checkout", None))
        self.adminlabel_welcome.setText(_translate("MainWindow", "Welcome to the Admin menu", None))
        self.adminlabel_student.setText(_translate("MainWindow", "Add/Remove/Delete Student", None))
        self.adminlabel_staff.setText(_translate("MainWindow", "Add/Remove/Delete Staff", None))
        self.adminlabel_log.setText(_translate("MainWindow", "Student log generator", None))
        self.adminlabel_checkout.setText(_translate("MainWindow", "Ordinary Checkout staff", None))

        # Student window
        self.StudentLabel_Grade.setText(_translate("MainWindow", "Grade Number:", None))
        self.StudentLabel_ID.setText(_translate("MainWindow", "Student ID:", None))
        self.StudentLabel_Picture_2.setText(_translate("MainWindow", "Picture", None))
        self.StudentLabel_SearchID.setText(_translate("MainWindow", "Search ID:", None))
        self.StudentButton_Remove.setText(_translate("MainWindow", "Remove Student", None))
        self.StudentButton_Exit.setText(_translate("MainWindow", "Exit", None))
        self.StudentButton_Edit.setText(_translate("MainWindow", "Edit Student", None))
        self.LogOffAdmin.setText(_translate("MainWindow", "Log Off Admin", None))
        self.StudentLabel_Name.setText(_translate("MainWindow", "Full Name:", None))
        self.StudentLabel_Picture.setText(_translate("MainWindow", "Picture:", None))
        self.StudentLabel_SearchName.setText(_translate("MainWindow", "Search Name:", None))
        self.StudentLabel_RFID.setText(_translate("MainWindow", "Tag ID:", None))
        self.StudentButton_Add.setText(_translate("MainWindow", "Add Student", None))
        self.StudentLabel_GName.setText(_translate("MainWindow", "Guardian:", None))
        self.StudentButton_SearchName.setText(_translate("MainWindow", "Search By Name", None))
        self.StudentButton_SearchName.clicked.connect(self.searchByName)
        self.StudentButton_SearchID.setText(_translate("MainWindow", "Search By ID", None))
        self.StudentButton_SearchID.clicked.connect(self.searchByID)
        self.StudentButton_Cancel.setText(_translate("Mainwindow", "Cancel", None))
        self.StudentButton_SaveAdd.setText(_translate("Mainwindow", "Save", None))
        self.StudentButton_SaveEdit.setText(_translate("Mainwindow", "Save", None))


        #staff Window
        self.StaffButton_Promote.setText(_translate("MainWindow", "Promote to Admin", None))
        self.StaffLabel_Email.setText(_translate("MainWindow", "Email:", None))
        self.StaffButton_Add.setText(_translate("MainWindow", "Add Staff", None))
        self.StaffButton_Remove.setText(_translate("MainWindow", "Remove Staff", None))
        self.StudentLabel_SearchName.setText(_translate("MainWindow", "Search Name:", None))
        self.LogOffAdmin_Staff.setText(_translate("MainWindow", "Log Off Admin Staff", None))
        self.StaffLabel_Name.setText(_translate("MainWindow", "Full Name:", None))
        self.StaffButton_Exit.setText(_translate("MainWindow", "Exit", None))
        self.StaffButton_Edit.setText(_translate("MainWindow", "Edit Staff", None))
        self.StaffLabel_Password.setText(_translate("MainWindow", "Password:", None))
        self.StaffLabel_CPassword.setText(_translate("MainWindow", "Re-Enter:", None))
        self.StaffLabel_ID.setText(_translate("MainWindow", "Staff ID:", None))

        self.StaffButton_SearchName.clicked.connect(self.searchByNameStaff)
        self.StaffButton_SearchID.clicked.connect(self.searchByIdStaff)
        self.hideall()
        self.showLogin()

    def AddStaffFunc(self):
        self.enableStaff()
        self.clearStaff()
        self.enableRightStaff()
        self.StaffText_ID.setEnabled(True)
        self.StaffText_Email.setEnabled(True)
        self.StaffButton_SaveEdit.hide()
        self.StaffButton_SaveAdd.show()

    def addStudentfunc(self,MainWindow):
        self.hideall()
        self.showStudentWindow()
        self.StudentButton_Cancel.show()
        self.StudentButton_SaveAdd.show()
        self.clearallfunction(MainWindow)
        self.enable()
        self.StudentButton_Cancel.setEnabled(True)
        self.StudentButton_SaveAdd.setEnabled(True)
        self.StudentText_Name.setEnabled(True)
        self.StudentText_RFID.setEnabled(True)
        self.StudentText_Grade.setEnabled(True)
        self.StudentText_GName.setEnabled(True)
        self.StudentText_ID.setEnabled(True)
        self.StudentText_Picture.setEnabled(True)
        self.StudentButton_Picture.setEnabled(True)
        self.StaffText_Pass.setEnabled(True)
        self.StaffText_CPass.setEnabled(True)
        self.StaffText_Email.setEnabled(True)

    def CancelActionfunc(self, MainWindow):
        self.hideall()
        self.showMainAdmin()
        ui.StudentView.clear()
        ui.StaffView.clear()

    def confirmsavestudent(self):
        checkduplicateid = int(self.StudentText_ID.text())
        duplicatecheck = Sys.searchByID(checkduplicateid)
        if (duplicatecheck != -1 and checkduplicateid != Sys.editstudentid):
            self.popupMessage2(MainWindow, "This id: " + str(checkduplicateid) + ", is already taken, please use another id.")
        else:
            if (self.popupMessage(MainWindow,"Do your really want to edit this student? ")):
                self.handleEditSaveStudent(MainWindow)

    def confirmsavestaff(self):
        password1 = self.StaffText_Pass.text()
        password2 = self.StaffText_CPass.text()
        if(password1 == password2):
            checkduplicateid = int(self.StaffText_ID.text())
            duplicatecheck = Sys.searchStaffIdNew(checkduplicateid)
            print ("dup: " + str(duplicatecheck))
            print ("old: " + str(Sys.editstaffid) + ", New: " + str(checkduplicateid))
            print(Sys.searchByEmail(self.StaffText_Email))
            if (duplicatecheck != -1 and checkduplicateid != Sys.editstaffid) :
                self.popupMessage2(MainWindow,"This id: " + str(checkduplicateid) + ", is already taken, please use another id.")
            elif(Sys.searchByEmail(self.StaffText_Email.text())):
                self.popupMessage2(MainWindow,
                                   "This email: " + self.StaffText_Email.text() + ", is already taken.")
            else:
                if (self.popupMessage(MainWindow,"Do your really want to edit this staff? ")):
                    self.handleEditSaveStaff(MainWindow)
                    self.enableLeftStaff()
        else:
            self.popupMessage2(MainWindow, "Password do not match. ")

    def clearStaff(self):
        self.StaffText_Name.clear()
        self.StaffText_ID.clear()
        self.StaffText_Pass.clear()
        self.StaffText_CPass.clear()
        self.StaffText_Email.clear()

    def clearallfunction(self,MainWindow):
        self.StudentText_Name.clear()
        self.StudentText_RFID.clear()
        self.StudentText_Grade.clear()
        self.StudentText_GName.clear()
        self.StudentText_ID.clear()
        self.StudentText_Picture.clear()
        self.StudentLabel_Picture_2.clear()

    def disableAll(self):
        #log
        #log all
        self.LogOffAdmin.setEnabled(False)
        self.LogOffAdmin2.setEnabled(False)
        self.LogButton_Exit.setEnabled(False)
        self.StartDateEdit.setEnabled(False)
        self.EndDateEdit.setEnabled(False)
        self.LogButton_Generate.setEnabled(False)
        self.LogButton_Print.setEnabled(False)
        self.DismissWidget.setEnabled(False)
        #log generic
        self.LogTableView_Generic.setEnabled(False)
        #log student
        self.LogListWidget_Student.setEnabled(False)
        self.LogTableView_Student.setEnabled(False)
        self.LogStudentText_SearchName.setEnabled(False)
        self.LogStudentText_SearchID.setEnabled(False)
        self.LogStudentButton_SearchName.setEnabled(False)
        self.LogStudentButton_SearchID.setEnabled(False)
        #log staff
        self.LogTableView_Staff.setEnabled(False)
        self.LogListWidget_Staff.setEnabled(False)
        self.LogStaffText_SearchName.setEnabled(False)
        self.LogStaffText_SearchID.setEnabled(False)
        self.LogStaffButton_SearchName.setEnabled(False)
        self.LogStaffButton_SearchID.setEnabled(False)

        #staff
        #staff textfields
        self.StaffText_Name.setEnabled(False)
        self.StaffText_ID.setEnabled(False)
        self.StaffText_Email.setEnabled(False)
        self.StaffText_Pass.setEnabled(False)
        self.StaffText_CPass.setEnabled(False)
        self.StaffSearch_Name.setEnabled(False)
        self.StaffSearch_ID.setEnabled(False)
        #staff buttons
        self.StaffButton_SearchName.setEnabled(False)
        self.StaffButton_SearchID.setEnabled(False)
        self.StaffButton_SaveAdd.setEnabled(False)
        self.StaffButton_SaveEdit.setEnabled(False)
        self.StaffButton_Cancel.setEnabled(False)
        self.StaffButton_Add.setEnabled(False)
        self.StaffButton_Edit.setEnabled(False)
        self.StaffButton_Remove.setEnabled(False)
        self.StaffButton_Promote.setEnabled(False)
        self.StaffButton_Exit.setEnabled(False)
        self.LogOffStaff.setEnabled(False)
        self.LogOffAdmin_Staff.setEnabled(False)
        #staff lists
        self.StaffView.setEnabled(False)

        #listview
        #listview buttons
        self.LeftClear.setEnabled(False)
        self.RightClear.setEnabled(False)
        #listview lists
        self.LeftList.setEnabled(False)
        self.RightList.setEnabled(False)

        #login
        self.LoginButton.setEnabled(False)
        self.Login_uname.setEnabled(False)
        self.Login_password.setEnabled(False)

        # hiding main admin page
        self.EditStudent.hide()
        self.EditStaff.hide()
        self.StudentLog.hide()
        self.EditStudent.hide()
        self.StudentLog.hide()
        self.LogOffAdmin1.hide()
        self.adminlabel_welcome.hide()
        self.adminlabel_student.hide()
        self.adminlabel_staff.hide()
        self.adminlabel_log.hide()
        self.adminlabel_checkout.hide()
        self.StudentCheckout.hide()

        #student
        #student textfields
        self.StudentText_Name.setEnabled(False)
        self.StudentText_ID.setEnabled(False)
        self.StudentText_Grade.setEnabled(False)
        self.StudentText_GName.setEnabled(False)
        self.StudentText_RFID.setEnabled(False)
        self.StudentSearch_Name.setEnabled(False)
        self.StudentSearch_ID.setEnabled(False)
        #student buttons
        self.StudentButton_SaveAdd.setEnabled(False)
        self.StudentButton_SaveEdit.setEnabled(False)
        self.StudentButton_SearchName.setEnabled(False)
        self.StudentButton_SearchID.setEnabled(False)
        self.StudentButton_Add.setEnabled(False)
        self.StudentButton_Edit.setEnabled(False)
        self.StudentButton_Remove.setEnabled(False)
        self.StudentButton_Exit.setEnabled(False)
        self.LogOffAdmin.setEnabled(False)
        #student lists
        self.StudentView.setEnabled(False)

    def editStudentfunc(self, MainWindow):
        self.hideall()
        self.showStudentWindow()
        self.StudentButton_Cancel.show()
        self.StudentButton_SaveEdit.show()
        self.enable()
        self.StudentButton_Cancel.setEnabled(True)
        self.StudentButton_SaveEdit.setEnabled(True)
        self.StudentText_Name.setEnabled(True)
        self.StudentText_RFID.setEnabled(True)
        self.StudentText_Grade.setEnabled(True)
        self.StudentText_GName.setEnabled(True)
        #getting student id that is being editted
        Sys.editstudentid = int(self.StudentText_ID.text())
        self.StudentText_ID.setEnabled(True)
        self.StudentText_Picture.setEnabled(True)
        self.StudentButton_Picture.setEnabled(True)

    def enableStaff(self):
        self.StaffButton_Add.setEnabled(False)
        self.StaffButton_Edit.setEnabled(False)
        self.StaffButton_Exit.setEnabled(False)
        self.StaffButton_Promote.setEnabled(False)
        self.StaffButton_Remove.setEnabled(False)
        self.StaffSearch_Name.setEnabled(False)
        self.StaffText_Pass.setEnabled(False)
        self.StaffText_CPass.setEnabled(False)
        self.StaffText_Email.setEnabled(False)
        self.StaffText_ID.setEnabled(False)
        self.StaffText_Name.setEnabled(False)
        self.StaffView.setEnabled(False)
        self.LogOffAdmin_Staff.setEnabled(False)
        self.StaffButton_SearchID.setEnabled(False)
        self.StaffButton_SearchName.setEnabled(False)
        self.StaffSearch_ID.setEnabled(False)
        self.StaffSearch_Name.setEnabled(False)

    def enable(self):
        self.StudentText_ID.setEnabled(False)
        self.StudentText_GName.setEnabled(False)
        self.StudentText_Grade.setEnabled(False)
        self.StudentText_Name.setEnabled(False)
        self.StudentText_RFID.setEnabled(False)
        self.StudentView.setEnabled(False)
        self.StudentButton_Exit.setEnabled(False)
        self.StudentText_Picture.setEnabled(False)

        self.StudentButton_Picture.setEnabled(False)
        self.StudentButton_SearchName.setEnabled(False)
        #self.StudentButton_ViewDetails.setEnabled(False)
        self.StudentButton_Add.setEnabled(False)
        self.StudentButton_Edit.setEnabled(False)
        self.StudentButton_Remove.setEnabled(False)
        self.StudentButton_SaveEdit.setEnabled(False)
        self.StudentButton_SaveAdd.setEnabled(False)
        self.StudentButton_SearchID.setEnabled(False)
        self.StudentButton_SearchName.setEnabled(False)
        self.LogOffAdmin.setEnabled(False)
        self.StudentSearch_Name.setEnabled(False)
        self.StudentSearch_ID.setEnabled(False)

    def enableListview(self):
        self.LeftClear.setEnabled(True)
        self.RightClear.setEnabled(True)
        self.LeftList.setEnabled(True)
        self.RightList.setEnabled(True)
        self.LogOffStaff.setEnabled(True)
        self.LeftClear.raise_()
        self.LeftList.raise_()
        self.RightClear.raise_()
        self.RightList.raise_()

    def enableLogin(self):
        self.LoginButton.setEnabled(True)
        self.Login_uname.setEnabled(True)
        self.Login_password.setEnabled(True)
        self.LoginButton.raise_()
        self.Login_uname.raise_()
        self.Login_password.raise_()

    def EditstaffFunc(self):
        Sys.editstaffid = int(self.StaffText_ID.text())
        Sys.editstaffemail = self.StaffText_Email.text()
        self.enableRightStaff()
        self.StaffButton_SaveEdit.show()
        self.StaffButton_Cancel.show()
        Sys.editstaffid = int(self.StaffText_ID.text())
        Sys.editstaffemail = self.StaffText_Email.text()

    def enableLeftStaff(self):
        self.enableStaff()
        self.StaffButton_Add.setEnabled(True)
        self.StaffButton_Edit.setEnabled(True)
        self.StaffButton_Exit.setEnabled(True)
        self.StaffButton_Promote.setEnabled(True)
        self.StaffButton_Remove.setEnabled(True)
        self.StaffLabel_Email.setEnabled(True)
        self.StaffLabel_ID.setEnabled(True)
        self.StaffLabel_Name.setEnabled(True)
        self.StaffLabel_Password.setEnabled(True)
        self.StaffLabel_CPassword.setEnabled(True)
        self.StaffSearch_Name.setEnabled(True)
        self.StaffText_Pass.setEnabled(False)
        self.StaffText_Pass.setEnabled(False)
        self.StaffText_Email.setEnabled(False)
        self.StaffText_ID.setEnabled(False)
        self.StaffText_Name.setEnabled(False)
        self.StaffView.setEnabled(True)
        self.LogOffAdmin_Staff.setEnabled(True)
        self.StaffLabel_SearchName.setEnabled(True)
        self.StaffLabel_SearchID.setEnabled(True)
        self.StaffButton_SearchID.setEnabled(True)
        self.StaffButton_SearchName.setEnabled(True)
        self.StaffSearch_ID.setEnabled(True)
        self.StaffSearch_Name.setEnabled(True)
        self.StaffButton_SaveEdit.hide()
        self.StaffButton_SaveAdd.hide()
        self.StaffButton_Cancel.hide()
        self.StaffLabel_CPassword.hide()
        self.StaffLabel_Password.hide()
        self.StaffText_CPass.hide()
        self.StaffText_Pass.hide()

    def enableRightStaff(self):
        self.enableStaff()
        self.StaffButton_SaveEdit.show()
        self.StaffButton_Cancel.show()
        self.StaffLabel_Password.show()
        self.StaffLabel_CPassword.show()
        self.StaffText_Name.setEnabled(True)
        self.StaffText_Email.setEnabled(True)
        self.StaffText_ID.setEnabled(True)
        self.StaffText_Pass.setEnabled(True)
        self.StaffText_CPass.setEnabled(True)
        self.StaffButton_SaveEdit.setEnabled(True)
        self.StaffButton_Cancel.setEnabled(True)
        self.StaffText_Pass.show()
        self.StaffText_CPass.show()
        self.StaffText_Pass.setText("")
        self.StaffText_CPass.clear()

    def handleBrowse(self):
        global filename
        filename = QtGui.QFileDialog.getOpenFileName()
        if filename != "":
            pixmap = QtGui.QPixmap(filename)
            pixmap = pixmap.scaled(510, 440, QtCore.Qt.KeepAspectRatio)
            self.StudentLabel_Picture_2.setPixmap(pixmap)
        MainWindow.setWindowState(MainWindow.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        # this will activate the window
        MainWindow.activateWindow()

    def handleViewDetailStaff(self):

        name = self.StaffSearch_Name.text()
        num = self.StaffView.currentRow()
        id = self.StaffSearch_ID.text()
        print(searchStaffStatus,"****")
        staff = []
        if(searchStaffStatus == 2):
            print("search id")
            if id == "":
                staff = Sys.staffList[num]

            else:
                result = Sys.searchByIdStaff(id)
                staff = result[num]

        else:
            if name == "":
                staff = Sys.staffList[num]
            else:
                result = Sys.searchByNameStaff(name)
                print(len(result))
                staff = result[num]

        self.StaffText_Email.setText(str(staff.Email))
        self.StaffText_ID.setText(str(staff.staffId))
        self.StaffText_Name.setText(staff.Name)
        print("Do nothing")
        print(os.getcwd())

    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_0 :
            self.close()

    def handleAddStaffSave(self, MainWindow):
        id = self.StaffText_ID.text()
        Email = self.StaffText_Email.text()
        name = self.StaffText_Name.text()
        password = self.StaffText_Pass.text()
        cpassword = self.StaffText_CPass.text()

        if (id == "" or Email == "" or name == "" or password == "" or cpassword == ""):
            print("One or more of the inputs is blank")
            self.popupMessage2(MainWindow, "Please fill in all the fields. ")
        else:
            if (password != cpassword):
                print(password + " " + cpassword)
                self.popupMessage2(MainWindow, "The passwords do not match, please try again. ")
                self.StaffText_CPass.setText("")
                self.StaffText_Pass.setText("")
            else:
                result = Sys.checkDuplicateIDStaff(id)
                if result:
                    self.popupMessage(MainWindow, "This staff id already exist.")
                if not result:
                    if (self.popupMessage(MainWindow, "Are you sure the information is correct? ")):
                        Sys.staffList.append(Staff(id, name, Email, password, 0))
                        Sys.addnewStaff(name, int(id), Email, password, 0)
                        self.searchByNameStaff()
                        print("Input validated")
                        print("Save1 Clicked")
                        self.enableLeftStaff()
                        self.clearallfunction(MainWindow)
                        self.StudentView.repaint()

    def handleviewLogStudent(self):
        conn = connectDB()
        cur = conn.cursor()
        name = self.LogStudentText_SearchName.text()
        num = self.LogListWidget_Student.currentRow()
        sDate = ui.StartDateEdit.date()
        eDate = ui.EndDateEdit.date()

        sDate = sDate.toPyDate()
        eDate = eDate.toPyDate()

        print(num)
        if name == "":
            student = Sys.studentList[num]
        else:
            result = Sys.searchByName(name)
            print(len(result))
            student = result[num]
        print(student.Name,"asd")
        cur.execute("SELECT * FROM LOG WHERE StudentID = "+ str(student.studentId))
        dataMain = cur.fetchall()

        data = {'Student ID': [], 'Staff ID': [], 'Date': [], 'Time': []}
        count = 0
        print(dataMain)
        for i in range(0, len(dataMain)):
            logDate = str(dataMain[i][2]).split(" ")[0]
            logDate = datetime.datetime.strptime(logDate, '%Y-%m-%d').date()
            difference = eDate - sDate
            print(difference)
            logdiff = logDate - sDate
            if((logdiff <= difference) and (logdiff >= datetime.timedelta(days=0))):
                count = count + 1
                print("Checks out!")
                print(difference)
                data['Student ID'].append(str(dataMain[i][1]))
                data['Staff ID'].append(str(dataMain[i][0]))
                data['Date'].append(str(logDate))
                data['Time'].append(str(dataMain[i][2]).split(" ")[1])
        ui.LogTableView_Student.setColumnCount(4)
        ui.LogTableView_Student.setRowCount(count)
        # LogTableView_Generic = QTableWidget(len(dataMain), 4)
        horHeaders = []
        for n, key in enumerate(sorted(data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QtGui.QTableWidgetItem(item)
                ui.LogTableView_Student.setItem(m, n, newitem)
            ui.LogTableView_Student.setHorizontalHeaderLabels(horHeaders)
            ui.LogTableView_Student.show()

    def handleviewLogStaff(self):
        conn = connectDB()
        cur = conn.cursor()
        name = self.LogStaffText_SearchName.text()
        num = self.LogListWidget_Staff.currentRow()
        sDate = ui.StartDateEdit.date()
        eDate = ui.EndDateEdit.date()

        sDate = sDate.toPyDate()
        eDate = eDate.toPyDate()

        print(num)
        if name == "":
            staff = Sys.staffList[num]
        else:
            result = Sys.searchByNameStaff(name)
            print(len(result))
            staff = result[num]
        cur.execute("SELECT * FROM LOG WHERE StaffID = " + str(staff.staffId))
        dataMain = cur.fetchall()

        data = {'Student ID': [], 'Staff ID': [], 'Date': [], 'Time': []}
        count = 0
        for i in range(0, len(dataMain)):
            logDate = str(dataMain[i][2]).split(" ")[0]
            logDate = datetime.datetime.strptime(logDate, '%Y-%m-%d').date()
            difference = eDate - sDate
            print(difference)
            logdiff = logDate - sDate
            if((logdiff <= difference) and (logdiff >= datetime.timedelta(days=0))):
                count = count + 1
                data['Student ID'].append(str(dataMain[i][1]))
                data['Staff ID'].append(str(dataMain[i][0]))
                data['Date'].append(str(dataMain[i][2]).split(" ")[0])
                data['Time'].append(str(dataMain[i][2]).split(" ")[1])
        ui.LogTableView_Staff.setColumnCount(4)
        ui.LogTableView_Staff.setRowCount(count)
        # LogTableView_Generic = QTableWidget(len(dataMain), 4)
        horHeaders = []
        for n, key in enumerate(sorted(data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                ui.LogTableView_Staff.setItem(m, n, newitem)
            ui.LogTableView_Staff.setHorizontalHeaderLabels(horHeaders)
            ui.LogTableView_Staff.show()

    def handleEditSaveStudent(self, MainWindow):

        id = self.StudentText_ID.text()
        grade = self.StudentText_Grade.text()
        rfid = self.StudentText_RFID.text()
        name = self.StudentText_Name.text()
        gname = self.StudentText_GName.text()
        pic = filename
        Sys.editStudent(id,grade,rfid,name,gname,pic)
        Ui_MainWindow.searchByName(self)

        self.enable()

        self.StudentView.setEnabled(True)
        self.StudentButton_Exit.setEnabled(True)

        self.StudentButton_SearchName.setEnabled(True)
        #self.StudentButton_ViewDetails.setEnabled(True)
        self.StudentButton_Add.setEnabled(True)
        self.StudentButton_Edit.setEnabled(True)
        self.StudentButton_Remove.setEnabled(True)
        self.StudentButton_SaveEdit.setEnabled(True)
        self.StudentButton_SaveAdd.setEnabled(True)
        self.StudentButton_SearchID.setEnabled(True)
        self.StudentButton_SearchName.setEnabled(True)
        self.LogOffAdmin.setEnabled(True)
        self.StudentSearch_Name.setEnabled(True)
        self.StudentSearch_ID.setEnabled(True)
        self.StudentButton_SaveEdit.hide()
        self.StudentButton_Cancel.hide()

    def handleEditSaveStaff(self, MainWindow):
        name = self.StaffText_Name.text()
        Email = self.StaffText_Email.text()
        id = self.StaffText_ID.text()
        password1 = self.StaffText_Pass.text()
        password2 = self.StaffText_CPass.text()
        for staff in(Sys.staffList):
            if(staff.Email == Email):
                oldPassword = staff.password
        if(password1 == password2 and password1==""):
            Sys.editStaff(name, Email, oldPassword, id)
        if password1 != password2 :
            self.popupMessage2(MainWindow, "Password do not match.")
        if(password1!="" and password1 == password2):
            Sys.editStaff(name, Email, password1, id)
            Ui_MainWindow.searchByName(self)

        self.enable()

        self.StudentView.setEnabled(True)
        self.StudentButton_Exit.setEnabled(True)
        self.StudentButton_SearchName.setEnabled(True)
        self.StudentButton_Add.setEnabled(True)
        self.StudentButton_Edit.setEnabled(True)
        self.StudentButton_Remove.setEnabled(True)
        self.StudentButton_SaveEdit.setEnabled(True)
        self.StudentButton_SaveAdd.setEnabled(True)
        self.StudentButton_SearchID.setEnabled(True)
        self.StudentButton_SearchName.setEnabled(True)
        self.LogOffAdmin.setEnabled(True)
        self.StudentSearch_Name.setEnabled(True)
        self.StudentSearch_ID.setEnabled(True)
        self.StudentButton_SaveEdit.hide()
        self.StudentButton_Cancel.hide()


        print("Save2 Clicked")

    def handleClearLeft(self):
        items = ui.LeftList.count()
        if (items == 0):
            self.popupMessage2(MainWindow, "Cannot remove that which is not there.")
            return
        rangedList = range(items)
        rangedList = rangedList.__reversed__()
        count = len(Sys.listL) - 1
        for i in rangedList:
            if ui.LeftList.isItemSelected(ui.LeftList.item(i)) == True:
                item = ui.LeftList.takeItem(i)
                break
            count = count - 1
        print(Sys.listL)
        if(Sys.listL[count] != -1):
            print("Calling Log with ID: " + str(Sys.listL[count]))
            Sys.logEntry(Sys.listL[count])
            del Sys.listL[count]
        else:
            del Sys.listL[count]
        #reset picture to first student in queue
        if (len(ui.LeftList) > 0):
            self.LeftStudentPicture.setPixmap(self.listItemToPicture(self.LeftList.item(0).text()))
        # remove picture if list is empty
        else:
            #doesn't clear picture need an empty picture
            ui.RightStudentPicture.setText("")

    def handleClearRight(self):
        items = ui.RightList.count()
        if (items == 0):
            self.popupMessage2(MainWindow, "Cannot remove that which is not there.")
            return
        rangedList = range(items)
        rangedList = rangedList.__reversed__()
        for i in rangedList:
            if ui.RightList.isItemSelected(ui.RightList.item(i)) == True:
                ui.RightList.takeItem(i)
                break
        #reset picture to next student
        if (len(ui.RightList) > 0):
            self.RightStudentPicture.setPixmap(self.listItemToPicture(self.RightList.item(0).text()))
        #remove picture if list is empty
        else:
            ui.RightStudentPicture.setText("")

    def handleViewDetail(self):
        picpath = "../pictures/"
        # item = self.StudentView.currentItem().text()
        # print(item)
        name = self.StudentSearch_Name.text()
        num = self.StudentView.currentRow()
        id = self.StudentSearch_ID.text()
        student =[]
        print(num)
        if searchStudentStatus == 2:
            if id =="":
                student = Sys.studentList[num]
            else:
                student = Sys.searchByID(id)
                student = student[num]
        else:
            if name == "":
                student = Sys.studentList[num]
            else:
                result = Sys.searchByName(name)
                print(len(result))
                student = result[num]

        self.StudentText_GName.setText(student.guardian)
        self.StudentText_Grade.setText(str(student.grade))
        self.StudentText_ID.setText(str(student.studentId))
        self.StudentText_Name.setText(student.Name)
        pixmap = QtGui.QPixmap(student.image)
        pixmap = pixmap.scaled(510,440,QtCore.Qt.KeepAspectRatio)
        #self.StudentLabel_Picture_2.setPixmap(QtGui.QPixmap(os.getcwd() + picpath + "student1.jpg"))
        self.StudentLabel_Picture_2.setPixmap(pixmap)
        #self.StudentLabel_Picture_2.setText("aaa")
        #QtCoreApplication::processEvents()
        self.StudentText_RFID.setText(student.tagId)
        print("Do nothing")
        print(os.getcwd())

    def handleAddSave(self, MainWindow):
        global filename
        print(filename,"this this")
        temp = filename.split("/")
        temp = temp[-1]
        print(temp)
        destination = "C:/Users/SeniorDesign/Documents/GitHub/Senior-Design/pictures/"
        pic = destination +"/"+ temp
        print("pp"+pic)


        id = self.StudentText_ID.text()
        grade = self.StudentText_Grade.text()
        rfid = self.StudentText_RFID.text()
        name = self.StudentText_Name.text()
        gname = self.StudentText_GName.text()


        if(id == "" or grade == "" or rfid == "" or name == "" or gname == ""):
            print("One of the inputs is blank")
            self.popupMessage2(MainWindow, "Please fill in all the fields. ")

        else:
            result = Sys.checkDuplicateID(id)
            if result:
                self.popupMessage(MainWindow,"This student id already exist.")
            if not result:
                if (self.popupMessage(MainWindow, "Are you sure the information is correct? ")):
                    if (filename == destination):
                        print("File already exists")
                    else:
                        shutil.copy(filename, destination)
                    Sys.studentList.append(Student(name,int(id),rfid,gname,pic,int(grade)))
                    Sys.addnewStudent(name,int(id),rfid,gname,pic,int(grade))
                    self.searchByName()
                    print("Input validated")
                    print("Save1 Clicked")
                    self.enable()
                    self.StudentView.setEnabled(True)
                    self.StudentButton_Exit.setEnabled(True)

                    self.StudentButton_SearchName.setEnabled(True)
                    #self.StudentButton_ViewDetails.setEnabled(True)
                    self.StudentButton_Add.setEnabled(True)
                    self.StudentButton_Edit.setEnabled(True)
                    self.StudentButton_Remove.setEnabled(True)
                    self.StudentButton_SaveEdit.setEnabled(True)
                    self.StudentButton_SaveAdd.setEnabled(True)
                    self.StudentButton_SearchID.setEnabled(True)
                    self.StudentButton_SearchName.setEnabled(True)
                    self.LogOffAdmin.setEnabled(True)
                    self.StudentSearch_Name.setEnabled(True)
                    self.StudentSearch_ID.setEnabled(True)

                    self.clearallfunction(MainWindow)
                    self.StudentView.repaint()

        # confirmation=QMessage()
        # confirmation.exec()
        #

    def handleAddCancel(self, MainWindow):
        self.StudentButton_SaveAdd.hide()
        self.StudentButton_Cancel.hide()
        self.StudentButton_SaveEdit.hide()
        self.clearallfunction(MainWindow)
        self.enable()
        Sys.editstudentid = -1
        self.StudentView.setEnabled(True)
        self.StudentButton_Exit.setEnabled(True)

        self.StudentButton_SearchName.setEnabled(True)
        #self.StudentButton_ViewDetails.setEnabled(True)
        self.StudentButton_Add.setEnabled(True)
        self.StudentButton_Edit.setEnabled(True)
        self.StudentButton_Remove.setEnabled(True)
        self.StudentButton_SaveEdit.setEnabled(True)
        self.StudentButton_SaveAdd.setEnabled(True)
        self.StudentButton_SearchID.setEnabled(True)
        self.StudentButton_SearchName.setEnabled(True)
        self.LogOffAdmin.setEnabled(True)
        self.StudentSearch_Name.setEnabled(True)
        self.StudentSearch_ID.setEnabled(True)

    def handleStaffCancel(self):
        self.clearStaff()
        self.enableLeftStaff()
        Sys.editstaffid = -1
        Sys.editstaffemail = ""

    def hideall(self):
        #comment out to make things work again
        #self.disableAll()
        #log hide
        self.LoginTitle.hide()
        self.LogButton_Exit.hide()
        self.LogButton_Generate.hide()
        self.LogButton_Print.hide()
        self.LogButton_Exit.hide()
        self.Login_uname.hide()
        self.LoginButton.hide()
        self.LogLabel_End.hide()
        self.LogLabel_Start.hide()
        self.LogTableView_Staff.hide()
        self.LogListWidget_Staff.hide()
        self.LogListWidget_Student.hide()
        self.LogTableView_Student.hide()
        self.LogTableView_Generic.hide()
        #self.LogStudentButton_SearchID.hide()
        self.LogStudentButton_SearchName.hide()
        self.LogStudentLabel_SearchName.hide()
        self.LogStudentLogLabel_SearchID.hide()
        self.LogStudentText_SearchID.hide()
        self.LogStudentText_SearchName.hide()
        self.LogStaffButton_SearchID.hide()
        self.LogStaffButton_SearchName.hide()
        self.LogStaffLabel_SearchName.hide()
        #self.LogStaffLogLabel_SearchID.hide()
        self.LogStaffText_SearchID.hide()
        self.LogStaffText_SearchName.hide()
        self.LogStaffLabel_SearchID.hide()
        self.LogStaffButton_SearchID.hide()
        self.LogStaffButton_SearchName.hide()
        self.LogTableView_Generic.hide()
        self.LogTableView_Student.hide()
        self.LogStudentButton_SearchID.hide()
        self.DismissWidget.hide()
        self.LogOffAdmin2.hide()
        self.StartDateEdit.hide()
        self.EndDateEdit.hide()
        self.LogLabel_Title.hide()
        self.LogListWidget_Staff.hide()
        self.LogOffAdmin.hide()
        self.LogOffStaff.hide()
        self.LogStaffButton_SearchID.hide()
        self.LoginTitle.hide()


        #staff hide

        self.StaffLabel_SearchName.hide()
        self.StaffLabel_SearchID.hide()
        self.StaffButton_SearchID.hide()
        self.StaffButton_SearchName.hide()
        self.StaffButton_SaveAdd.hide()
        self.StaffButton_SaveEdit.hide()
        self.StaffButton_Cancel.hide()
        self.StaffSearch_ID.hide()
        self.StaffSearch_Name.hide()
        self.LogOffStaff.hide()

        #listview hide
        self.LeftListTitle.hide()
        self.RightListTitle.hide()
        self.LeftClear.hide()
        self.RightClear.hide()
        self.LeftList.hide()
        self.RightList.hide()
        self.LeftStudentPicture.hide()
        self.RightStudentPicture.hide()
        self.SplittingLine.hide()

        #login hide
        self.Username.hide()
        self.Password.hide()
        self.LoginButton.hide()
        self.LoginTitle.hide()
        self.Login_uname.hide()
        self.Login_uname.clear()
        self.Login_password.hide()
        self.Login_password.clear()

        #hiding main admin page
        self.EditStudent.hide()
        self.EditStaff.hide()
        self.StudentLog.hide()
        self.EditStudent.hide()
        self.StudentLog.hide()
        self.LogOffAdmin1.hide()
        self.adminlabel_welcome.hide()
        self.adminlabel_student.hide()
        self.adminlabel_staff.hide()
        self.adminlabel_log.hide()
        self.adminlabel_checkout.hide()
        self.StudentCheckout.hide()

        #hide all student window
        self.StudentButton_Picture.hide()
        self.StudentLabel_Grade.hide()
        self.StudentLabel_ID.hide()
        self.StudentLabel_Picture_2.hide()
        self.StudentLabel_SearchID.hide()
        self.StudentButton_Remove.hide()
        self.StudentButton_Exit.hide()
        self.StudentButton_Edit.hide()
        self.LogOffAdmin.hide()
        self.StudentLabel_Name.hide()
        self.StudentLabel_Picture.hide()
        self.StudentLabel_SearchName.hide()
        self.StudentLabel_RFID.hide()
        self.StudentButton_Add.hide()
        self.StudentLabel_GName.hide()
        self.StudentText_GName.hide()
        self.StudentText_Grade.hide()
        self.StudentText_ID.hide()
        self.StudentText_Name.hide()
        self.StudentText_Picture.hide()
        self.StudentText_RFID.hide()
        self.StudentSearch_ID.hide()
        self.StudentSearch_Name.hide()
        self.StudentButton_SearchID.hide()
        self.StudentSearch_Name.hide()
        self.StudentView.hide()
        self.StudentView.clear()

        #hide all staff window
        self.StaffButton_Add.hide()
        self.StaffButton_Edit.hide()
        self.StaffButton_Exit.hide()
        self.StaffButton_Promote.hide()
        self.StaffButton_Remove.hide()
        self.StaffLabel_Email.hide()
        self.StaffLabel_ID.hide()
        self.StaffLabel_Name.hide()
        self.StaffLabel_Password.hide()
        self.StaffLabel_CPassword.hide()
        self.StaffSearch_Name.hide()
        self.StaffText_Pass.hide()
        self.StaffText_CPass.hide()
        self.StaffText_Email.hide()
        self.StaffText_ID.hide()
        self.StaffText_Name.hide()
        self.StaffView.hide()
        self.LogOffAdmin_Staff.hide()
        self.StudentButton_SearchName.hide()
        self.StudentButton_SaveAdd.hide()
        self.StudentButton_Cancel.hide()
        self.StudentButton_SaveEdit.hide()

    def listItemToPicture(self, item):
        try:
            picture = Sys.searchByName(item)[0].image
        except IndexError:
            picture = ""
        print(picture)
        pixmap = QtGui.QPixmap(picture)
        return pixmap.scaled(180, 170, QtCore.Qt.KeepAspectRatio)

    def LogOffAdminfunc(self, MainWindow):
        #when Admin Login is clicked is clicked
        self.hideall()
        self.showLogin()

    def LogAdminfunc(self, MainWindow):
        self.hideall()
        self.showLog()

    def LogOffStafffunc(self, MainWindow):
        #when Admin Login is clicked is clicked
        self.hideall()
        self.showLogin()

    def MainAdminfunc(self, MainWindow):
        # when Admin Login is clicked is clicked
        global currentUser
        try:
            conn = connectDB()
            cur = conn.cursor()
            userpassword = str(self.Login_password.text())
            username = self.Login_uname.text()
            currentUser = username
            temp = cur.execute("Select * FROM staff WHERE Email = %s", username)
            if temp == 0:
                print("Invalid Username")
            else:
                check = cur.fetchone()
                password = check[2]
                isAdmin = check[4]
                if (password == userpassword):
                    if (isAdmin == 1):
                        self.hideall()
                        self.showMainAdmin()
                        print("Show Admin Page")
                    elif (isAdmin == 0):
                        self.hideall()
                        self.showMain()

                        print("Show Staff Page")
                else:
                    print("Show Incorrect Password message!")
            conn.close()
        except:
            print("db error")
            password = str(self.Login_password.text())
            if (password == "a"):
                self.hideall()
                self.showMainAdmin()
                print("Show Admin Page")
            elif (password == "s"):
                self.hideall()
                self.showMain()
                print("Show staff Page")

    def newOnKeyPressEvent(self, event):
        if (((event.key() == QtCore.Qt.Key_Enter) or (event.key() == QtCore.Qt.Key_Return)) and (
        self.LoginButton.isEnabled())):
            print("enter ")
            self.MainAdminfunc(MainWindow)
        if (event.key() == QtCore.Qt.Key_1):
            print("Pressed 1 Idiot :)")
        if (event.key() == QtCore.Qt.Key_E):
            print("IM NOT LISTENING")
        if ((event.key() == QtCore.Qt.Key_1) and (self.LeftClear.isEnabled())):
            print("Clearing Left Side")
            self.handleClearLeft()
        if ((event.key() == QtCore.Qt.Key_2) and (self.RightClear.isEnabled())):
            print("Clearing Right Side")
            self.handleClearRight()

    def PromoteFunction (self):
        print('this')
        global Sys
        id = self.StaffText_ID.text()
        if(Sys.promoteStaff(id)):
            self.popupMessage2(MainWindow, self.StaffText_Name.text() + " is already an admin.")
        else:
            print("Not admin----")
            if(self.popupMessage(MainWindow, "Are you sure you want to promote " + self.StaffText_Name.text() + " to an admin?")):
                query = "UPDATE staff  SET isAdmin=1  WHERE StaffID=%s;"
                query2 = (id)
                conn = connectDB()
                cur = conn.cursor()
                addq = cur.execute(query, query2)
                conn.commit()
                conn.close()
                print("admin updated")
                print(Sys.staffList[1].Name)
                for i in range(0,len( Sys.staffList)):
                    print(i)
                    if(Sys.staffList[i].staffId == id):

                        Sys.staffList[i].isAdmin = 1
                        break
                self.searchByNameStaff("")
                print(Sys.staffList[2].isAdmin, "kjkkkkkkkkkkkkkkkkkkkk")
            else:
                print("admin canceled")

    def popupMessage(self, MainWindow,StringText):
        PopupMessage = QtGui.QMessageBox()
        PopupMessage.setWindowTitle("Confirmation")
        PopupMessage.setIcon(4)
        PopupMessage.setText(StringText)
        PopupMessage.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        result = PopupMessage.exec()
        print(result)
        if result==4194304:
            return False
        else:
            return True

    def popupMessage2(self, MainWindow, StringText):
            PopupMessage2 = QtGui.QMessageBox()
            PopupMessage2.setWindowTitle("Confirmation")
            PopupMessage2.setIcon(4)
            PopupMessage2.setText(StringText)
            PopupMessage2.setStandardButtons(QtGui.QMessageBox.Ok )
            result = PopupMessage2.exec()
            print(result)

    def PrintPDF(self):
        print("print")

    def redrawTables(self):
        print("Generate Clicked")
        self.handleviewLogStudent()
        self.handleviewLogStaff()
        Sys.showLogData()

    def RemoveStudentfunc(self, name):
        name =  self.StudentText_Name.text()
        id = self.StudentText_ID.text()
        print(name)
        if(self.popupMessage(MainWindow,"Do you really want to delete " + name + " from the database ?")):
            Sys.removeStudent(id)
            query = "DELETE FROM student WHERE StudentID= %s;"
            query2 = (id)
            conn = connectDB()
            cur = conn.cursor()
            addq = cur.execute(query, query2)
            self.clearallfunction(MainWindow)
            conn.commit()
            conn.close()
            self.searchByName()

    def RemoveStafffunc(self, name):
        name =  self.StaffText_Name.text()
        id = self.StaffText_ID.text()
        Email = self.StaffText_Email.text()
        if(Email == currentUser):
            self.popupMessage2(MainWindow, "Admins are not allowed to remove themselves. \nPlease get another admin to remove you. ")
        else:
            if(self.popupMessage(MainWindow,"Do you really want to delete " + name + " from the database ?")):
                print(str(id) + name + str(currentUser))
                if(Sys.removeStaff(id, currentUser)):
                    query = "DELETE FROM staff WHERE StaffID= %s;"
                    query2 = (id)
                    conn = connectDB()
                    cur = conn.cursor()
                    addq = cur.execute(query, query2)
                    self.clearallfunction(MainWindow)
                    conn.commit()
                    conn.close()
                else:
                    self.popupMessage2(MainWindow,"Admins are not allowed to remove themselves. Please get another admin to remove you. ")

    def searchIDStudentLog(self):
        result = []
        print("by id")
        id = self.LogStudentText_SearchID.text()
        result = Sys.searchByID(id)
        ui.LogListWidget_Student.clear()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i].Name)
            ui.LogListWidget_Student.addItem(item)

    def searchNameStaffLog(self):
        result = []
        name = self.LogStaffText_SearchName.text()

        result = Sys.searchByNameStaff(name)
        ui.LogListWidget_Staff.clear()
        if len(result) == 0:
            result = Sys.staffList
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i].Name)
            ui.LogListWidget_Staff.addItem(item)

    def searchIDStaffLog(self):
        result = []
        id = self.LogStaffText_SearchID.text()
        if id == "":
            result = Sys.staffList
        else:
            result = Sys.searchByIdStaff(id)
        ui.LogListWidget_Staff.clear()

        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i].Name)
            ui.LogListWidget_Staff.addItem(item)

    def searchByName(self):
        global searchStudentStatus
        searchStaffStatus = 1

        name = self.StudentSearch_Name.text()
        result = Sys.searchByName(name)
        print(result)
        ui.StudentView.clear()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i].Name)
            ui.StudentView.addItem(item)
        self.StudentView.show()

    def searchByNameStaff(self):
        global searchStaffStatus
        searchStaffStatus = 1

        name = self.StaffSearch_Name.text()
        result = Sys.searchByNameStaff(name)
        ui.StaffView.clear()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i].Name)
            ui.StaffView.addItem(item)
        self.StaffView.show()

    def searchByIdStaff(self):
        global searchStaffStatus
        searchStaffStatus = 2

        id = self.StaffSearch_ID.text()
        if id == "":
            result = Sys.staffList
        else:
            result = Sys.searchByIdStaff(id)
        ui.StaffView.clear()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i].Name)
            ui.StaffView.addItem(item)
        self.enableLeftStaff()
        self.StaffView.show()

    def searchByID(self):
        global searchStudentStatus
        searchStudentStatus = 2

        id = self.StudentSearch_ID.text()

        if id == "":
            result = Sys.studentList
        else:
            result = Sys.searchByID(id)
        ui.StudentView.clear()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i].Name)
            ui.StudentView.addItem(item)
        self.StudentView.show()

    def showStaffWindow(self):
        self.enableLeftStaff()
        self.StaffButton_Add.show()
        self.StaffButton_Edit.show()
        self.StaffButton_Exit.show()
        self.StaffButton_Promote.show()
        self.StaffButton_Remove.show()
        self.StaffLabel_Email.show()
        self.StaffLabel_ID.show()
        self.StaffLabel_Name.show()
        self.StaffLabel_Password.show()
        self.StaffLabel_CPassword.show()
        self.StaffSearch_Name.show()
        self.StaffText_Pass.show()
        self.StaffText_CPass.show()
        self.StaffText_Email.show()
        self.StaffText_ID.show()
        self.StaffText_Name.show()
        result = Sys.getStaffNames()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i])
            ui.StaffView.addItem(item)
        self.StaffView.show()
        self.LogOffAdmin_Staff.show()
        self.StaffLabel_SearchName.show()
        self.StaffLabel_SearchID.show()
        self.StaffButton_SearchID.show()
        self.StaffButton_SearchName.show()
        self.StaffSearch_ID.show()
        self.StaffSearch_Name.show()

    def ShowStudentLogFunc(self):
        self.hideall()
        self.LogButton_Exit.show()
        self.LogButton_Generate.show()
        self.LogButton_Print.show()
        self.LogLabel_End.show()
        self.LogLabel_Start.show()
        self.LogTableView_Staff.show()
        self.LogListWidget_Staff.show()
        self.LogListWidget_Student.show()
        self.LogTableView_Student.show()
        self.LogTableView_Generic.show()
        self.LogStudentButton_SearchName.show()
        self.LogStudentLabel_SearchName.show()
        self.LogStudentLogLabel_SearchID.show()
        self.LogStudentText_SearchID.show()
        self.LogStudentText_SearchName.show()
        self.LogStaffButton_SearchID.show()
        self.LogStaffButton_SearchName.show()
        self.LogStaffLabel_SearchName.show()
        self.LogStaffText_SearchID.show()
        self.LogStaffText_SearchName.show()
        self.LogStaffLabel_SearchID.show()
        self.LogStaffButton_SearchID.show()
        self.LogStaffButton_SearchName.show()
        self.LogTableView_Generic.show()
        self.LogTableView_Student.show()
        self.LogStudentButton_SearchID.show()
        self.DismissWidget.show()
        self.LogOffAdmin2.show()
        self.StartDateEdit.show()
        self.EndDateEdit.show()
        self.LogLabel_Title.show()
        self.LogListWidget_Staff.show()
        self.LogStaffButton_SearchID.show()
        Sys.showLogData()

    def searchNameStudentLog(self):
        print("A")
        result = []

        print(sDate, eDate)
        name = str(self.LogStudentText_SearchName.text())
        result = Sys.searchByName(name)
        print(result)
        ui.LogListWidget_Student.clear()

        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i].Name)
            ui.LogListWidget_Student.addItem(item)
        ui.LogListWidget_Student.show()

    def showStudentWindow(self):
        self.StudentButton_SearchName.show()
        self.StudentLabel_Grade.show()
        self.StudentLabel_ID.show()
        self.StudentLabel_Picture_2.show()
        self.StudentLabel_SearchID.show()
        self.StudentButton_Remove.show()
        self.StudentButton_Exit.show()
        self.StudentButton_Edit.show()
        self.LogOffAdmin.show()
        self.StudentLabel_Name.show()
        self.StudentLabel_Picture.show()
        # self.StudentLabel_SearchName.show()
        self.StudentLabel_RFID.show()
        self.StudentButton_Add.show()
        self.StudentLabel_GName.show()
        self.StudentText_GName.show()
        self.StudentText_Grade.show()
        self.StudentText_ID.show()
        self.StudentButton_SearchID.show()
        self.StudentView.show()
        self.StudentSearch_Name.show()
        self.StudentButton_Exit.show()
        self.StudentText_Name.show()
        self.StudentText_Picture.hide()
        self.StudentButton_Picture.show()
        self.StudentText_RFID.show()
        self.StudentLabel_SearchName.show()

        result = Sys.getStudentNames()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i])
            ui.StudentView.addItem(item)

        self.StudentView.show()
        self.StudentSearch_ID.show()
        self.StudentSearch_Name.show()

    def showLog(self):
        self.LogButton_Exit.show()
        self.LogOffAdminStudent.show()

    def showMain(self):
        self.hideall()
        self.enableListview()
        #show main application
        self.LeftListTitle.show()
        self.RightListTitle.show()
        self.LeftClear.show()
        self.RightClear.show()
        self.LeftList.show()
        self.RightList.show()
        self.LeftStudentPicture.show()
        self.RightStudentPicture.show()
        self.SplittingLine.show()
        self.LogOffStaff.show()

    def showMainAdmin(self):
        #show admin page
        self.EditStudent.show()
        self.EditStaff.show()
        self.StudentLog.show()
        self.LogOffAdmin1.show()
        self.StudentCheckout.show()

        self.adminlabel_welcome.show()
        self.adminlabel_student.show()
        self.adminlabel_staff.show()
        self.adminlabel_log.show()
        self.adminlabel_checkout.show()

        self.EditStudent.raise_()
        self.EditStaff.raise_()
        self.StudentLog.raise_()
        self.LogOffAdmin1.raise_()
        self.StudentCheckout.raise_()

    def showLogin(self):
        self.enableLogin()
        self.Username.show()
        self.Password.show()
        self.LoginButton.show()
        self.LoginTitle.show()
        self.Login_uname.show()
        self.Login_password.show()

    def ShowAdminFunc(self, MainWindow):
        self.hideall()
        self.showStudentWindow()
        self.StudentButton_Picture.setEnabled(False)

    def ShowStaffWindonFunc(self,MainWindow):
        self.hideall()
        self.showStaffWindow()
        self.enableLeftStaff()

    def tabControl(self):
        self.redrawTables()
        #get current index of dismiss widget
        #tab control needs to save variable
        #new function printPDF reads from that variable for the switch case to print the data that is currently shown

    def updateLeftPicture(self):
        self.LeftStudentPicture.setPixmap(self.listItemToPicture(self.LeftList.currentItem().text()))

    def updateRightPicture(self):
        self.RightStudentPicture.setPixmap(self.listItemToPicture(self.RightList.currentItem().text()))

class WorkerThread(QThread):
    def __init__(self, parent = None):
        super(WorkerThread, self).__init__(parent)

    def run(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server Log: " + socket.gethostname())
        print("\n")
        serverSocket.bind(('localhost', 8086))
        serverSocket.listen(5)
        threads = []
        while True:
            (clientsocket, address) = serverSocket.accept()
            clientsocket.settimeout(60)
            try:
                t = threading.Thread(target=client_thread, args=(clientsocket,))
                threads.append(t)
                t.start()
            except:
                print("Just keep ignoring it all.")
                continue
        serverSocket.close()

def client_thread(clientsocket):
    message = clientsocket.recv(2048)
    rfid = message.decode("utf-8")
    result = search_query(rfid[2:])
    if result != -1:
        (temp, temppic) = result
    else:
        # to do change empty string with unidentified user picture
        (temp, temppic) = ("Not Found!", "")
    # (temp, temppic) = search_query(rfid[2:])
    if(rfid[0:2] == "R1"):
        res = Sys.lookUpRfid(rfid[2:])
        if res != -1:
            Sys.listL.append(res.studentId)
        else:
            Sys.listL.append(res)
        item = QtGui.QListWidgetItem(temp)
        ui.LeftList.addItem(item)
        if (len(ui.LeftList) == 1):
            pixmapL = QtGui.QPixmap(temppic)
            pixmapL = pixmapL.scaled(180, 170, QtCore.Qt.KeepAspectRatio)
            ui.LeftStudentPicture.setPixmap(pixmapL)

    elif(rfid[0:2] == "R2"):
        res = Sys.lookUpRfid(rfid[2:])
        if res != -1:
            Sys.listR.append(res.studentId)
        else:
            Sys.listR.append(res)
        item = QtGui.QListWidgetItem(temp)
        ui.RightList.addItem(item)
        if (len(ui.RightList) == 1):
            pixmapR = QtGui.QPixmap(temppic)
            pixmapR = pixmapR.scaled(180, 170, QtCore.Qt.KeepAspectRatio)
            ui.RightStudentPicture.setPixmap(pixmapR)
    MainWindow.update()
    clientsocket.close()
    print("Thread Complete")

def search_query(rfid):
    result = Sys.lookUpRfid(rfid)
    if result != -1:
        return (result.Name, result.image)
    else:
        return result

app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

"""
Comment Type 1
"""

## Comment Type 2

if __name__ == "__main__":
    MainWindow.show()
    Sys = System()
    global listR
    listR = []
    global listL
    listL = []
    print("I am awesome!")
    sys.exit(app.exec_())
	

