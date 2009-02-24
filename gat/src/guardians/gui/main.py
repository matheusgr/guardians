# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Sun Feb 22 09:37:40 2009
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(524,356)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtGui.QFrame(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.quota_button = QtGui.QToolButton(self.frame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/network-server-database.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.quota_button.setIcon(icon)
        self.quota_button.setIconSize(QtCore.QSize(48,48))
        self.quota_button.setObjectName("quota_button")
        self.verticalLayout_4.addWidget(self.quota_button)
        self.home_button = QtGui.QToolButton(self.frame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/user-home.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.home_button.setIcon(icon)
        self.home_button.setIconSize(QtCore.QSize(48,48))
        self.home_button.setObjectName("home_button")
        self.verticalLayout_4.addWidget(self.home_button)
        self.mail_button = QtGui.QToolButton(self.frame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/mail-message.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.mail_button.setIcon(icon)
        self.mail_button.setIconSize(QtCore.QSize(48,48))
        self.mail_button.setObjectName("mail_button")
        self.verticalLayout_4.addWidget(self.mail_button)
        self.faq_button = QtGui.QToolButton(self.frame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/system-help.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.faq_button.setIcon(icon)
        self.faq_button.setIconSize(QtCore.QSize(48,48))
        self.faq_button.setObjectName("faq_button")
        self.verticalLayout_4.addWidget(self.faq_button)
        self.verticalLayout_3.addWidget(self.frame)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.current_widget = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.current_widget.sizePolicy().hasHeightForWidth())
        self.current_widget.setSizePolicy(sizePolicy)
        self.current_widget.setObjectName("current_widget")
        self.verticalLayout.addWidget(self.current_widget)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Guardians Admin Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.quota_button.setToolTip(QtGui.QApplication.translate("Form", "Quota Check", None, QtGui.QApplication.UnicodeUTF8))
        self.home_button.setToolTip(QtGui.QApplication.translate("Form", "Disk Utils", None, QtGui.QApplication.UnicodeUTF8))
        self.mail_button.setToolTip(QtGui.QApplication.translate("Form", "Mail To Admin", None, QtGui.QApplication.UnicodeUTF8))
        self.faq_button.setToolTip(QtGui.QApplication.translate("Form", "Go To FAQ", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
