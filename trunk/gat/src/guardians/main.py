import functools

from PyQt4 import QtCore, QtGui

import disk, quota
import gui
import config

from gui.disk_model import DiskModel

def new_widget(widget):
    form.verticalLayout.removeWidget(form.current_widget)
    form.current_widget.hide()
    form.current_widget = widget
    form.verticalLayout.addWidget(widget)
    widget.show()
    widget.repaint()
    main_widget.repaint()

def create_quota_buttons(widget, quotas_map):
    result = {}
    i = 0
    for server in quotas_map.keys():
        button = QtGui.QToolButton(widget)
        font = QtGui.QFont()
        font.setPointSize(6)
        button.setFont(font)
        button.setObjectName("quota_button" + str(i))
        result[server] = button
        model = DiskModel(disk.get_list(quotas_map[server]), lambda x : ' '.join(disk.translate_size(x)))
        f = functools.partial(
            lambda x : quota_frame.diskTreeView.setModel(x) or \
                quota_frame.diskTreeView.setColumnWidth(0, 280) or \
                quota_frame.diskTreeView.setColumnWidth(1, 100), \
            model)
        QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), f)
        i += 1
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
            result += str(disk.translate_size(curblocks)[0]) + '/' + ' '.join(disk.translate_size(hardlimit))
        else:
            result += '-'
        buttons[(server, dir)].setText(QtGui.QApplication.translate("Frame", result, None, QtGui.QApplication.UnicodeUTF8))

app = QtGui.QApplication([])
main_widget = QtGui.QWidget()

quota_widget = QtGui.QFrame(main_widget)
quota_widget.hide()
quota_frame = gui.disk.Ui_Frame()
quota_frame.setupUi(quota_widget)

quota_map = config.Config().getQuotasMap()
quota_model = quota.QuotaCheck(quota_map.keys())
quotas = quota_model.getQuota()
quota_buttons = create_quota_buttons(quota_widget, quota_map)
set_buttons(quotas, quota_buttons)
for button in quota_buttons.values():
    quota_frame.quotaLayout.addWidget(button)

message_widget = QtGui.QFrame(main_widget)
message_widget.hide()
gui.message.Ui_SendMailWidget().setupUi(message_widget)

faq_widget = QtGui.QFrame(main_widget)
faq_widget.hide()
gui.faq.Ui_Frame().setupUi(faq_widget)

form = gui.main.Ui_Form()
form.setupUi(main_widget)

QtCore.QObject.connect(form.quota_button, QtCore.SIGNAL("clicked()"), functools.partial(lambda x : new_widget(x), quota_widget))
QtCore.QObject.connect(form.message_button, QtCore.SIGNAL("clicked()"), functools.partial(lambda x : new_widget(x), message_widget))
QtCore.QObject.connect(form.faq_button, QtCore.SIGNAL("clicked()"), functools.partial(lambda x : new_widget(x), faq_widget))

main_widget.show()
app.setStyle('cleanlooks')
app.exec_()
