
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
        #when Registration is clicked
        self.RegisterStaff.clicked.connect(self.Registrationfunc)

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
        self.hideall()
        self.showLogin()

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
        self.LogOffAdmin2.hide()


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
