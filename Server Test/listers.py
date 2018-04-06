# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ActualProgram.ui'
#
# Created: Sun Mar 18 15:17:23 2018
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(968, 649)
        self.RightList = QtGui.QListWidget(Dialog)
        self.RightList.setGeometry(QtCore.QRect(480, 240, 310, 380))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.RightList.setFont(font)
        self.RightList.setObjectName(_fromUtf8("RightList"))
        self.LeftList = QtGui.QListWidget(Dialog)
        self.LeftList.setGeometry(QtCore.QRect(20, 240, 310, 380))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.LeftList.setFont(font)
        self.LeftList.setObjectName(_fromUtf8("LeftList"))
        self.LeftListTitle = QtGui.QLabel(Dialog)
        self.LeftListTitle.setGeometry(QtCore.QRect(160, 10, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.LeftListTitle.setFont(font)
        self.LeftListTitle.setObjectName(_fromUtf8("LeftListTitle"))
        self.RightClear = QtGui.QPushButton(Dialog)
        self.RightClear.setGeometry(QtCore.QRect(820, 360, 70, 25))
        self.RightClear.setObjectName(_fromUtf8("RightClear"))
        self.LeftClear = QtGui.QPushButton(Dialog)
        self.LeftClear.setGeometry(QtCore.QRect(350, 360, 70, 25))
        self.LeftClear.setObjectName(_fromUtf8("LeftClear"))
        self.RightListTitle = QtGui.QLabel(Dialog)
        self.RightListTitle.setGeometry(QtCore.QRect(620, 10, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.RightListTitle.setFont(font)
        self.RightListTitle.setObjectName(_fromUtf8("RightListTitle"))
        self.LeftStudentPicture = QtGui.QLabel(Dialog)
        self.LeftStudentPicture.setGeometry(QtCore.QRect(150, 50, 180, 170))
        self.LeftStudentPicture.setObjectName(_fromUtf8("LeftStudentPicture"))
        self.RightStudentPicture = QtGui.QLabel(Dialog)
        self.RightStudentPicture.setGeometry(QtCore.QRect(610, 50, 180, 170))
        self.RightStudentPicture.setObjectName(_fromUtf8("RightStudentPicture"))
        self.line = QtGui.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(450, 0, 20, 650))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.LeftListTitle.setText(_translate("Dialog", "Lane 1", None))
        self.RightClear.setText(_translate("Dialog", "Clear", None))
        self.LeftClear.setText(_translate("Dialog", "Clear", None))
        self.RightListTitle.setText(_translate("Dialog", "Lane 2", None))
        self.LeftStudentPicture.setText(_translate("Dialog", "Picture", None))
        self.RightStudentPicture.setText(_translate("Dialog", "Picture", None))

