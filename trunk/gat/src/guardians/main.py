import functools

from PyQt4 import QtCore, QtGui

import dc_model
import qc_model
import config

from gui import main, disk, message, faq
from disk_model import DiskModel, translate_size

def new_widget(widget):
    form.verticalLayout.removeWidget(form.current_widget)
    form.current_widget.hide()
    form.current_widget = widget
    form.verticalLayout.addWidget(widget)
    widget.show()
    widget.repaint()
    main_widget.repaint()

def message_clicked():
    new_widget(message_widget)

def disk_clicked():
    new_widget(disk_widget)

def faq_clicked():
    new_widget(faq_widget)

def create_quota_buttons(quotas_map):
    result = {}
    i = 0
    for server in quotas_map.keys():
        button = QtGui.QToolButton(disk_widget)
        font = QtGui.QFont()
        font.setPointSize(6)
        button.setFont(font)
        button.setObjectName("quota_button" + str(i))
        result[server] = button
        model = DiskModel(dc_model.get_list(quotas_map[server]))
        f = functools.partial(lambda x : d_frame.diskTreeView.setModel(x) or d_frame.diskTreeView.setColumnWidth(0, 280) or d_frame.diskTreeView.setColumnWidth(1, 100), model)
        QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), f)
    return result

def set_buttons(quotas, buttons):
    for q in quotas:
        server = q[0]
        dir = q[1]
        status = q[2]
        result = server + ":" + dir + '\n'
        if status == 1: # Avaliable
            bzise = q[3][0]
            hardlimit = q[3][2]
            softlimit = q[3][3]
            curblocks = q[3][4]
            result += str(translate_size(curblocks).split()[0]) + '/' + translate_size(hardlimit)
        else:
            result += '-'
        buttons[(server, dir)].setText(QtGui.QApplication.translate("Frame", result, None, QtGui.QApplication.UnicodeUTF8))

app = QtGui.QApplication([])
main_widget = QtGui.QWidget()

disk_widget = QtGui.QFrame(main_widget)
disk_widget.hide()
d_frame = disk.Ui_Frame()
d_frame.setupUi(disk_widget)

quota_map = config.Config().getQuotasMap()
quota_model = qc_model.QuotaCheckModel(quota_map.keys())
quotas = quota_model.getQuota()
quota_buttons = create_quota_buttons(quota_map)
set_buttons(quotas, quota_buttons)
for button in quota_buttons.values():
    d_frame.quotaLayout.addWidget(button)
#model = DiskModel(dc_model.get_list('.'))

#d_frame.diskTreeView.setModel(model)

message_widget = QtGui.QFrame(main_widget)
message_widget.hide()
message.Ui_SendMailWidget().setupUi(message_widget)

faq_widget = QtGui.QFrame(main_widget)
faq_widget.hide()
faq.Ui_Frame().setupUi(faq_widget)

form = main.Ui_Form()
form.setupUi(main_widget)

QtCore.QObject.connect(form.quota_button, QtCore.SIGNAL("clicked()"), disk_clicked)
QtCore.QObject.connect(form.mail_button, QtCore.SIGNAL("clicked()"), message_clicked)
QtCore.QObject.connect(form.faq_button, QtCore.SIGNAL("clicked()"), faq_clicked)
main_widget.show()
app.setStyle('cleanlooks')
app.exec_()
