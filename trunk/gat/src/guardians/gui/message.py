# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'message.ui'
#
# Created: Sun Feb 22 09:37:40 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SendMailWidget(object):
    def setupUi(self, SendMailWidget):
        SendMailWidget.setObjectName("SendMailWidget")
        SendMailWidget.resize(400,300)
        SendMailWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        SendMailWidget.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(SendMailWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(SendMailWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label,0,0,1,1)
        self.lineEdit = QtGui.QLineEdit(SendMailWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit,0,1,1,1)
        self.label_2 = QtGui.QLabel(SendMailWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2,1,0,1,1)
        self.pushButton = QtGui.QPushButton(SendMailWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton,2,1,1,1)
        self.plainTextEdit = QtGui.QPlainTextEdit(SendMailWidget)
        self.plainTextEdit.setTabChangesFocus(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit,1,1,1,1)

        self.retranslateUi(SendMailWidget)
        QtCore.QMetaObject.connectSlotsByName(SendMailWidget)
        SendMailWidget.setTabOrder(self.lineEdit,self.plainTextEdit)
        SendMailWidget.setTabOrder(self.plainTextEdit,self.pushButton)

    def retranslateUi(self, SendMailWidget):
        SendMailWidget.setWindowTitle(QtGui.QApplication.translate("SendMailWidget", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SendMailWidget", "Subject", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SendMailWidget", "Message", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("SendMailWidget", "Send", None, QtGui.QApplication.UnicodeUTF8))

