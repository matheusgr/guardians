# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'faq.ui'
#
# Created: Sun Feb 22 09:37:41 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(400,300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Frame.sizePolicy().hasHeightForWidth())
        Frame.setSizePolicy(sizePolicy)
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(Frame)
        self.gridLayout.setObjectName("gridLayout")
        self.webView = QtWebKit.QWebView(Frame)
        self.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.webView.setAcceptDrops(False)
        self.webView.setUrl(QtCore.QUrl("http://www.google.com.br/"))
        self.webView.setObjectName("webView")
        self.gridLayout.addWidget(self.webView,0,0,1,1)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
