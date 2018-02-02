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

        #=======================================================
        # main admin page

        self.RegisterStaff = QtGui.QPushButton(MainWindow)
        self.RegisterStaff.setGeometry(QtCore.QRect(120, 150, 151, 61))
        self.RegisterStaff.setObjectName(_fromUtf8("RegisterStaff"))
        #when Registration is clicked
        self.RegisterStaff.clicked.connect(self.Registrationfunc)

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
        self.StudentLog = QtGui.QPushButton(MainWindow)
        self.StudentLog.setGeometry(QtCore.QRect(430, 600, 151, 61))
        self.StudentLog.setObjectName(_fromUtf8("StudentLog"))
        #when Registration is clicked
        self.StudentLog.clicked.connect(self.LogAdminfunc)

        self.LogOffAdmin = QtGui.QCommandLinkButton(MainWindow)
        self.LogOffAdmin.setGeometry(QtCore.QRect(790, 780, 187, 41))
        self.LogOffAdmin.setObjectName(_fromUtf8("LogOffAdmin"))
        #when Registration is clicked
        self.LogOffAdmin.clicked.connect(self.LogOffAdminfunc)



        #=======================================================
        #Log page
        self.LogStudendid = QtGui.QLabel(MainWindow)
        self.LogStudendid.setGeometry(QtCore.QRect(10, 10, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.LogStudendid.setFont(font)
        self.LogStudendid.setObjectName(_fromUtf8("LogStudendid"))
        self.LogDate = QtGui.QLabel(MainWindow)
        self.LogDate.setGeometry(QtCore.QRect(10, 70, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.LogDate.setFont(font)
        self.LogDate.setObjectName(_fromUtf8("LogDate"))
        self.LogStudentIdText = QtGui.QLineEdit(MainWindow)
        self.LogStudentIdText.setGeometry(QtCore.QRect(150, 20, 211, 41))
        self.LogStudentIdText.setObjectName(_fromUtf8("LogStudentIdText"))
        self.LogDateText = QtGui.QLineEdit(MainWindow)
        self.LogDateText.setGeometry(QtCore.QRect(150, 80, 211, 41))
        self.LogDateText.setObjectName(_fromUtf8("LogDateText"))
        self.LogCancel = QtGui.QPushButton(MainWindow)
        self.LogCancel.setGeometry(QtCore.QRect(70, 180, 99, 27))
        self.LogCancel.setObjectName(_fromUtf8("LogCancel"))
        self.LogOk = QtGui.QPushButton(MainWindow)
        self.LogOk.setGeometry(QtCore.QRect(240, 180, 99, 27))
        self.LogOk.setObjectName(_fromUtf8("LogOk"))





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
        self.hideMain()
        self.label_reg.setText(_translate("MainWindow", "Email ID", None))
        self.Reg_reg_btn.setText(_translate("MainWindow", "Register", None))
        self.Usernamereg.setText(_translate("MainWindow", "Username", None))
        self.label_3reg.setText(_translate("MainWindow", "Password", None))
        self.textEditreg.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt; font-weight:600; font-style:italic; color:#ff0000;\">Registration</span></p></body></html>", None))

        # Registration
        self.RegisterStaff.setText(_translate("MainWindow", "Register Staff", None))
        self.EditStudent.setText(_translate("MainWindow", "Edit Student", None))
        self.AddStudent.setText(_translate("MainWindow", "Add Student", None))
        self.RemoveStudent.setText(_translate("MainWindow", "Remove Student", None))
        self.RemoveStaff.setText(_translate("MainWindow", "Remove Staff", None))
        self.EditStaff.setText(_translate("MainWindow", "Edit Staff", None))
        self.StudentLog.setText(_translate("MainWindow", "Student Log", None))
        self.LogOffAdmin.setText(_translate("MainWindow", "Log Off", None))
        #Log
        self.LogStudendid.setText(_translate("MainWindow", "Student ID", None))
        self.LogDate.setText(_translate("MainWindow", "Date", None))
        self.LogCancel.setText(_translate("MainWindow", "Cancel", None))
        self.LogOk.setText(_translate("MainWindow", "Ok", None))

    def showLog(self):
        self.LogStudendid.show()
        self.LogDate.show()
        self.LogCancel.show()
        self.LogOk.show()


    def hideLog(self):
        #hide registration page
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
        self.label_reg.show()
        self.label_3reg.hide()
        #hiding main admin page
        self.RegisterStaff.hide()
        self.EditStudent.hide()
        self.AddStudent.hide()
        self.RemoveStudent.hide()
        self.RemoveStaff.hide()
        self.EditStaff.hide()
        self.StudentLog.hide()
        self.LogOffAdmin.hide()  
        #hiding registration
        #show registration page
        self.Reg_reg_btn.hide()
        self.Reg_email.hide()
        self.Reg_username.hide()
        self.Reg_password.hide()
        self.textEditreg.hide()
        self.label_3reg.hide()
        self.Usernamereg.hide()
        self.label_reg.hide()      



    def hideMain(self):
        #hide for login
        self.label.hide()
        self.label_2.hide()
        self.pushButton.hide()
        self.pushButton_3.hide()
        self.pushButton_2.hide()
        self.pushButton_4.hide()
        self.listWidget_2.hide()
        self.listWidget.hide()
        self.Usernamereg.hide()        
        self.Reg_reg_btn.hide()
        self.Reg_email.hide()
        self.Reg_username.hide()
        self.Reg_password.hide()
        self.label_reg.hide()
        self.textEditreg.hide()
        self.label_3reg.hide()
        #hiding main admin page
        self.RegisterStaff.hide()
        self.EditStudent.hide()
        self.AddStudent.hide()
        self.RemoveStudent.hide()
        self.RemoveStaff.hide()
        self.EditStaff.hide()
        self.StudentLog.hide()
        self.LogOffAdmin.hide()
        #hide log
        self.LogStudendid.hide()
        self.LogDate.hide()
        self.LogCancel.hide()
        self.LogOk.hide()



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

    def showMainAdmin(self):
        #show admin page
        self.RegisterStaff.show()
        self.EditStudent.show()
        self.AddStudent.show()
        self.RemoveStudent.show()
        self.RemoveStaff.show()
        self.EditStaff.show()
        self.StudentLog.show()
        self.LogOffAdmin.show()

    def hideMainAdmin(self):
        #hide Admin Page
        self.label.hide()
        self.label_2.hide()
        self.pushButton.hide()
        self.pushButton_3.hide()
        self.pushButton_2.hide()
        self.pushButton_4.hide()
        self.listWidget.hide()
        self.listWidget_2.hide()
        #hide login
        self.label.hide()
        self.label_2.hide()
        self.pushButton.hide()
        self.pushButton_3.hide()
        self.pushButton_2.hide()
        self.pushButton_4.hide()
        self.listWidget_2.hide()
        self.listWidget.hide()
        self.Usernamereg.hide()        
        self.Reg_reg_btn.hide()
        self.Reg_email.hide()
        self.Reg_username.hide()
        self.Reg_password.hide()
        self.label_reg.hide()
        self.textEditreg.hide()
        self.label_3reg.hide()

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
        self.label_reg.hide()
        self.label_3reg.hide()
        #hide log
        self.LogStudendid.hide()
        self.LogDate.hide()
        self.LogCancel.hide()
        self.LogOk.hide()



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
       
    def hideRegistration(self):
        #hide registration page
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
        self.label_reg.show()
        self.label_3reg.hide()
        #hiding main admin page
        self.RegisterStaff.hide()
        self.EditStudent.hide()
        self.AddStudent.hide()
        self.RemoveStudent.hide()
        self.RemoveStaff.hide()
        self.EditStaff.hide()
        self.StudentLog.hide()
        self.LogOffAdmin.hide()
        #hide log
        self.LogStudendid.hide()
        self.LogDate.hide()
        self.LogCancel.hide()
        self.LogOk.hide()

          
    def hideLogin(self):
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
        self.textEditreg.hide()
        self.label_3reg.hide()
        #hide log
        self.LogStudendid.hide()
        self.LogDate.hide()
        self.LogCancel.hide()
        self.LogOk.hide()

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

    def loginfunc(self, MainWindow):
        #when Login button is clicked
        self.hideLogin()
        self.showMain()
        print("login clicked")

    def Registrationfunc(self, MainWindow):
        #when Registration is clicked
        self.hideRegistration()
        self.showRegistration()
        ##print("Registration clicked")

    def MainAdminfunc(self, MainWindow):
        #when Admin Login is clicked is clicked
        self.hideMainAdmin()
        self.showMainAdmin()
        ##print("Registration clicked")

    def LogOffAdminfunc(self, MainWindow):
        #when Admin Login is clicked is clicked
        self.hideLogin()
        self.hideRegistration()
        self.hideMainAdmin()
        self.showLogin()
        ##print("Registration clicked")
    def LogAdminfunc(self, MainWindow):
        self.showLog()
        self.hideog()
        


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
    temp = search_query(message.decode("utf-8"))
    item = QtGui.QListWidgetItem(temp)
    ui.listWidget.addItem(item)
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
    sys.exit(app.exec_())


