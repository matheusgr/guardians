# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quota.ui'
#
# Created: Sun Feb 22 09:37:40 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(356,219)
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(Frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(Frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label,0,0,1,1)
        self.progressBar = QtGui.QProgressBar(Frame)
        self.progressBar.setMaximum(150)
        self.progressBar.setProperty("value",QtCore.QVariant(89))
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar,0,1,1,1)
        self.label_2 = QtGui.QLabel(Frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2,1,0,1,1)
        self.progressBar_2 = QtGui.QProgressBar(Frame)
        self.progressBar_2.setMaximum(8)
        self.progressBar_2.setProperty("value",QtCore.QVariant(2))
        self.progressBar_2.setObjectName("progressBar_2")
        self.gridLayout.addWidget(self.progressBar_2,1,1,1,1)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Frame", "home", None, QtGui.QApplication.UnicodeUTF8))
        self.progressBar.setFormat(QtGui.QApplication.translate("Frame", "%v / %m MB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Frame", "mail", None, QtGui.QApplication.UnicodeUTF8))
        self.progressBar_2.setFormat(QtGui.QApplication.translate("Frame", "%v / %m MB", None, QtGui.QApplication.UnicodeUTF8))

