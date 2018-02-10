
import socket
import threading
import os
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1200, 900)
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
        self.Login_password.setGeometry(QtCore.QRect(430, 290, 271, 41))
        self.Login_password.setObjectName(_fromUtf8("Login_password"))
        self.Login_login_btn = QtGui.QPushButton(MainWindow)
        self.Login_login_btn.setGeometry(QtCore.QRect(270, 450, 211, 61))
        self.Login_login_btn.setObjectName(_fromUtf8("Login_login_btn"))
        #when login is clicked
        self.Login_login_btn.clicked.connect(self.loginfunc)

        self.Login_registration_btn = QtGui.QPushButton(MainWindow)
        self.Login_registration_btn.setGeometry(QtCore.QRect(520, 450, 211, 61))
        self.Login_registration_btn.setObjectName(_fromUtf8("Login_registration_btn"))
        #when Login Admin is clicked
        self.Login_registration_btn.clicked.connect(self.MainAdminfunc)

        self.textEdit = QtGui.QTextEdit(MainWindow)
        self.textEdit.setGeometry(QtCore.QRect(330, 90, 421, 61))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))

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
        self.horizontalLayout.addWidget(self.EditStudent)
        self.RegisterStaff = QtGui.QPushButton(self.verticalLayoutWidget)
        self.RegisterStaff.setObjectName(_fromUtf8("RegisterStaff"))
        #when Edit staff is clicked
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
        #when Registration is clicked
        self.StudentLog.clicked.connect(self.LogAdminfunc)

        #when Registration is clicked
        self.StudentCheckout.clicked.connect(self.loginfunc)

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











        '''self.LogOffAdmin = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffAdmin.setGeometry(QtCore.QRect(990, 10, 187, 41))
        self.LogOffAdmin.setObjectName(_fromUtf8("LogOffAdmin"))
        #when Registration is clicked
        self.LogOffAdmin.clicked.connect(self.LogOffAdminfunc)

        self.RegisterStaff = QtGui.QPushButton(MainWindow)
        self.RegisterStaff.setGeometry(QtCore.QRect(120, 150, 151, 61))
        self.RegisterStaff.setObjectName(_fromUtf8("RegisterStaff"))
        #when Registration is clicked
        self.RegisterStaff.clicked.connect(self.Registrationfunc)

        self.verticalLayoutWidget = QtGui.QWidget(MainWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 169, 1071, 271))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))


        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.EditStudent = QtGui.QPushButton(MainWindow)
        self.EditStudent.setGeometry(QtCore.QRect(120, 300, 151, 61))
        self.EditStudent.setObjectName(_fromUtf8("EditStudent"))

        self.AddStudent = QtGui.QPushButton(MainWindow)
        self.AddStudent.setGeometry(QtCore.QRect(120, 490, 151, 61))
        self.AddStudent.setObjectName(_fromUtf8("AddStudent"))

        self.RemoveStudent = QtGui.QPushButton(MainWindow)
        self.RemoveStudent.setGeometry(QtCore.QRect(740, 150, 151, 61))
        self.RemoveStudent.setObjectName(_fromUtf8("RemoveStudent"))

        self.RemoveStaff = QtGui.QPushButton(MainWindow)
        self.RemoveStaff.setGeometry(QtCore.QRect(740, 290, 151, 61))
        self.RemoveStaff.setObjectName(_fromUtf8("RemoveStaff"))

        self.EditStaff = QtGui.QPushButton(MainWindow)
        self.EditStaff.setGeometry(QtCore.QRect(750, 480, 151, 61))
        self.EditStaff.setObjectName(_fromUtf8("EditStaff"))



        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))


        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)

        self.StudentCheckout = QtGui.QPushButton(self.verticalLayoutWidget)
        self.StudentCheckout.setObjectName(_fromUtf8("StudentCheckout"))
        self.horizontalLayout_2.addWidget(self.StudentCheckout)

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.StudentLog = QtGui.QPushButton(self.verticalLayoutWidget)
        self.StudentLog.setObjectName(_fromUtf8("StudentLog"))
        #when Registration is clicked
        self.StudentLog.clicked.connect(self.LogAdminfunc)

        self.horizontalLayout.addWidget(self.StudentLog)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.EditStudent = QtGui.QPushButton(self.verticalLayoutWidget)
        self.EditStudent.setObjectName(_fromUtf8("EditStudent"))
        self.horizontalLayout.addWidget(self.EditStudent)

        self.RegisterStaff = QtGui.QPushButton(self.verticalLayoutWidget)
        self.RegisterStaff.setObjectName(_fromUtf8("RegisterStaff"))
        self.horizontalLayout.addWidget(self.RegisterStaff)



        font = QtGui.QFont()
        font.setPointSize(16)
        self.adminlabel = QtGui.QLabel(MainWindow)
        self.adminlabel.setFont(font)
        self.adminlabel.setObjectName(_fromUtf8("adminlabel"))

        self.adminlabel_2 = QtGui.QLabel(MainWindow)
        self.adminlabel_2.setGeometry(QtCore.QRect(130, 240, 141, 20))
        self.adminlabel_2.setObjectName(_fromUtf8("adminlabel_2"))

        self.adminlabel_3 = QtGui.QLabel(MainWindow)
        self.adminlabel_3.setGeometry(QtCore.QRect(490, 220, 121, 61))
        self.adminlabel_3.setObjectName(_fromUtf8("adminlabel_3"))

        self.adminlabel_4 = QtGui.QLabel(MainWindow)
        self.adminlabel_4.setGeometry(QtCore.QRect(850, 240, 111, 16))
        self.adminlabel_4.setObjectName(_fromUtf8("adminlabel_4"))

        self.adminlabel_5 = QtGui.QLabel(MainWindow)
        self.adminlabel_5.setGeometry(QtCore.QRect(490, 390, 141, 16))
        self.adminlabel_5.setObjectName(_fromUtf8("adminlabel_5"))'''






        #=======================================================
        #Log page

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.LogButton_Exit = QtGui.QPushButton(self.centralwidget)
        self.LogButton_Exit.setGeometry(QtCore.QRect(720, 550, 75, 23))
        self.LogButton_Exit.setObjectName(_fromUtf8("LogButton_Exit"))
        self.LogOffAdmin2 = QtGui.QCommandLinkButton(self.centralwidget)
        self.LogOffAdmin2.setGeometry(QtCore.QRect(700, 10, 187, 41))
        self.LogOffAdmin2.setObjectName(_fromUtf8("LogOffAdmin2"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 70, 781, 441))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.GenericReport_AppendText = QtGui.QTextEdit(self.tab)
        self.GenericReport_AppendText.setGeometry(QtCore.QRect(0, 10, 771, 401))
        self.GenericReport_AppendText.setObjectName(_fromUtf8("GenericReport_AppendText"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
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
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
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
<<<<<<< HEAD
        self.DismissWidget.addTab(self.tab_3, _fromUtf8(""))

  

        #self.LogCancel.clicked.connect(self.CancleRegfunc)
        #=======================================================
        #student window
        self.StudentLabel_Grade = QtGui.QLabel(MainWindow)
        self.StudentLabel_Grade.setGeometry(QtCore.QRect(530, 200, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentLabel_Grade.setFont(font)
        self.StudentLabel_Grade.setObjectName(_fromUtf8("StudentLabel_Grade"))
        self.StudentText_Grade = QtGui.QLineEdit(MainWindow)
        self.StudentText_Grade.setGeometry(QtCore.QRect(650, 200, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentText_Grade.setFont(font)
        self.StudentText_Grade.setObjectName(_fromUtf8("StudentText_Grade"))
        self.StudentText_Name = QtGui.QLineEdit(MainWindow)
        self.StudentText_Name.setGeometry(QtCore.QRect(650, 60, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentText_Name.setFont(font)
        self.StudentText_Name.setObjectName(_fromUtf8("StudentText_Name"))
        self.StudentLabel_ID = QtGui.QLabel(MainWindow)
        self.StudentLabel_ID.setGeometry(QtCore.QRect(530, 130, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentLabel_ID.setFont(font)
        self.StudentLabel_ID.setObjectName(_fromUtf8("StudentLabel_ID"))
        self.StudentLabel_Picture_2 = QtGui.QLabel(MainWindow)
        self.StudentLabel_Picture_2.setGeometry(QtCore.QRect(530, 460, 361, 271))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentLabel_Picture_2.setFont(font)
        self.StudentLabel_Picture_2.setObjectName(_fromUtf8("StudentLabel_Picture_2"))
        self.StudentLabel_SearchID = QtGui.QLabel(MainWindow)
        self.StudentLabel_SearchID.setGeometry(QtCore.QRect(300, 630, 91, 16))
        self.StudentLabel_SearchID.setObjectName(_fromUtf8("StudentLabel_SearchID"))
        self.StudentText_ID = QtGui.QLineEdit(MainWindow)
        self.StudentText_ID.setGeometry(QtCore.QRect(650, 130, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentText_ID.setFont(font)
        self.StudentText_ID.setObjectName(_fromUtf8("StudentText_ID"))
        self.StudentButton_Remove = QtGui.QPushButton(MainWindow)
        self.StudentButton_Remove.setGeometry(QtCore.QRect(380, 780, 101, 23))
        self.StudentButton_Remove.setObjectName(_fromUtf8("StudentButton_Remove"))
        self.StudentButton_Remove.clicked.connect(self.RemoveStudentfunc)

        self.StudentButton_Exit = QtGui.QPushButton(MainWindow)
        self.StudentButton_Exit.setGeometry(QtCore.QRect(790, 780, 75, 23))
        self.StudentButton_Exit.setObjectName(_fromUtf8("StudentButton_Exit"))
        self.StudentButton_Exit.clicked.connect(self.CancleRegfunc)

        self.StudentSearch_ID = QtGui.QLineEdit(MainWindow)
        self.StudentSearch_ID.setGeometry(QtCore.QRect(300, 660, 161, 31))
        self.StudentSearch_ID.setObjectName(_fromUtf8("StudentSearch_ID"))
        self.StudentButton_Edit = QtGui.QPushButton(MainWindow)
        self.StudentButton_Edit.setGeometry(QtCore.QRect(250, 780, 91, 23))
        self.StudentButton_Edit.setObjectName(_fromUtf8("StudentButton_Edit"))
        self.StudentButton_Edit.clicked.connect(self.addStudentfunc)


        self.LogOffAdmin = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffAdmin.setGeometry(QtCore.QRect(1100, 10, 187, 41))
        self.LogOffAdmin.setObjectName(_fromUtf8("LogOffAdmin"))
        self.LogOffAdmin.clicked.connect(self.LogOffAdminfunc)

        self.StudentText_RFID = QtGui.QLineEdit(MainWindow)
        self.StudentText_RFID.setGeometry(QtCore.QRect(650, 340, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentText_RFID.setFont(font)
        self.StudentText_RFID.setObjectName(_fromUtf8("StudentText_RFID"))
        self.StudentText_GName = QtGui.QLineEdit(MainWindow)
        self.StudentText_GName.setGeometry(QtCore.QRect(650, 270, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentText_GName.setFont(font)
        self.StudentText_GName.setObjectName(_fromUtf8("StudentText_GName"))
        self.StudentLabel_Name = QtGui.QLabel(MainWindow)
        self.StudentLabel_Name.setGeometry(QtCore.QRect(530, 60, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentLabel_Name.setFont(font)
        self.StudentLabel_Name.setObjectName(_fromUtf8("StudentLabel_Name"))
        self.StudentLabel_Picture = QtGui.QLabel(MainWindow)
        self.StudentLabel_Picture.setGeometry(QtCore.QRect(530, 410, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentLabel_Picture.setFont(font)
        self.StudentLabel_Picture.setObjectName(_fromUtf8("StudentLabel_Picture"))
        self.StudentLabel_SearchName = QtGui.QLabel(MainWindow)
        self.StudentLabel_SearchName.setGeometry(QtCore.QRect(10, 630, 91, 16))
        self.StudentLabel_SearchName.setObjectName(_fromUtf8("StudentLabel_SearchName"))
        self.StudentText_Picture = QtGui.QLineEdit(MainWindow)
        self.StudentText_Picture.setGeometry(QtCore.QRect(650, 410, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentText_Picture.setFont(font)
        self.StudentText_Picture.setObjectName(_fromUtf8("StudentText_Picture"))
        self.StudentSearch_Name = QtGui.QLineEdit(MainWindow)
        self.StudentSearch_Name.setGeometry(QtCore.QRect(10, 660, 281, 31))
        self.StudentSearch_Name.setObjectName(_fromUtf8("StudentSearch_Name"))
        self.StudentLabel_RFID = QtGui.QLabel(MainWindow)
        self.StudentLabel_RFID.setGeometry(QtCore.QRect(530, 340, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentLabel_RFID.setFont(font)
        self.StudentLabel_RFID.setObjectName(_fromUtf8("StudentLabel_RFID"))
        self.StudentButton_Add = QtGui.QPushButton(MainWindow)
        self.StudentButton_Add.setGeometry(QtCore.QRect(120, 780, 91, 23))
        self.StudentButton_Add.setObjectName(_fromUtf8("StudentButton_Add"))
        self.StudentButton_Add.clicked.connect(self.addStudentfunc)

        self.StudentLabel_GName = QtGui.QLabel(MainWindow)
        self.StudentLabel_GName.setGeometry(QtCore.QRect(530, 270, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StudentLabel_GName.setFont(font)
        self.StudentLabel_GName.setObjectName(_fromUtf8("StudentLabel_GName"))
        self.StudentView = QtGui.QListView(MainWindow)
        self.StudentView.setGeometry(QtCore.QRect(10, 60, 450, 550))
        self.StudentView.setObjectName(_fromUtf8("StudentView"))

        #=================================================
        #Staff Window
        self.StaffText_Grade = QtGui.QLineEdit(MainWindow)
        self.StaffText_Grade.setGeometry(QtCore.QRect(670, 200, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffText_Grade.setFont(font)
        self.StaffText_Grade.setObjectName(_fromUtf8("StaffText_Grade"))
        self.StaffButton_Promote = QtGui.QPushButton(MainWindow)
        self.StaffButton_Promote.setGeometry(QtCore.QRect(520, 780, 101, 23))
        self.StaffButton_Promote.setObjectName(_fromUtf8("StaffButton_Promote"))
        self.StaffButton_Promote.clicked.connect(self.PromoteFunction)

        self.StaffLabel_Email = QtGui.QLabel(MainWindow)
        self.StaffLabel_Email.setGeometry(QtCore.QRect(550, 200, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffLabel_Email.setFont(font)
        self.StaffLabel_Email.setObjectName(_fromUtf8("StaffLabel_Email"))
        self.StaffText_ID = QtGui.QLineEdit(MainWindow)
        self.StaffText_ID.setGeometry(QtCore.QRect(670, 130, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffText_ID.setFont(font)
        self.StaffText_ID.setObjectName(_fromUtf8("StaffText_ID"))
        self.StaffButton_Add = QtGui.QPushButton(MainWindow)
        self.StaffButton_Add.setGeometry(QtCore.QRect(120, 780, 91, 23))
        self.StaffButton_Add.setObjectName(_fromUtf8("StaffButton_Add"))
        self.StaffButton_Add.clicked.connect(self.AddStaffFunc)

        self.StaffText_Name = QtGui.QLineEdit(MainWindow)
        self.StaffText_Name.setGeometry(QtCore.QRect(670, 60, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffText_Name.setFont(font)
        self.StaffText_Name.setObjectName(_fromUtf8("StaffText_Name"))
        self.StaffButton_Remove = QtGui.QPushButton(MainWindow)
        self.StaffButton_Remove.setGeometry(QtCore.QRect(380, 780, 101, 23))
        self.StaffButton_Remove.setObjectName(_fromUtf8("StaffButton_Remove"))
        self.StaffButton_Remove.clicked.connect(self.RemoveStudentfunc)

        self.StaffText_GName = QtGui.QLineEdit(MainWindow)
        self.StaffText_GName.setGeometry(QtCore.QRect(670, 270, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffText_GName.setFont(font)
        self.StaffText_GName.setObjectName(_fromUtf8("StaffText_GName"))
        self.StaffView = QtGui.QListView(MainWindow)
        self.StaffView.setGeometry(QtCore.QRect(10, 60, 450, 550))
        self.StaffView.setObjectName(_fromUtf8("StaffView"))
        self.StudentLabel_SearchName = QtGui.QLabel(MainWindow)
        self.StudentLabel_SearchName.setGeometry(QtCore.QRect(10, 630, 91, 16))
        self.StudentLabel_SearchName.setObjectName(_fromUtf8("StudentLabel_SearchName"))
        self.LogOffAdmin_Staff = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffAdmin_Staff.setGeometry(QtCore.QRect(1100, 10, 187, 41))
        self.LogOffAdmin_Staff.setObjectName(_fromUtf8("LogOffAdmin_Staff"))
        self.LogOffAdmin_Staff.clicked.connect(self.LogOffAdminfunc)

        self.StaffLabel_Name = QtGui.QLabel(MainWindow)
        self.StaffLabel_Name.setGeometry(QtCore.QRect(550, 60, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffLabel_Name.setFont(font)
        self.StaffLabel_Name.setObjectName(_fromUtf8("StaffLabel_Name"))
        self.StaffButton_Exit = QtGui.QPushButton(MainWindow)
        self.StaffButton_Exit.setGeometry(QtCore.QRect(790, 780, 75, 23))
        self.StaffButton_Exit.setObjectName(_fromUtf8("StaffButton_Exit"))
        self.StaffButton_Exit.clicked.connect(self.CancleRegfunc)

        self.StaffButton_Edit = QtGui.QPushButton(MainWindow)
        self.StaffButton_Edit.setGeometry(QtCore.QRect(250, 780, 91, 23))
        self.StaffButton_Edit.setObjectName(_fromUtf8("StaffButton_Edit"))
        self.StaffButton_Edit.clicked.connect(self.AddStaffFunc)

        self.StaffLabel_Password = QtGui.QLabel(MainWindow)
        self.StaffLabel_Password.setGeometry(QtCore.QRect(550, 270, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffLabel_Password.setFont(font)
        self.StaffLabel_Password.setObjectName(_fromUtf8("StaffLabel_Password"))
        self.StaffLabel_ID = QtGui.QLabel(MainWindow)
        self.StaffLabel_ID.setGeometry(QtCore.QRect(550, 130, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffLabel_ID.setFont(font)
        self.StaffLabel_ID.setObjectName(_fromUtf8("StaffLabel_ID"))
        self.StaffSearch_Name = QtGui.QLineEdit(MainWindow)
        self.StaffSearch_Name.setGeometry(QtCore.QRect(10, 660, 451, 31))
        self.StaffSearch_Name.setObjectName(_fromUtf8("StaffSearch_Name"))
=======
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.dateEdit = QtGui.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(20, 550, 110, 22))
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.dateEdit_2 = QtGui.QDateEdit(self.centralwidget)
        self.dateEdit_2.setGeometry(QtCore.QRect(190, 550, 110, 22))
        self.dateEdit_2.setObjectName(_fromUtf8("dateEdit_2"))
        self.Log_label = QtGui.QLabel(self.centralwidget)
        self.Log_label.setGeometry(QtCore.QRect(310, 20, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Log_label.setFont(font)
        self.Log_label.setObjectName(_fromUtf8("Log_label"))
        self.Log_label1 = QtGui.QLabel(self.centralwidget)
        self.Log_label1.setGeometry(QtCore.QRect(30, 530, 61, 21))
        self.Log_label1.setObjectName(_fromUtf8("Log_label1"))
        self.Log_label2 = QtGui.QLabel(self.centralwidget)
        self.Log_label2.setGeometry(QtCore.QRect(200, 530, 61, 21))
        self.Log_label2.setObjectName(_fromUtf8("Log_label2"))
        self.LogButton_Generate = QtGui.QPushButton(self.centralwidget)
        self.LogButton_Generate.setGeometry(QtCore.QRect(370, 550, 75, 23))
        self.LogButton_Generate.setObjectName(_fromUtf8("LogButton_Generate"))
        #MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        #MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        #MainWindow.setStatusBar(self.statusbar)


        #self.LogCancel.clicked.connect(self.CancleRegfunc)



>>>>>>> Kashif

        #=======================================================
        self.workerThread = WorkerThread()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.workerThread.start()


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Lane 1", None))
        self.label_2.setText(_translate("MainWindow", "Lane 2", None))
        self.pushButton.setText(_translate("MainWindow", "Clear", None))
        self.pushButton_3.setText(_translate("MainWindow", "Undo", None))
        self.pushButton_2.setText(_translate("MainWindow", "Clear", None))
        self.pushButton_4.setText(_translate("MainWindow", "Undo", None))

        self.Username.setText(_translate("MainWindow", "Username", None))
        self.Password.setText(_translate("MainWindow", "Password", None))
        self.Login_login_btn.setText(_translate("MainWindow", "Login", None))
        self.Login_registration_btn.setText(_translate("MainWindow", "Admin Login", None))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
                                         "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt; font-weight:600; font-style:italic; color:#ff0000;\">Login</span></p></body></html>",
                                         None))

        self.label_reg.setText(_translate("MainWindow", "Email ID", None))
        self.Reg_reg_btn.setText(_translate("MainWindow", "Register", None))
        self.Usernamereg.setText(_translate("MainWindow", "Username", None))
        #self.LogOffAdmin3.setText(_translate("MainWindow", "Log Offff", None))
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
        self.LogButton_Exit.setText(_translate("MainWindow", "Exit", None))
        self.LogOffAdmin1.setText(_translate("MainWindow", "Log Off", None))
        self.GenericReport_AppendText.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.5pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Write in this location to insert into the report.</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Generic Report", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Student Report", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Staff Report", None))
        self.Log_label.setText(_translate("MainWindow", "Dismissal Log", None))
        self.Log_label1.setText(_translate("MainWindow", "Start Date", None))
        self.Log_label2.setText(_translate("MainWindow", "End Date", None))
        self.LogButton_Generate.setText(_translate("MainWindow", "Generate", None))


        #mainadmin
        self.LogOffAdmin2.setText(_translate("MainWindow", "Log Off", None))
        self.EditStudent.setText(_translate("MainWindow", "Edit Student", None))
        self.RegisterStaff.setText(_translate("MainWindow", "Edit Staff", None))
        self.StudentLog.setText(_translate("MainWindow", "Student Log", None))
        self.StudentCheckout.setText(_translate("MainWindow", "Student Checkout", None))
        self.adminlabel.setText(_translate("MainWindow", "Welcome to the Admin menu", None))
        self.adminlabel_2.setText(_translate("MainWindow", "Add/Remove/Delete Student", None))
        self.adminlabel_3.setText(_translate("MainWindow", "Add/Remove/Delete Staff", None))
        self.adminlabel_4.setText(_translate("MainWindow", "Student log generator", None))
        self.adminlabel_5.setText(_translate("MainWindow", "Ordinary Checkout staff", None))
<<<<<<< HEAD
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
        self.StaffLabel_ID.setText(_translate("MainWindow", "Staff ID:", None))
        self.hideall()
        self.showLogin()

    def addstudentfun(self):
        self.homewindow = QtGui.QDialog()
        self.ui = Ui_DialogAdd()
        self.ui.setupUi(self.homewindow)
        self.homewindow.exec_()

    def showStaffWindow(self):
        self.StaffButton_Add.show()
        self.StaffButton_Edit.show()
        self.StaffButton_Exit.show()
        self.StaffButton_Promote.show()
        self.StaffButton_Remove.show()
        self.StaffLabel_Email.show()
        self.StaffLabel_ID.show()
        self.StaffLabel_Name.show()
        self.StaffLabel_Password.show()
        self.StaffSearch_Name.show()
        self.StaffText_GName.show()
        self.StaffText_Grade.show()
        self.StaffText_ID.show()
        self.StaffText_Name.show()
        self.StaffView.show()
        self.LogOffAdmin_Staff.show()
    def showStudentWindow(self):
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
        self.StudentText_Name.show()
        self.StudentText_Picture.show()
        self.StudentText_RFID.show()
        self.StudentSearch_ID.show()
        self.StudentSearch_Name.show()
        self.StudentView.show()

=======
        self.hideall()
        self.showLogin()

>>>>>>> Kashif
    def showLog(self):
        #self.GenericReport_AppendText.show()

        self.LogButton_Exit.show()
        '''self.LogOffAdmin2.show()
        self.GenericReport_AppendText.show()
        self.Log_label.show()
        self.Log_label1.show()
        self.Log_label2.show()
	print("hello")
        self.LogButton_Generate.show()
        self.LogListView_Student1.show()
        self.LogListView_Student2.show()
        self.LogListView_Staff2.show()
        self.LogListView_Staff1.show()
        self.centralwidget.show()
        self.tab.show()
        self.tabWidget.show()
        self.tab_3.show()
        self.tab_2.show()

        self.dateEdit_2.show()
        self.menubar.show()
        self.statusbar.show()
        self.dateEdit.show()'''

	#MainWindow.update()



    def hideall(self):
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
        self.Login_password.hide()
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
        self.LogOffAdmin2.hide()
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
        self.tabWidget.hide()
        self.LogListView_Student1.hide()
        self.LogListView_Student2.hide()
        self.LogListView_Staff2.hide()
        self.LogListView_Staff1.hide()
        self.centralwidget.hide()
        self.tab.hide()
        self.tabWidget.hide()
        self.tab_3.hide()
        self.tab_2.hide()
        self.dateEdit.hide()
        self.dateEdit_2.hide()
        self.menubar.hide()
        self.statusbar.hide()
<<<<<<< HEAD
        #self.LogOffAdmin2.hide()
        self.DismissWidget.hide()
        self.LogOffAdminStudent.hide()

        #hide all student window
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
        self.StudentView.hide()

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
        self.StaffSearch_Name.hide()
        self.StaffText_GName.hide()
        self.StaffText_Grade.hide()
        self.StaffText_ID.hide()
        self.StaffText_Name.hide()
        self.StaffView.hide()
        self.LogOffAdmin_Staff.hide()

=======
        self.LogOffAdmin2.hide()
>>>>>>> Kashif


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
                break

    def handleClear2(self):
        items = ui.listWidget_2.count()
        rangedList = range(items)
        rangedList = rangedList.__reversed__()
        for i in rangedList:
            if ui.listWidget_2.isItemSelected(ui.listWidget_2.item(i)) == True:
                ui.listWidget_2.takeItem(i)
                break

    def loginfunc(self, MainWindow):
        #when Login button is clicked
        self.hideall()
        self.showMain()
        print("login clicked")

    def Registrationfunc(self, MainWindow):
        #when Registration is clicked
        self.hideall()
        self.showRegistration()
        ##print("Registration clicked")

    def MainAdminfunc(self, MainWindow):
        #when Admin Login is clicked is clicked
        self.hideall()
        self.showMainAdmin()
        ##print("Registration clicked")

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
    def CancleRegfunc(self, MainWindow):
        #when Admin Login is clicked is clicked
        self.hideall()
        self.showMainAdmin()
<<<<<<< HEAD
    def ShowAdminFunc(self, MainWindow):
        self.hideall()
        self.showStudentWindow()
    def ShowStaffWindonFunc(self,MainWondow):
        self.hideall()
        self.showStaffWindow()


    def addStudentfunc(self):
        self.homewindow = QtGui.QDialog()
        self.ui = Ui_DialogAdd()
        self.ui.setupUi(self.homewindow)
        self.homewindow.exec_()

    def RemoveStudentfunc(self):
        self.homewindow = QtGui.QDialog()
        self.ui = Ui_ConfirmRemove()
        self.ui.setupUi(self.homewindow)
        self.homewindow.exec_()

    def AddStaffFunc(self):
        self.homewindow = QtGui.QDialog()
        self.ui = Ui_StaffDialog()
        self.ui.setupUi(self.homewindow)
        self.homewindow.exec_()

    def PromoteFunction (self):
        self.homewindow = QtGui.QDialog()
        self.ui = Ui_ConfirmPromote()
        self.ui.setupUi(self.homewindow)
        self.homewindow.exec_()

#classs for add and edit student

class Ui_DialogAdd(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(480, 640)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 30, 91, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(140, 30, 161, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 140, 81, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 130, 161, 27))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 200, 68, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 260, 121, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 320, 91, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineEdit_3 = QtGui.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 190, 161, 27))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.lineEdit_4 = QtGui.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(140, 250, 161, 27))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.lineEdit_5 = QtGui.QLineEdit(Dialog)
        self.lineEdit_5.setGeometry(QtCore.QRect(140, 310, 161, 27))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(10, 380, 111, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(140, 380, 99, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 530, 61, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        #self.pushButton_2.clicked.connect(self.cancelClicked)

        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(230, 530, 71, 27))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(10, 90, 81, 17))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.lineEdit_6 = QtGui.QLineEdit(Dialog)
        self.lineEdit_6.setGeometry(QtCore.QRect(140, 80, 161, 27))
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)



    def addstudentclicked(self):
	    username = self.Login_uname.text()
	    password = self.Login_password.text()
        #print(username)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "First Name : ", None))
        self.label_2.setText(_translate("Dialog", "Student Id :", None))
        self.label_3.setText(_translate("Dialog", "Grade :", None))
        self.label_4.setText(_translate("Dialog", "Guardian Name :", None))
        self.label_5.setText(_translate("Dialog", "RFID Tag ID :", None))
        self.label_6.setText(_translate("Dialog", "Upload Photo :", None))
        self.pushButton.setText(_translate("Dialog", "Browse", None))
        self.pushButton_2.setText(_translate("Dialog", "Cancel", None))
        self.pushButton_3.setText(_translate("Dialog", "Add", None))
        self.label_7.setText(_translate("Dialog", "Last Name : ", None))

###class for remove student

class Ui_ConfirmRemove(object):
    def setupUi(self, ConfirmRemove):
        ConfirmRemove.setObjectName(_fromUtf8("ConfirmRemove"))
        ConfirmRemove.resize(400, 150)
        ConfirmRemove.setMaximumSize(QtCore.QSize(400, 150))
        ConfirmRemove.setBaseSize(QtCore.QSize(400, 300))
        self.RemoveText = QtGui.QLabel(ConfirmRemove)
        self.RemoveText.setGeometry(QtCore.QRect(20, -30, 371, 141))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.RemoveText.setFont(font)
        self.RemoveText.setAlignment(QtCore.Qt.AlignCenter)
        self.RemoveText.setObjectName(_fromUtf8("RemoveText"))
        self.RemoveConfirm = QtGui.QPushButton(ConfirmRemove)
        self.RemoveConfirm.setGeometry(QtCore.QRect(60, 100, 75, 23))
        self.RemoveConfirm.setObjectName(_fromUtf8("RemoveConfirm"))

        self.RemoveCancel = QtGui.QPushButton(ConfirmRemove)
        self.RemoveCancel.setGeometry(QtCore.QRect(260, 100, 75, 23))
        self.RemoveCancel.setObjectName(_fromUtf8("RemoveCancel"))
        #self.RemoveCancel.clicked.connect(self.closeIt)

        self.retranslateUi(ConfirmRemove)
        QtCore.QMetaObject.connectSlotsByName(ConfirmRemove)



    def retranslateUi(self, ConfirmRemove):
        ConfirmRemove.setWindowTitle(_translate("ConfirmRemove", "Confirm", None))
        self.RemoveText.setText(_translate("ConfirmRemove", "Are you sure you want to \n"
"remove $student_staff? ", None))
        self.RemoveConfirm.setText(_translate("ConfirmRemove", "Confirm", None))
        self.RemoveCancel.setText(_translate("ConfirmRemove", "Cancel", None))




#class for promoting staff to admin
class Ui_ConfirmPromote(object):
    def setupUi(self, ConfirmPromote):
        ConfirmPromote.setObjectName(_fromUtf8("ConfirmPromote"))
        ConfirmPromote.resize(400, 150)
        ConfirmPromote.setMaximumSize(QtCore.QSize(400, 150))
        ConfirmPromote.setBaseSize(QtCore.QSize(400, 300))
        self.PromoteText = QtGui.QLabel(ConfirmPromote)
        self.PromoteText.setGeometry(QtCore.QRect(20, -30, 371, 141))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.PromoteText.setFont(font)
        self.PromoteText.setAlignment(QtCore.Qt.AlignCenter)
        self.PromoteText.setObjectName(_fromUtf8("PromoteText"))
        self.PromoteConfirm = QtGui.QPushButton(ConfirmPromote)
        self.PromoteConfirm.setGeometry(QtCore.QRect(60, 100, 75, 23))
        self.PromoteConfirm.setObjectName(_fromUtf8("PromoteConfirm"))
        self.PromoteCancel = QtGui.QPushButton(ConfirmPromote)
        self.PromoteCancel.setGeometry(QtCore.QRect(260, 100, 75, 23))
        self.PromoteCancel.setObjectName(_fromUtf8("PromoteCancel"))
        #self.PromoteCancel.clicked.connect(self.closeIt)

        self.retranslateUi(ConfirmPromote)
        QtCore.QMetaObject.connectSlotsByName(ConfirmPromote)



    def retranslateUi(self, ConfirmPromote):
        ConfirmPromote.setWindowTitle(_translate("ConfirmPromote", "Confirm", None))
        self.PromoteText.setText(_translate("ConfirmPromote", "Are you sure you want to promote \n"
"$staff_user to an admin? ", None))
        self.PromoteConfirm.setText(_translate("ConfirmPromote", "Confirm", None))
        self.PromoteCancel.setText(_translate("ConfirmPromote", "Cancel", None))





#Class for add and edit staff
class Ui_StaffDialog(object):
    def setupUi(self, StaffDialog):
        StaffDialog.setObjectName(_fromUtf8("StaffDialog"))
        StaffDialog.resize(400, 220)
        StaffDialog.setMaximumSize(QtCore.QSize(400, 220))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 254, 227))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 254, 227))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 254, 227))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 254, 227))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        StaffDialog.setPalette(palette)
        self.StaffLabel_Name = QtGui.QLabel(StaffDialog)
        self.StaffLabel_Name.setGeometry(QtCore.QRect(20, 20, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffLabel_Name.setFont(font)
        self.StaffLabel_Name.setObjectName(_fromUtf8("StaffLabel_Name"))
        self.StaffLabel_ID = QtGui.QLabel(StaffDialog)
        self.StaffLabel_ID.setGeometry(QtCore.QRect(20, 60, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffLabel_ID.setFont(font)
        self.StaffLabel_ID.setObjectName(_fromUtf8("StaffLabel_ID"))
        self.StaffLabel_Email = QtGui.QLabel(StaffDialog)
        self.StaffLabel_Email.setGeometry(QtCore.QRect(20, 100, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffLabel_Email.setFont(font)
        self.StaffLabel_Email.setObjectName(_fromUtf8("StaffLabel_Email"))
        self.StaffLabel_Password = QtGui.QLabel(StaffDialog)
        self.StaffLabel_Password.setGeometry(QtCore.QRect(20, 140, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffLabel_Password.setFont(font)
        self.StaffLabel_Password.setObjectName(_fromUtf8("StaffLabel_Password"))
        self.StaffText_Name = QtGui.QLineEdit(StaffDialog)
        self.StaffText_Name.setGeometry(QtCore.QRect(140, 20, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffText_Name.setFont(font)
        self.StaffText_Name.setObjectName(_fromUtf8("StaffText_Name"))
        self.StaffText_ID = QtGui.QLineEdit(StaffDialog)
        self.StaffText_ID.setGeometry(QtCore.QRect(140, 60, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffText_ID.setFont(font)
        self.StaffText_ID.setObjectName(_fromUtf8("StaffText_ID"))
        self.StaffText_Grade = QtGui.QLineEdit(StaffDialog)
        self.StaffText_Grade.setGeometry(QtCore.QRect(140, 100, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffText_Grade.setFont(font)
        self.StaffText_Grade.setObjectName(_fromUtf8("StaffText_Grade"))
        self.StaffText_GName = QtGui.QLineEdit(StaffDialog)
        self.StaffText_GName.setGeometry(QtCore.QRect(140, 140, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.StaffText_GName.setFont(font)
        self.StaffText_GName.setObjectName(_fromUtf8("StaffText_GName"))
        self.StaffConfirm = QtGui.QPushButton(StaffDialog)
        self.StaffConfirm.setGeometry(QtCore.QRect(70, 190, 75, 23))
        self.StaffConfirm.setObjectName(_fromUtf8("StaffConfirm"))
        self.StaffCancel = QtGui.QPushButton(StaffDialog)
        self.StaffCancel.setGeometry(QtCore.QRect(270, 190, 75, 23))
        self.StaffCancel.setObjectName(_fromUtf8("StaffCancel"))
        #self.StaffCancel.clicked.connect(self.closeIt)


        self.retranslateUi(StaffDialog)
        QtCore.QMetaObject.connectSlotsByName(StaffDialog)



    def retranslateUi(self, StaffDialog):
        StaffDialog.setWindowTitle(_translate("StaffDialog", "Staff Information", None))
        self.StaffLabel_Name.setText(_translate("StaffDialog", "Full Name:", None))
        self.StaffLabel_ID.setText(_translate("StaffDialog", "Staff ID:", None))
        self.StaffLabel_Email.setText(_translate("StaffDialog", "Email:", None))
        self.StaffLabel_Password.setText(_translate("StaffDialog", "Password:", None))
        self.StaffConfirm.setText(_translate("StaffDialog", "Confirm", None))
        self.StaffCancel.setText(_translate("StaffDialog", "Cancel", None))





=======
>>>>>>> Kashif


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
    # MainWindow.show()
    # sys.exit(app.exec_())
    print(temp)
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
    print("Hey man")
    sys.exit(app.exec_())
