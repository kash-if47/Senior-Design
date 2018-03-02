import socket
import threading
import glob
import shutil
import os
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QThread
import pymysql

filename = ""

def connectDB():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='rfid1234', db='rfid')
    # cur = conn.cursor()
    return conn

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

    def __init__(self):
        try:
            conn = connectDB()
            cur = conn.cursor()
            temp = cur.execute("SELECT * FROM student")
            data = cur.fetchall()
            for i in range(0, len(data)):
                Name = data[i][0]
                tagId = data[i][1]
                studentId = data[i][2]
                guardian = data[i][3]
                grade = data[i][4]
                pic = data[i][5]
                student = Student(Name, studentId, tagId, guardian, pic,grade)
                self.studentList.append(student)
            temp = cur.execute("SELECT * FROM staff")
            data2 = cur.fetchall()
            for i in range(0, len(data2)):
                fName = data2[i][0]
                email = data2[i][1]
                password = data2[i][2]
                staffId = data2[i][3]
                isAdmin = data2[i][4]
                staff = Staff(staffId, fName, email, password, isAdmin)
                self.staffList.append(staff)
        except:
            print("db error HEHE")

    def redraw(self):
        self.searchByName("")

    def getStudentNames(self):
        result = []
        for i in range(0, len(self.studentList)):
            name = self.studentList[i].Name
            result.append(name)
        return result

    def getStaffNames(self):
        result = []
        for i in range(0, len(self.staffList)):
            name = self.staffList[i].Name
            result.append(name)
        return result

    def searchByName(self, name):
        result = []
        for i in range(0, len(self.studentList)):
            fullName = self.studentList[i].Name
            if name in fullName:
                print("found " + fullName)
                result.append(self.studentList[i])
        return result

    def searchByNameStaff(self, name):
        result = []
        for i in range(0, len(self.staffList)):
            fullName = self.staffList[i].Name
            if name in fullName:
                print("found " + fullName)
                result.append(self.staffList[i])
        return result

    def searchByID(self, id):
        result = []
        for i in range(0, len(self.studentList)):
            idval = self.studentList[i].studentId
            if int(id) == int(idval) :
                print("found " + id)
                result.append(self.studentList[i])
        if(len(result) == 0):
            print("not found")
        return result

    def searchByIdStaff(self, id):
        result = []
        for i in range(0, len(self.staffList)):
            idval = self.staffList[i].staffId
            if int(id) == int(idval) :
                print("found " + id)
                result.append(self.staffList[i])
        if(len(result) == 0):
            print("not found")
        return result

    def checkDuplicateID(self,id):
        result = False
        for i in range(0, len(self.studentList)):
            idval = self.studentList[i].studentId
            if int(id) == idval:
                print("found " + id)
                result = True

        return result

    def checkDuplicateIDStaff(self,id):
        result = False
        for i in range(0, len(self.staffList)):
            idval = self.staffList[i].staffId
            if int(id) == idval:
                print("found " + id)
                result = True
        return result

    def addnewStudent(self,name,id,rfid,gname,pic,grade):
        conn = connectDB()
        cur = conn.cursor()
        query3 = "INSERT INTO STUDENT (Name, TagId, StudentID, GuardianName, grade, pic) VALUES (%s,%s,%s,%s,%s,%s);"
        queryval = (name,rfid,id,gname,grade,pic)
        addq = cur.execute(query3,queryval)
        conn.commit()
        conn.close()

    def addnewStaff(self,name,id,email,password,is_admin):
        conn = connectDB()
        cur = conn.cursor()
        query3 = "INSERT INTO STAFF (Fname, Email, Password, StaffID, isAdmin) VALUES (%s,%s,%s,%s,%s);"
        queryval = (name, email, password, id, is_admin)
        addq = cur.execute(query3,queryval)
        conn.commit()
        conn.close()

    def removeStudent(self,id):
        for i in range(0, len(self.studentList)):
            idval = self.studentList[i].studentId
            print(idval)
            if int(id) == int(idval):
                print("found " + id)
                del self.studentList[i]

    def removeStaff(self,id,user):
        for i in range(0, len(self.staffList)):
            idval = self.staffList[i].staffId
            print(idval)
            if int(id) == int(idval):
                print("found " + id)
                if(user == self.staffList[i].Name):
                    return 0
                else:
                    del self.staffList[i]
                    return 1

    def promoteStaff(self,id):
        for i in range(0, len(self.staffList)):
            idval = self.staffList[i].staffId
            if int(id) == int(idval):
                if (self.staffList[i].isAdmin):
                    return True
                else:
                    return False


    def editStudent(self,id,grade,rfid,name,gname,pic):

        conn = connectDB()
        cur = conn.cursor()
        cur.execute ("""   UPDATE student   SET Name=%s, TagId=%s, GuardianName=%s, grade=%s ,pic=%s  WHERE StudentID=%s""", (name, rfid, gname, grade, pic, id,))
        conn.commit()
        temp = cur.execute("SELECT * FROM student")
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

        conn.close()

    def editStaff(self,name,email,password,id):

        conn = connectDB()
        cur = conn.cursor()
        cur.execute ("""   UPDATE staff  SET Fname=%s, Email=%s, Password=%s  WHERE StaffID=%s""", (name, email, password, id,))
        conn.commit()
        temp = cur.execute("SELECT * FROM staff")
        data = cur.fetchall()
        self.staffList = []
        for i in range(0, len(data)):
            fName = data[i][0]
            email = data[i][1]
            password = data[i][2]
            staffId = data[i][3]
            isAdmin = data[i][4]
            staff = Staff(staffId, fName, email, password, isAdmin)
            self.staffList.append(staff)

        conn.close()

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
    email = ""
    password = ""
    isAdmin = 0

    def __init__(self, staffId, Name, email, password, isAdmin):
        self.staffId = staffId
        self.Name = Name
        self.email = email
        self.password = password
        self.isAdmin = isAdmin

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1200, 900)
        #MessageBox for Statuses
        self.PopupMessage = QtGui.QMessageBox()
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(13, 538, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 3, 3, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 5, 1, 1)
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 3)
        self.listWidget_2 = QtGui.QListWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.listWidget_2.setFont(font)
        self.listWidget_2.setObjectName(_fromUtf8("listWidget_2"))
        self.gridLayout.addWidget(self.listWidget_2, 1, 4, 1, 3)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 2, 2, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 2, 4, 1, 1)
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.gridLayout.addWidget(self.pushButton_4, 2, 6, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.pushButton.clicked.connect(self.handleClear1)
        self.pushButton_2.clicked.connect(self.handleClear2)
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
        ########################################

        self.Login_login_btn = QtGui.QPushButton(MainWindow)
        self.Login_login_btn.setGeometry(QtCore.QRect(270, 450, 211, 61))
        self.Login_login_btn.setObjectName(_fromUtf8("Login_login_btn"))
        #when login is clicked
        # self.Login_login_btn.clicked.connect(self.loginfunc)

        self.Login_registration_btn = QtGui.QPushButton(MainWindow)
        self.Login_registration_btn.setGeometry(QtCore.QRect(520, 450, 211, 61))
        self.Login_registration_btn.setObjectName(_fromUtf8("Login_registration_btn"))
        #when Login Admin is clicked
        self.Login_registration_btn.clicked.connect(self.MainAdminfunc)

        # self.Login_registration_btn.keyPressEvent(QtCore.Qt.Key_Enter).connect(self.MainAdminfunc)

        self.textEdit = QtGui.QLabel(MainWindow)
        self.textEdit.setGeometry(QtCore.QRect(450, 90, 421, 80))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textEdit.setText("Login")
        font = QtGui.QFont()
        font.setPointSize(50)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet('color: red')
        self.LogOffstaff = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffstaff.setGeometry(QtCore.QRect(790, 780, 187, 41))
        self.LogOffstaff.setObjectName(_fromUtf8("LogOffstaff"))
        #when Registration is clicked
        self.LogOffstaff.clicked.connect(self.LogOffStafffunc)
        #=======================================================
        #Registration Page

        self.label_reg = QtGui.QLabel(MainWindow)
        self.label_reg.setGeometry(QtCore.QRect(290, 230, 191, 101))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_reg.setFont(font)
        self.label_reg.setObjectName(_fromUtf8("label_reg"))
        self.Reg_email = QtGui.QLineEdit(MainWindow)
        self.Reg_email.setGeometry(QtCore.QRect(500, 260, 271, 41))
        self.Reg_email.setObjectName(_fromUtf8("Reg_email"))
        self.Reg_reg_btn = QtGui.QPushButton(MainWindow)
        self.Reg_reg_btn.setGeometry(QtCore.QRect(420, 490, 211, 61))
        self.Reg_reg_btn.setObjectName(_fromUtf8("Reg_reg_btn"))
        self.Usernamereg = QtGui.QLabel(MainWindow)
        self.Usernamereg.setGeometry(QtCore.QRect(290, 150, 191, 101))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Usernamereg.setFont(font)
        self.Usernamereg.setObjectName(_fromUtf8("Usernamereg"))
        self.Reg_username = QtGui.QLineEdit(MainWindow)
        self.Reg_username.setGeometry(QtCore.QRect(500, 180, 271, 41))
        self.Reg_username.setObjectName(_fromUtf8("Reg_username"))
        self.label_3reg = QtGui.QLabel(MainWindow)
        self.label_3reg.setGeometry(QtCore.QRect(290, 310, 191, 101))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_3reg.setFont(font)
        self.label_3reg.setObjectName(_fromUtf8("label_3reg"))
        self.Reg_password = QtGui.QLineEdit(MainWindow)
        self.Reg_password.setGeometry(QtCore.QRect(500, 340, 271, 41))
        self.Reg_password.setObjectName(_fromUtf8("Reg_password"))
        self.textEditreg = QtGui.QTextEdit(MainWindow)
        self.textEditreg.setGeometry(QtCore.QRect(380, 60, 421, 61))
        self.textEditreg.setObjectName(_fromUtf8("textEditreg"))
        self.CancleReg = QtGui.QCommandLinkButton(MainWindow)
        self.CancleReg.setGeometry(QtCore.QRect(790, 780, 187, 41))
        self.CancleReg.setObjectName(_fromUtf8("CancleReg"))
        #when Registration is clicked
        self.CancleReg.clicked.connect(self.MainAdminfunc)

        #=======================================================
        # main admin page

        self.LogOffAdmin1 = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffAdmin1.setGeometry(QtCore.QRect(990, 10, 187, 41))
        self.LogOffAdmin1.setObjectName(_fromUtf8("LogOffAdmin1"))
        #when Registration is clicked
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
        self.RegisterStaff = QtGui.QPushButton(self.verticalLayoutWidget)
        self.RegisterStaff.setObjectName(_fromUtf8("RegisterStaff"))
        self.RegisterStaff.clicked.connect(self.ShowStaffWindonFunc)
        self.horizontalLayout.addWidget(self.RegisterStaff)
        self.StudentLog = QtGui.QPushButton(self.verticalLayoutWidget)
        self.StudentLog.setObjectName(_fromUtf8("StudentLog"))
        self.horizontalLayout.addWidget(self.StudentLog)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.StudentCheckout = QtGui.QPushButton(self.verticalLayoutWidget)
        self.StudentCheckout.setObjectName(_fromUtf8("StudentCheckout"))
        self.StudentLog.clicked.connect(self.LogAdminfunc)
        self.horizontalLayout_2.addWidget(self.StudentCheckout)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.adminlabel = QtGui.QLabel(MainWindow)
        self.adminlabel.setGeometry(QtCore.QRect(30, 10, 981, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.adminlabel.setFont(font)
        self.adminlabel.setObjectName(_fromUtf8("adminlabel"))
        self.adminlabel_2 = QtGui.QLabel(MainWindow)
        self.adminlabel_2.setGeometry(QtCore.QRect(120, 270, 141, 20))
        self.adminlabel_2.setObjectName(_fromUtf8("adminlabel_2"))
        self.adminlabel_3 = QtGui.QLabel(MainWindow)
        self.adminlabel_3.setGeometry(QtCore.QRect(490, 250, 201, 61))
        self.adminlabel_3.setObjectName(_fromUtf8("adminlabel_3"))
        self.adminlabel_4 = QtGui.QLabel(MainWindow)
        self.adminlabel_4.setGeometry(QtCore.QRect(850, 270, 171, 16))
        self.adminlabel_4.setObjectName(_fromUtf8("adminlabel_4"))
        self.adminlabel_5 = QtGui.QLabel(MainWindow)
        self.adminlabel_5.setGeometry(QtCore.QRect(480, 410, 191, 16))
        self.adminlabel_5.setObjectName(_fromUtf8("adminlabel_5"))

        #=======================================================
        #Log page

        self.LogButton_Generate = QtGui.QPushButton(MainWindow)
        self.LogButton_Generate.setGeometry(QtCore.QRect(370, 550, 75, 23))
        self.LogButton_Generate.setMaximumSize(QtCore.QSize(1200, 900))
        self.LogButton_Generate.setObjectName(_fromUtf8("LogButton_Generate"))
        self.dateEdit_2 = QtGui.QDateEdit(MainWindow)
        self.dateEdit_2.setGeometry(QtCore.QRect(190, 550, 110, 22))
        self.dateEdit_2.setMaximumSize(QtCore.QSize(1200, 900))
        self.dateEdit_2.setObjectName(_fromUtf8("dateEdit_2"))
        self.LogButton_Exit = QtGui.QPushButton(MainWindow)
        self.LogButton_Exit.setGeometry(QtCore.QRect(720, 550, 75, 23))
        self.LogButton_Exit.setMaximumSize(QtCore.QSize(1200, 900))
        self.LogButton_Exit.setObjectName(_fromUtf8("LogButton_Exit"))
        self.LogButton_Exit.clicked.connect(self.CancelRegfunc)
        self.dateEdit = QtGui.QDateEdit(MainWindow)
        self.dateEdit.setGeometry(QtCore.QRect(20, 550, 110, 22))
        self.dateEdit.setMaximumSize(QtCore.QSize(1200, 900))
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.Log_label = QtGui.QLabel(MainWindow)
        self.Log_label.setGeometry(QtCore.QRect(310, 20, 251, 51))
        self.Log_label.setMaximumSize(QtCore.QSize(1200, 900))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Log_label.setFont(font)
        self.Log_label.setObjectName(_fromUtf8("Log_label"))
        self.Log_label1 = QtGui.QLabel(MainWindow)
        self.Log_label1.setGeometry(QtCore.QRect(30, 530, 61, 21))
        self.Log_label1.setMaximumSize(QtCore.QSize(1200, 900))
        self.Log_label1.setObjectName(_fromUtf8("Log_label1"))
        self.Log_label2 = QtGui.QLabel(MainWindow)
        self.Log_label2.setGeometry(QtCore.QRect(200, 530, 61, 21))
        self.Log_label2.setMaximumSize(QtCore.QSize(1200, 900))
        self.Log_label2.setObjectName(_fromUtf8("Log_label2"))
        self.LogOffAdminStudent = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffAdminStudent.setGeometry(QtCore.QRect(700, 10, 187, 41))
        self.LogOffAdminStudent.setMaximumSize(QtCore.QSize(1200, 900))
        self.LogOffAdminStudent.setObjectName(_fromUtf8("LogOffAdmin"))
        self.LogOffAdminStudent.clicked.connect(self.LogOffAdminfunc)
        self.DismissWidget = QtGui.QTabWidget(MainWindow)
        self.DismissWidget.setGeometry(QtCore.QRect(10, 70, 781, 441))
        self.DismissWidget.setMaximumSize(QtCore.QSize(1200, 900))
        self.DismissWidget.setObjectName(_fromUtf8("DismissWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.GenericReport_AppendText = QtGui.QTextEdit(self.tab)
        self.GenericReport_AppendText.setGeometry(QtCore.QRect(0, 10, 771, 401))
        self.GenericReport_AppendText.setObjectName(_fromUtf8("GenericReport_AppendText"))
        self.DismissWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.tab_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 781, 421))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.LogListView_Student1 = QtGui.QListView(self.horizontalLayoutWidget)
        self.LogListView_Student1.setObjectName(_fromUtf8("LogListView_Student1"))
        self.horizontalLayout.addWidget(self.LogListView_Student1)
        self.LogListView_Student2 = QtGui.QListView(self.horizontalLayoutWidget)
        self.LogListView_Student2.setObjectName(_fromUtf8("LogListView_Student2"))
        self.horizontalLayout.addWidget(self.LogListView_Student2)
        self.DismissWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.tab_3)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(-1, -1, 781, 421))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.LogListView_Staff1 = QtGui.QListView(self.horizontalLayoutWidget_2)
        self.LogListView_Staff1.setObjectName(_fromUtf8("LogListView_Staff1"))
        self.horizontalLayout_2.addWidget(self.LogListView_Staff1)
        self.LogListView_Staff2 = QtGui.QListView(self.horizontalLayoutWidget_2)
        self.LogListView_Staff2.setObjectName(_fromUtf8("LogListView_Staff2"))
        self.horizontalLayout_2.addWidget(self.LogListView_Staff2)
        self.DismissWidget.addTab(self.tab_3, _fromUtf8(""))

        #=======================================================

        #student window
        #generic font
        font = QtGui.QFont()
        font.setPointSize(12)
        #validators
        validator = QtGui.QIntValidator()
        regex = QtCore.QRegExp("[a-z-A-Z _]+")
        azvalidator = QtGui.QRegExpValidator(regex)
        #Labels
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
        self.StudentLabel_SearchName.setGeometry(QtCore.QRect(10, 700, 31, 16))
        self.StudentLabel_SearchName.setObjectName(_fromUtf8("StudentLabel_SearchName"))

        self.StudentLabel_SearchID = QtGui.QLabel(MainWindow)
        self.StudentLabel_SearchID.setGeometry(QtCore.QRect(310, 680, 91, 16))
        self.StudentLabel_SearchID.setObjectName(_fromUtf8("StudentLabel_SearchID"))

        #textfields
        self.StudentText_Name = QtGui.QLineEdit(MainWindow)
        self.StudentText_Name.setEnabled(False)
        self.StudentText_Name.setGeometry(QtCore.QRect(650, 60, 241, 31))
        self.StudentText_Name.setFont(font)
        self.StudentText_Name.setObjectName(_fromUtf8("StudentText_Name"))
        self.StudentText_Name.setValidator(azvalidator)

        self.StudentText_ID = QtGui.QLineEdit(MainWindow)
        self.StudentText_ID.setGeometry(QtCore.QRect(650, 130, 241, 31))
        self.StudentText_ID.setEnabled(False)
        self.StudentText_ID.setValidator(validator)
        self.StudentText_ID.setFont(font)
        self.StudentText_ID.setObjectName(_fromUtf8("StudentText_ID"))

        self.StudentText_Grade = QtGui.QLineEdit(MainWindow)
        self.StudentText_Grade.setEnabled(False)
        self.StudentText_Grade.setGeometry(QtCore.QRect(650, 200, 241, 31))
        self.StudentText_Grade.setFont(font)
        self.StudentText_Grade.setObjectName(_fromUtf8("StudentText_Grade"))
        self.StudentText_Grade.setValidator(validator)

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

        #this text is depreciated and needs to be removed everywhere
        self.StudentText_Picture = QtGui.QLineEdit(MainWindow)
        self.StudentText_Picture.setGeometry(QtCore.QRect(650, 410, 241, 31))
        self.StudentText_Picture.setFont(font)
        self.StudentText_Picture.setObjectName(_fromUtf8("StudentText_Picture"))

        #Buttons
        self.StudentButton_Remove = QtGui.QPushButton(MainWindow)
        self.StudentButton_Remove.setGeometry(QtCore.QRect(330, 830, 111, 23))
        self.StudentButton_Remove.setObjectName(_fromUtf8("StudentButton_Remove"))
        self.StudentButton_Remove.clicked.connect(self.RemoveStudentfunc)

        self.StudentButton_Exit = QtGui.QPushButton(MainWindow)
        self.StudentButton_Exit.setGeometry(QtCore.QRect(790, 780, 75, 23))
        self.StudentButton_Exit.setObjectName(_fromUtf8("StudentButton_Exit"))
        self.StudentButton_Exit.clicked.connect(self.CancelRegfunc)

        self.StudentButton_Save = QtGui.QPushButton(MainWindow)
        self.StudentButton_Save.setGeometry(QtCore.QRect(1000, 130, 75, 23))
        self.StudentButton_Save.setObjectName(_fromUtf8("StudentButton_Save"))
        self.StudentButton_Save.clicked.connect(self.handleAddSave)

        self.StudentButton_Picture = QtGui.QPushButton(MainWindow)
        self.StudentButton_Picture.setGeometry(QtCore.QRect(700, 410, 81, 31))
        self.StudentButton_Picture.setObjectName(_fromUtf8("StudentButton_Save"))
        self.StudentButton_Picture.setText(_translate("MainWindow", "Browse", None))
        self.StudentButton_Picture.clicked.connect(self.handleBrowse)

        self.StudentButton_Save2 = QtGui.QPushButton(MainWindow)
        self.StudentButton_Save2.setGeometry(QtCore.QRect(1000, 130, 75, 23))
        self.StudentButton_Save2.setObjectName(_fromUtf8("StudentButton_Save2"))
        self.StudentButton_Save2.clicked.connect(self.confirmsavestudent)

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

        #Searchfield
        self.StudentSearch_ID = QtGui.QLineEdit(MainWindow)
        self.StudentSearch_ID.setGeometry(QtCore.QRect(310, 700, 161, 31))
        self.StudentSearch_ID.setObjectName(_fromUtf8("StudentSearch_ID"))
        self.StudentSearch_ID.setValidator(validator)

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
        # StaffSearch_Name ,

        self.StaffText_Name = QtGui.QLineEdit(MainWindow)
        self.StaffText_Name.setGeometry(QtCore.QRect(670, 60, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffText_Name.setFont(font)
        self.StaffText_Name.setObjectName(_fromUtf8("StaffText_Name"))

        self.StaffText_ID = QtGui.QLineEdit(MainWindow)
        self.StaffText_ID.setGeometry(QtCore.QRect(670, 130, 241, 31))
        self.StaffText_ID.setFont(font)
        self.StaffText_ID.setObjectName(_fromUtf8("StaffText_ID"))

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

        self.StaffLabel_CPassword = QtGui.QLabel(MainWindow)
        self.StaffLabel_CPassword.setGeometry(QtCore.QRect(550, 340, 81, 31))
        self.StaffLabel_CPassword.setFont(font)
        self.StaffLabel_CPassword.setObjectName(_fromUtf8("StaffLabel_CPassword"))

        self.StaffButton_Promote = QtGui.QPushButton(MainWindow)
        self.StaffButton_Promote.setGeometry(QtCore.QRect(520, 780, 101, 23))
        self.StaffButton_Promote.setObjectName(_fromUtf8("StaffButton_Promote"))
        self.StaffButton_Promote.clicked.connect(self.PromoteFunction)

        self.StaffLabel_Email = QtGui.QLabel(MainWindow)
        self.StaffLabel_Email.setGeometry(QtCore.QRect(550, 200, 121, 31))
        self.StaffLabel_Email.setFont(font)
        self.StaffLabel_Email.setObjectName(_fromUtf8("StaffLabel_Email"))

        self.StaffButton_Add = QtGui.QPushButton(MainWindow)
        self.StaffButton_Add.setGeometry(QtCore.QRect(120, 780, 91, 23))
        self.StaffButton_Add.setObjectName(_fromUtf8("StaffButton_Add"))
        self.StaffButton_Add.clicked.connect(self.AddStaffFunc)

        self.StaffSearch_Name = QtGui.QLineEdit(MainWindow)
        self.StaffSearch_Name.setGeometry(QtCore.QRect(10, 700, 281, 31))
        self.StaffSearch_Name.setObjectName(_fromUtf8("StaffSearch_Name"))
        regex = QtCore.QRegExp("[a-z-A-Z_]+")
        validator = QtGui.QRegExpValidator(regex)
        self.StaffSearch_Name.setValidator(validator)

        self.StaffLabel_SearchID = QtGui.QLabel(MainWindow)
        self.StaffLabel_SearchID.setGeometry(QtCore.QRect(310, 680, 91, 16))
        self.StaffLabel_SearchID.setObjectName(_fromUtf8("StaffLabel_SearchID"))
        self.StaffLabel_SearchID.setText(_translate("MainWindow", "Search ID", None))

        self.StaffSearch_ID = QtGui.QLineEdit(MainWindow)
        self.StaffSearch_ID.setGeometry(QtCore.QRect(310, 700, 161, 31))
        self.StaffSearch_ID.setObjectName(_fromUtf8("StaffSearch_ID"))
        validator = QtGui.QIntValidator()
        self.StaffSearch_ID.setValidator(validator)
        self.StaffButton_SearchID = QtGui.QPushButton(MainWindow)
        self.StaffButton_SearchID.setGeometry(QtCore.QRect(310, 740, 121, 27))
        self.StaffButton_SearchID.setObjectName(_fromUtf8("StaffButton_SearchID"))
        self.StaffButton_SearchID.setText(_translate("MainWindow", "Search by ID", None))


        self.StaffButton_SearchName = QtGui.QPushButton(MainWindow)
        self.StaffButton_SearchName.setGeometry(QtCore.QRect(10, 740, 121, 27))
        self.StaffButton_SearchName.setObjectName(_fromUtf8("StaffButton_SearchName"))
        self.StaffButton_SearchName.setText(_translate("MainWindow", "Search Name", None))

        self.StaffButton_Save2 = QtGui.QPushButton(MainWindow)
        self.StaffButton_Save2.setGeometry(QtCore.QRect(1000, 130, 75, 23))
        self.StaffButton_Save2.setObjectName(_fromUtf8("StaffButton_Save2"))
        self.StaffButton_Save2.setText(_translate("MainWindow", "Save", None))
        self.StaffButton_Save2.clicked.connect(self.confirmsavestaff)

        self.StaffButton_Save = QtGui.QPushButton(MainWindow)
        self.StaffButton_Save.setGeometry(QtCore.QRect(1000, 130, 75, 23))
        self.StaffButton_Save.setObjectName(_fromUtf8("StaffButton_Save"))
        self.StaffButton_Save.setText(_translate("MainWindow", "Save", None))
        self.StaffButton_Save.clicked.connect(self.handleAddStaffSave)

        self.StaffButton_Cancel = QtGui.QPushButton(MainWindow)
        self.StaffButton_Cancel.setGeometry(QtCore.QRect(1000, 200, 75, 23))
        self.StaffButton_Cancel.setObjectName(_fromUtf8("StaffButton_Cancel"))
        self.StaffButton_Cancel.setText(_translate("MainWindow", "Cancel", None))
        self.StaffButton_Cancel.clicked.connect(self.handleStaffCancel)

        self.StaffButton_Remove = QtGui.QPushButton(MainWindow)
        self.StaffButton_Remove.setGeometry(QtCore.QRect(380, 780, 101, 23))
        self.StaffButton_Remove.setObjectName(_fromUtf8("StaffButton_Remove"))
        self.StaffButton_Remove.clicked.connect(self.RemoveStafffunc)

        self.StaffView = QtGui.QListWidget(MainWindow)
        self.StaffView.setGeometry(QtCore.QRect(10, 60, 450, 550))
        self.StaffView.setObjectName(_fromUtf8("StaffView"))
        self.StaffView.itemClicked.connect(self.handleViewDetailStaff)

        self.StaffLabel_SearchName = QtGui.QLabel(MainWindow)
        self.StaffLabel_SearchName.setGeometry(QtCore.QRect(10, 680, 91, 16))
        self.StaffLabel_SearchName.setObjectName(_fromUtf8("StaffLabel_SearchName"))
        self.StaffLabel_SearchName.setText(_translate("MainWindow", "Search Name", None))


        self.LogOffAdmin_Staff = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffAdmin_Staff.setGeometry(QtCore.QRect(1100, 10, 187, 41))
        self.LogOffAdmin_Staff.setObjectName(_fromUtf8("LogOffAdmin_Staff"))
        self.LogOffAdmin_Staff.clicked.connect(self.LogOffAdminfunc)

        self.StaffLabel_Name = QtGui.QLabel(MainWindow)
        self.StaffLabel_Name.setGeometry(QtCore.QRect(550, 60, 81, 31))
        self.StaffLabel_Name.setFont(font)
        self.StaffLabel_Name.setObjectName(_fromUtf8("StaffLabel_Name"))
        self.StaffButton_Exit = QtGui.QPushButton(MainWindow)
        self.StaffButton_Exit.setGeometry(QtCore.QRect(790, 780, 75, 23))
        self.StaffButton_Exit.setObjectName(_fromUtf8("StaffButton_Exit"))
        self.StaffButton_Exit.clicked.connect(self.CancelRegfunc)

        self.StaffButton_Edit = QtGui.QPushButton(MainWindow)
        self.StaffButton_Edit.setGeometry(QtCore.QRect(250, 780, 91, 23))
        self.StaffButton_Edit.setObjectName(_fromUtf8("StaffButton_Edit"))
        self.StaffButton_Edit.clicked.connect(self.EditstaffFunc)

        self.StaffLabel_Password = QtGui.QLabel(MainWindow)
        self.StaffLabel_Password.setGeometry(QtCore.QRect(550, 270, 81, 31))
        self.StaffLabel_Password.setFont(font)
        self.StaffLabel_Password.setObjectName(_fromUtf8("StaffLabel_Password"))

        self.StaffLabel_ID = QtGui.QLabel(MainWindow)
        self.StaffLabel_ID.setGeometry(QtCore.QRect(550, 130, 81, 31))
        self.StaffLabel_ID.setFont(font)
        self.StaffLabel_ID.setObjectName(_fromUtf8("StaffLabel_ID"))


        # =================================================
        self.workerThread = WorkerThread()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.workerThread.start()

    def confirmsavestudent(self):
        if (self.popupMessage(MainWindow,"Do your really want to edit this student? ")):
            self.handleEditSaveStudent(MainWindow)

    def newOnKeyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Enter :
            print("enter ")
            self.MainAdminfunc(MainWindow)

    def confirmsavestaff(self):
        if (self.popupMessage(MainWindow,"Do your really want to edit this staff? ")):
            self.handleEditSaveStaff(MainWindow)
            self.enableLeftStaff()

    def newOnKeyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Enter :
            print("enter ")
            self.MainAdminfunc(MainWindow)

    def handleBrowse(self):
        global filename
        filename = QtGui.QFileDialog.getOpenFileName()
        pixmap = QtGui.QPixmap(filename)
        pixmap = pixmap.scaled(510, 440, QtCore.Qt.KeepAspectRatio)
        self.StudentLabel_Picture_2.setPixmap(pixmap)

    def handleViewDetailStaff(self):
        print("Bullshit")
        name = self.StaffSearch_Name.text()
        num = self.StaffView.currentRow()
        print(num)
        if name == "":
            staff = Sys.staffList[num]
        else:
            result = Sys.searchByNameStaff(name)
            print(len(result))
            staff = result[num]

        self.StaffText_Email.setText(str(staff.email))
        self.StaffText_ID.setText(str(staff.staffId))
        self.StaffText_Name.setText(staff.Name)
        # QtCoreApplication::processEvents()
        print("Do nothing")
        print(os.getcwd())

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Lane 1", None))
        self.label_2.setText(_translate("MainWindow", "Lane 2", None))
        self.pushButton.setText(_translate("MainWindow", "Clear", None))
        self.pushButton_3.setText(_translate("MainWindow", "Undo", None))
        self.pushButton_2.setText(_translate("MainWindow", "Clear", None))
        self.pushButton_4.setText(_translate("MainWindow", "Undo", None))
        self.StudentButton_Cancel.setText(_translate("Mainwindow","Cancel",None))
        self.StudentButton_Save.setText(_translate("Mainwindow", "Save", None))
        self.StudentButton_Save2.setText(_translate("Mainwindow", "Save2", None))

        self.Username.setText(_translate("MainWindow", "Username", None))
        self.Password.setText(_translate("MainWindow", "Password", None))
        self.Login_login_btn.setText(_translate("MainWindow", "Login", None))
        self.Login_registration_btn.setText(_translate("MainWindow", "Admin Login", None))
        # self.textEdit.setHtml(_translate("MainWindow",
        #                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        #                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        #                                  "p, li { white-space: pre-wrap; }\n"
        #                                  "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
        #                                  "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt; font-weight:600; font-style:italic; color:#ff0000;\">Login</span></p></body></html>",
        #                                  None))
        #self.textEdit.setText(_translate("MainWindow"),"LOGIN",None)
        self.label_reg.setText(_translate("MainWindow", "Email ID", None))
        self.Reg_reg_btn.setText(_translate("MainWindow", "Register", None))
        self.Usernamereg.setText(_translate("MainWindow", "Username", None))
        self.LogOffAdmin1.setText(_translate("MainWindow", "Log Off", None))
        self.LogOffstaff.setText(_translate("MainWindow", "Log Off", None))
        self.CancleReg.setText(_translate("MainWindow", "Cancel", None))
        self.label_3reg.setText(_translate("MainWindow", "Password", None))
        self.textEditreg.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt; font-weight:600; font-style:italic; color:#ff0000;\">Registration</span></p></body></html>", None))

        # Registration
        self.RegisterStaff.setText(_translate("MainWindow", "Register Staff", None))
        self.EditStudent.setText(_translate("MainWindow", "Edit Student", None))
        #self.AddStudent.setText(_translate("MainWindow", "Add Student", None))
        #self.RemoveStudent.setText(_translate("MainWindow", "Remove Student", None))
        #self.RemoveStaff.setText(_translate("MainWindow", "Remove Staff", None))
        #self.EditStaff.setText(_translate("MainWindow", "Edit Staff", None))
        self.StudentLog.setText(_translate("MainWindow", "Student Log", None))
        #self.LogOffAdmin.setText(_translate("MainWindow", "Log Offff", None))

        #Log
        self.LogButton_Generate.setText(_translate("MainWindow", "Generate", None))
        self.LogButton_Exit.setText(_translate("MainWindow", "Exit", None))
        self.Log_label.setText(_translate("MainWindow", "Dismissal Log", None))
        self.Log_label1.setText(_translate("MainWindow", "Start Date", None))
        self.Log_label2.setText(_translate("MainWindow", "End Date", None))
        #self.LogOffAdmin.setText(_translate("MainWindow", "Log Off", None))
        self.LogOffAdminStudent.setText(_translate("MainWindow", "Log Off", None))
        self.GenericReport_AppendText.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.5pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Write in this location to insert into the report.</span></p></body></html>", None))
        self.DismissWidget.setTabText(self.DismissWidget.indexOf(self.tab), _translate("MainWindow", "Generic Report", None))
        self.DismissWidget.setTabText(self.DismissWidget.indexOf(self.tab_2), _translate("MainWindow", "Student Report", None))
        self.DismissWidget.setTabText(self.DismissWidget.indexOf(self.tab_3), _translate("MainWindow", "Staff Report", None))

        

        #mainadmin
        #self.LogOffAdmin2.setText(_translate("MainWindow", "Log Off", None))
        self.EditStudent.setText(_translate("MainWindow", "Edit Student", None))
        self.RegisterStaff.setText(_translate("MainWindow", "Edit Staff", None))
        self.StudentLog.setText(_translate("MainWindow", "Student Log", None))
        self.StudentCheckout.setText(_translate("MainWindow", "Student Checkout", None))
        self.adminlabel.setText(_translate("MainWindow", "Welcome to the Admin menu", None))
        self.adminlabel_2.setText(_translate("MainWindow", "Add/Remove/Delete Student", None))
        self.adminlabel_3.setText(_translate("MainWindow", "Add/Remove/Delete Staff", None))
        self.adminlabel_4.setText(_translate("MainWindow", "Student log generator", None))
        self.adminlabel_5.setText(_translate("MainWindow", "Ordinary Checkout staff", None))
        # Student window
        self.StudentLabel_Grade.setText(_translate("MainWindow", "Grade Number:", None))
        self.StudentLabel_ID.setText(_translate("MainWindow", "Student ID:", None))
        self.StudentLabel_Picture_2.setText(_translate("MainWindow", "Picture", None))
        self.StudentLabel_SearchID.setText(_translate("MainWindow", "Search ID:", None))
        self.StudentButton_Remove.setText(_translate("MainWindow", "Remove Student", None))
        self.StudentButton_Exit.setText(_translate("MainWindow", "Exit", None))
        self.StudentButton_Edit.setText(_translate("MainWindow", "Edit Student", None))
        self.LogOffAdmin.setText(_translate("MainWindow", "Log Off", None))
        self.StudentLabel_Name.setText(_translate("MainWindow", "Full Name:", None))
        self.StudentLabel_Picture.setText(_translate("MainWindow", "Picture:", None))
        self.StudentLabel_SearchName.setText(_translate("MainWindow", "Search Name:", None))
        self.StudentLabel_RFID.setText(_translate("MainWindow", "Tag ID:", None))
        self.StudentButton_Add.setText(_translate("MainWindow", "Add Student", None))
        self.StudentLabel_GName.setText(_translate("MainWindow", "Guardian:", None))
        #self.StudentButton_ViewDetails.setText(_translate("MainWindow", "View Details", None))
        self.StudentButton_SearchName.setText(_translate("MainWindow", "Search By Name", None))
        self.StudentButton_SearchName.clicked.connect(self.searchByName)
        self.StudentButton_SearchID.setText(_translate("MainWindow", "Search By ID", None))
        self.StudentButton_SearchID.clicked.connect(self.searchByID)


        #staff Window
        self.StaffButton_Promote.setText(_translate("MainWindow", "Promote to Admin", None))
        self.StaffLabel_Email.setText(_translate("MainWindow", "Email:", None))
        self.StaffButton_Add.setText(_translate("MainWindow", "Add Staff", None))
        self.StaffButton_Remove.setText(_translate("MainWindow", "Remove Staff", None))
        self.StudentLabel_SearchName.setText(_translate("MainWindow", "Search Name:", None))
        self.LogOffAdmin_Staff.setText(_translate("MainWindow", "Log Off", None))
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

    def searchByName(self):
        name = self.StudentSearch_Name.text()
        result = Sys.searchByName(name)
        ui.StudentView.clear()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i].Name)
            ui.StudentView.addItem(item)
        self.StudentView.show()

    def searchByNameStaff(self):
        name = self.StaffSearch_Name.text()
        result = Sys.searchByNameStaff(name)
        ui.StaffView.clear()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i].Name)
            ui.StaffView.addItem(item)
        self.StaffView.show()

    def searchByIdStaff(self):
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
        self.StudentButton_Save2.setEnabled(False)
        self.StudentButton_Save.setEnabled(False)
        self.StudentButton_SearchID.setEnabled(False)
        self.StudentButton_SearchName.setEnabled(False)
        self.LogOffAdmin.setEnabled(False)
        self.StudentSearch_Name.setEnabled(False)
        self.StudentSearch_ID.setEnabled(False)

    def searchByID(self):
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
        self.StudentLabel_SearchName.show()
        self.StudentLabel_RFID.show()
        self.StudentButton_Add.show()
        self.StudentLabel_GName.show()
        self.StudentText_GName.show()
        self.StudentText_Grade.show()
        self.StudentText_ID.show()
        self.StudentButton_SearchID.show()
        self.StudentView.show()
        self.StudentSearch_Name.show()
        #self.StudentButton_ViewDetails.show()

        self.StudentButton_Exit.show()
        self.StudentText_Name.show()
        self.StudentText_Picture.hide()
        self.StudentButton_Picture.show()
        self.StudentText_RFID.show()

        result = Sys.getStudentNames()
        for i in range(0, len(result)):
            item = QtGui.QListWidgetItem(result[i])
            ui.StudentView.addItem(item)

        self.StudentView.show()

        # temp = self.StudentSearch_ID.text()
        # if(temp != ''):
        #     for i in range(0, len(data)):
        #         if(data[3] == int(temp)):
        #             name = data[i][0] + " " + data[i][1]
        #             item = QtGui.QListWidgetItem(name)
        #             self.StudentSearch_ID.scrollToItem()
        self.StudentSearch_ID.show()
        self.StudentSearch_Name.show()

    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_0 :
            self.close()

    def showLog(self):
        self.GenericReport_AppendText.show()
        #self.centralwidgetlog.show()
        self.LogButton_Exit.show()
        #self.LogOffAdmin2.show()
        self.GenericReport_AppendText.show()
        self.Log_label.show()
        self.Log_label1.show()
        self.Log_label2.show()
        self.LogButton_Generate.show()
        self.LogListView_Student1.show()
        self.LogListView_Student2.show()
        self.LogListView_Staff2.show()
        self.LogListView_Staff1.show()
        self.LogOffAdminStudent.show()
        self.tab.show()
        #self.tabWidget.show()
        self.tab_3.show()
        self.tab_2.show()
        self.dateEdit_2.show()
        self.menubar.show()
        self.statusbar.show()
        self.dateEdit.show()
        self.DismissWidget.show()

    def hideall(self):
        #staff hide
        self.StaffLabel_SearchName.hide()
        self.StaffLabel_SearchID.hide()
        self.StaffButton_SearchID.hide()
        self.StaffButton_SearchName.hide()
        self.StaffButton_Save.hide()
        self.StaffButton_Save2.hide()
        self.StaffButton_Cancel.hide()
        #self.StaffButton_ViewDetails.hide()
        self.StaffSearch_ID.hide()
        self.StaffSearch_Name.hide()




        self.label.hide()
        self.label_2.hide()
        self.pushButton.hide()
        self.pushButton_3.hide()
        self.pushButton_2.hide()
        self.pushButton_4.hide()
        self.listWidget.hide()


        self.Username.hide()
        self.Password.hide()
        self.Login_login_btn.hide()
        self.Login_registration_btn.hide()
        self.textEdit.hide()

        self.Login_uname.hide()
        self.Login_uname.clear()

        self.Login_password.hide()
        self.Login_password.clear()

        self.Reg_reg_btn.hide()
        self.Reg_email.hide()
        self.Reg_username.hide()
        self.Reg_password.hide()
        self.Usernamereg.hide()
        self.label_3reg.hide()
        #hiding main admin page
        self.RegisterStaff.hide()
        self.EditStudent.hide()
        #self.AddStudent.hide()
        #self.RemoveStudent.hide()
        #self.RemoveStaff.hide()
        #self.EditStaff.hide()
        self.StudentLog.hide()
        #self.LogOffAdmin.hide()  
        #hiding registration
        #show registration page
        self.textEditreg.hide()
        self.label_reg.hide()      
        #self.LogStudendid.hide()
        #self.LogDate.hide()
        #self.LogCancel.hide()
        #self.LogOk.hide()
        self.listWidget_2.hide()
        #self.LogStudentIdText.hide()
        #self.LogDateText.hide()
        self.LogOffstaff.hide()
        self.CancleReg.hide()
        self.RegisterStaff.hide()
        self.EditStudent.hide()
        self.StudentLog.hide()
        self.LogOffAdmin1.hide()
        #self.LogOffAdmin2.hide()
        #self.LogOffAdmin3.hide()
        self.adminlabel.hide()
        self.adminlabel_2.hide()
        self.adminlabel_3.hide()
        self.adminlabel_4.hide()
        self.adminlabel_5.hide()
        self.StudentCheckout.hide()
        #for log
        self.LogButton_Exit.hide()
        #self.LogOffAdmin.hide()
        self.Log_label.hide()
        self.Log_label1.hide()
        self.Log_label2.hide()
        self.LogButton_Generate.hide()
        #self.tabWidget.hide()
        self.LogListView_Student1.hide()
        self.LogListView_Student2.hide()
        self.LogListView_Staff2.hide()
        self.LogListView_Staff1.hide()
        #self.centralwidgetlog.hide()
        self.tab.hide()
        #self.tabWidget.hide()
        self.tab_3.hide()
        self.tab_2.hide()
        self.dateEdit.hide()
        self.dateEdit_2.hide()
        self.menubar.hide()
        self.statusbar.hide()
        #self.LogOffAdmin2.hide()
        self.DismissWidget.hide()
        self.LogOffAdminStudent.hide()

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
        #self.StudentButton_ViewDetails.hide()
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
        self.StudentButton_Save.hide()
        self.StudentButton_Cancel.hide()
        self.StudentButton_Save2.hide()

    def showMain(self):
        #show for main
        self.label.show()
        self.label_2.show()
        self.pushButton.show()
        self.pushButton_3.show()
        self.pushButton_2.show()
        self.pushButton_4.show()
        self.listWidget.show()
        self.listWidget_2.show()
        self.LogOffstaff.show()

    def showMainAdmin(self):
        #show admin page
        self.RegisterStaff.show()
        self.EditStudent.show()
        self.StudentLog.show()
        self.LogOffAdmin1.show()
        #self.verticalLayoutWidget.show()
        #self.horizontalLayout.show()
        self.adminlabel.show()
        self.adminlabel_2.show()
        self.adminlabel_3.show()
        self.adminlabel_4.show()
        self.adminlabel_5.show()
        self.StudentCheckout.show()

    def showRegistration(self):
        #show registration page
        self.Reg_reg_btn.show()
        self.Reg_email.show()
        self.Reg_username.show()
        self.Reg_password.show()
        #self.Username.show()
        self.textEditreg.show()
        self.label_3reg.show()
        self.Usernamereg.show()
        self.label_reg.show()
        self.CancleReg.show()

    def showLogin(self):
        self.Username.show()
        self.Password.show()
        self.Login_login_btn.show()
        self.Login_registration_btn.show()
        self.textEdit.show()
        self.Login_uname.show()
        self.Login_password.show()        

    def handleClear1(self):
        items = ui.listWidget.count()
        rangedList = range(items)
        rangedList = rangedList.__reversed__()
        for i in rangedList:
            if ui.listWidget.isItemSelected(ui.listWidget.item(i)) == True:
                ui.listWidget.takeItem(i)

    def handleClear2(self):
        items = ui.listWidget_2.count()
        rangedList = range(items)
        rangedList = rangedList.__reversed__()
        for i in rangedList:
            if ui.listWidget_2.isItemSelected(ui.listWidget_2.item(i)) == True:
                ui.listWidget_2.takeItem(i)
                break

    def handleViewDetail(self):
        picpath = "../pictures/"
        # item = self.StudentView.currentItem().text()
        # print(item)
        name = self.StudentSearch_Name.text()
        num = self.StudentView.currentRow()
        print(num)
        if name == "":
            student = Sys.studentList[num]
        else:
            result = Sys.searchByName(name)
            print(len(result))
            student = result[num]

        print(student.image)
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
                        self.StudentButton_Save2.setEnabled(True)
                        self.StudentButton_Save.setEnabled(True)
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
        self.StudentButton_Save.hide()
        self.StudentButton_Cancel.hide()
        self.StudentButton_Save2.hide()
        self.clearallfunction(MainWindow)
        self.enable()


        self.StudentView.setEnabled(True)
        self.StudentButton_Exit.setEnabled(True)

        self.StudentButton_SearchName.setEnabled(True)
        #self.StudentButton_ViewDetails.setEnabled(True)
        self.StudentButton_Add.setEnabled(True)
        self.StudentButton_Edit.setEnabled(True)
        self.StudentButton_Remove.setEnabled(True)
        self.StudentButton_Save2.setEnabled(True)
        self.StudentButton_Save.setEnabled(True)
        self.StudentButton_SearchID.setEnabled(True)
        self.StudentButton_SearchName.setEnabled(True)
        self.LogOffAdmin.setEnabled(True)
        self.StudentSearch_Name.setEnabled(True)
        self.StudentSearch_ID.setEnabled(True)

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

    def handleAddStaffSave(self, MainWindow):
        id = self.StaffText_ID.text()
        email = self.StaffText_Email.text()
        name = self.StaffText_Name.text()
        password = self.StaffText_Pass.text()
        cpassword = self.StaffText_CPass.text()

        if (id == "" or email == "" or name == "" or password == "" or cpassword == ""):
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
                        Sys.staffList.append(Staff(id, name, email, password, 0))
                        Sys.addnewStaff(name, int(id), email, password, 0)
                        self.searchByNameStaff()
                        print("Input validated")
                        print("Save1 Clicked")
                        self.enableLeftStaff()
                        self.clearallfunction(MainWindow)
                        self.StudentView.repaint()

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
        self.StudentButton_Save2.setEnabled(True)
        self.StudentButton_Save.setEnabled(True)
        self.StudentButton_SearchID.setEnabled(True)
        self.StudentButton_SearchName.setEnabled(True)
        self.LogOffAdmin.setEnabled(True)
        self.StudentSearch_Name.setEnabled(True)
        self.StudentSearch_ID.setEnabled(True)
        self.StudentButton_Save2.hide()
        self.StudentButton_Cancel.hide()
        print("Save2 Clicked")

    def handleEditSaveStaff(self, MainWindow):
        name = self.StaffText_Name.text()
        email = self.StaffText_Email.text()
        id = self.StaffText_ID.text()
        password = self.StaffText_Pass.text()
        Sys.editStaff(name, email, password, id)
        Ui_MainWindow.searchByName(self)

        self.enable()

        self.StudentView.setEnabled(True)
        self.StudentButton_Exit.setEnabled(True)

        self.StudentButton_SearchName.setEnabled(True)
        #self.StudentButton_ViewDetails.setEnabled(True)
        self.StudentButton_Add.setEnabled(True)
        self.StudentButton_Edit.setEnabled(True)
        self.StudentButton_Remove.setEnabled(True)
        self.StudentButton_Save2.setEnabled(True)
        self.StudentButton_Save.setEnabled(True)
        self.StudentButton_SearchID.setEnabled(True)
        self.StudentButton_SearchName.setEnabled(True)
        self.LogOffAdmin.setEnabled(True)
        self.StudentSearch_Name.setEnabled(True)
        self.StudentSearch_ID.setEnabled(True)
        self.StudentButton_Save2.hide()
        self.StudentButton_Cancel.hide()


        print("Save2 Clicked")

    def Registrationfunc(self, MainWindow):
        #when Registration is clicked
        self.hideall()
        self.showRegistration()
        ##print("Registration clicked")

    def MainAdminfunc(self, MainWindow):
        #when Admin Login is clicked is clicked
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

    def LogOffAdminfunc(self, MainWindow):
        #when Admin Login is clicked is clicked
        self.hideall()
        self.showLogin()
        ##print("Registration clicked")

    def LogAdminfunc(self, MainWindow):
        self.hideall()
        self.showLog()

    def LogOffStafffunc(self, MainWindow):
        #when Admin Login is clicked is clicked
        self.hideall()
        self.showLogin()

    def CancelRegfunc(self, MainWindow):
        #when Admin Login is clicked is clicked
        self.hideall()
        self.showMainAdmin()
        ui.StudentView.clear()
        ui.StaffView.clear()

    def ShowAdminFunc(self, MainWindow):
        self.hideall()
        self.showStudentWindow()
        self.StudentButton_Picture.setEnabled(False)

    def ShowStaffWindonFunc(self,MainWindow):
        self.hideall()
        self.showStaffWindow()
        self.enableLeftStaff()

    def addStudentfunc(self,MainWindow):
        self.hideall()
        self.showStudentWindow()
        self.StudentButton_Cancel.show()
        self.StudentButton_Save.show()
        self.clearallfunction(MainWindow)
        self.enable()
        self.StudentButton_Cancel.setEnabled(True)
        self.StudentButton_Save.setEnabled(True)
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

    def clearallfunction(self,MainWindow):
        self.StudentText_Name.clear()
        self.StudentText_RFID.clear()
        self.StudentText_Grade.clear()
        self.StudentText_GName.clear()
        self.StudentText_ID.clear()
        self.StudentText_Picture.clear()
        self.StudentLabel_Picture_2.clear()

    def editStudentfunc(self, MainWindow):
        self.hideall()
        self.showStudentWindow()
        self.StudentButton_Cancel.show()
        self.StudentButton_Save2.show()
        self.enable()
        self.StudentButton_Cancel.setEnabled(True)
        self.StudentButton_Save2.setEnabled(True)
        self.StudentText_Name.setEnabled(True)
        self.StudentText_RFID.setEnabled(True)
        self.StudentText_Grade.setEnabled(True)
        self.StudentText_GName.setEnabled(True)
        self.StudentText_ID.setEnabled(True)
        self.StudentText_Picture.setEnabled(True)
        self.StudentButton_Picture.setEnabled(True)

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
        print(name)
        if(self.popupMessage(MainWindow,"Do you really want to delete " + name + " from the database ?")):
            if(Sys.removeStaff(id, currentUser)):
                query = "DELETE FROM staff WHERE StaffID= %s;"
                query2 = (id)
                conn = connectDB()
                cur = conn.cursor()
                addq = cur.execute(query, query2)
                self.clearallfunction(MainWindow)
                conn.commit()
                conn.close()
                self.searchByNameStaff()
            else:
                self.popupMessage2(MainWindow,"Admins are not allowed to remove themselves. Please get another admin to remove you. ")

    def EditstaffFunc(self):
        self.enableRightStaff()
        self.StaffButton_Save2.show()
        self.StaffButton_Cancel.show()

    def clearStaff(self):
        self.StaffText_Name.clear()
        self.StaffText_ID.clear()
        self.StaffText_Pass.clear()
        self.StaffText_CPass.clear()
        self.StaffText_Email.clear()

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
        self.StaffButton_Save2.hide()
        self.StaffButton_Save.hide()
        self.StaffButton_Cancel.hide()
        self.StaffLabel_CPassword.hide()
        self.StaffLabel_Password.hide()
        self.StaffText_CPass.hide()
        self.StaffText_Pass.hide()

    def enableRightStaff(self):
        self.enableStaff()
        self.StaffButton_Save2.show()
        self.StaffButton_Cancel.show()
        self.StaffLabel_Password.show()
        self.StaffLabel_CPassword.show()
        self.StaffText_Name.setEnabled(True)
        self.StaffText_Email.setEnabled(True)
        self.StaffText_ID.setEnabled(True)
        self.StaffText_Pass.setEnabled(True)
        self.StaffText_CPass.setEnabled(True)
        self.StaffButton_Save2.setEnabled(True)
        self.StaffButton_Cancel.setEnabled(True)
        self.StaffText_Pass.show()
        self.StaffText_CPass.show()

    def handleStaffCancel(self):
        self.clearStaff()

        self.enableLeftStaff()

    def AddStaffFunc(self):
        self.enableStaff()
        self.clearStaff()
        self.enableRightStaff()
        self.StaffButton_Save2.hide()
        self.StaffButton_Save.show()

    def PromoteFunction (self):
        print('this')
        id = self.StaffText_ID.text()
        if(Sys.promoteStaff(id)):
            self.popupMessage2(MainWindow, self.StaffText_Name.text() + " is already an admin.")
        else:
            if(self.popupMessage(MainWindow, "Are you sure you want to promote " + self.StaffText_Name.text() + " to an admin?")):
                query = "UPDATE staff  SET isAdmin=1  WHERE StaffID=%s;"
                query2 = (id)
                conn = connectDB()
                cur = conn.cursor()
                addq = cur.execute(query, query2)
                conn.commit()
                conn.close()
                print("admin updated")
            else:
                print("admin canceled")

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
                continue
        serverSocket.close()

def client_thread(clientsocket):
    message = clientsocket.recv(2048)
    rfid = message.decode("utf-8")
    temp = search_query(rfid[2:])
    if(rfid[0:2] == "R1"):
        item = QtGui.QListWidgetItem(temp)
        ui.listWidget.addItem(item)
    elif(rfid[0:2] == "R2"):
        item = QtGui.QListWidgetItem(temp)
        ui.listWidget_2.addItem(item)
    MainWindow.update()
    clientsocket.close()

placeHolder = [["E2000017571001991550787E", "Kashif Iqbal"], ["E20051860607016213308EA2" ,"Joe Smith"], ["E2000016551401070900BF7D", "Nupur Pandey"], ["E20000175710020015507886", "Bibek"], ["E2005186060701621260955C", "Austin Hasting"], ["E2000016551400980900BF95", "Albaro Tinoco"]]

def search_query(rfid):
    for i in range(0, len(placeHolder)):
        if rfid == placeHolder[i][0]:
            return placeHolder[i][1]
    return "Not Found!"

app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

if __name__ == "__main__":
    MainWindow.show()
    print("Hello Austin")
    Sys = System()


    sys.exit(app.exec_())
