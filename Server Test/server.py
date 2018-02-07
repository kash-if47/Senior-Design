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
        MainWindow.resize(800, 600)
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

        self.Login_login_btn.clicked.connect(self.loginfunc)

        self.Login_registration_btn = QtGui.QPushButton(MainWindow)
        self.Login_registration_btn.setGeometry(QtCore.QRect(520, 450, 211, 61))
        self.Login_registration_btn.setObjectName(_fromUtf8("Login_registration_btn"))

        self.Login_registration_btn.clicked.connect(self.Registrationfunc)

        self.textEdit = QtGui.QTextEdit(MainWindow)
        self.textEdit.setGeometry(QtCore.QRect(330, 90, 421, 61))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
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
        self.Username.setText(_translate("Dialog", "Username", None))
        self.Password.setText(_translate("Dialog", "Password", None))
        self.Login_login_btn.setText(_translate("Dialog", "Login", None))
        self.Login_registration_btn.setText(_translate("Dialog", "Register", None))
        self.textEdit.setHtml(_translate("Dialog",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
                                         "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt; font-weight:600; font-style:italic; color:#ff0000;\">Login</span></p></body></html>",
                                         None))
        self.hideMain()

    def hideMain(self):
        self.label.hide()
        self.label_2.hide()
        self.pushButton.hide()
        self.pushButton_3.hide()
        self.pushButton_2.hide()
        self.pushButton_4.hide()
        self.listWidget_2.hide()
        self.listWidget.hide()

    def showMain(self):
        self.label.show()
        self.label_2.show()
        self.pushButton.show()
        self.pushButton_3.show()
        self.pushButton_2.show()
        self.pushButton_4.show()
        self.listWidget.show()
        self.listWidget_2.show()

    def hideLogin(self):
        self.Username.hide()
        self.Password.hide()
        self.Login_login_btn.hide()
        self.Login_registration_btn.hide()
        self.textEdit.hide()
        self.Login_uname.hide()
        self.Login_password.hide()


    def handleClear1(self):
        items = ui.listWidget.count()
        rangedList = range(items)
        rangedList = rangedList.__reversed__()
        for i in rangedList:
            if ui.listWidget.isItemSelected(ui.listWidget.item(i)) == True:
                ui.listWidget.takeItem(i)

    def loginfunc(self, MainWindow):
        self.hideLogin()
        self.showMain()
        print("login clicked")

    def Registrationfunc(self, MainWindow):
        print("Registration clicked")

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




