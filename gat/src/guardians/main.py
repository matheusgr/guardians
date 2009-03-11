import functools

from PyQt4 import QtCore, QtGui

import disk, quota, mail
import gui
import config

from gui.disk_model import DiskModel

class ModelUpdate:

    def __init__(self, frame, quota_widget, quotas_map):
        self.quotas = quotas_map
        self.frame = frame
        self.models = {}
        self.buttons = {}
        self.quota_model = quota.QuotaCheck(quota_map.keys())
        i = 0
        font = QtGui.QFont()
        font.setPointSize(6)
        for server in quotas_map.keys():
            model = DiskModel(disk.get_list(quotas_map[server]), \
                              lambda x : ' '.join(disk.translate_size(x)))
            self.models[server] = model
            button = QtGui.QToolButton(quota_widget)
            button.setFont(font)
            button.setObjectName("quota_button" + str(i))
            self.buttons[server] = button
            f = functools.partial(
                lambda x, y : frame.diskTreeView.setModel(x[y]) or \
                    frame.diskTreeView.setColumnWidth(0, 280) or \
                    frame.diskTreeView.setColumnWidth(1, 100) or \
                    self.set_current_model(y), \
                self.models, server)
            QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), f)
            i += 1

    def set_current_model(self, server):
        self.server = server

    def set_ui(self):
        self._set_buttons()
        for button in self.buttons.values():
            self.frame.quotaLayout.addWidget(button)      

    def _set_buttons(self):
        qquotas = self.quota_model.getQuota()
        for q in qquotas:
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
            self.buttons[(server, dir)].setText(QtGui.QApplication.translate("Frame", result, None, QtGui.QApplication.UnicodeUTF8))

    def update(self):
        self._set_buttons()
        model = DiskModel(disk.get_list(self.quotas[self.server]), \
                          lambda x : ' '.join(disk.translate_size(x)))
        self.models[self.server] = model
        self.frame.diskTreeView.setModel(model) 

def new_widget(widget):
    form.verticalLayout.removeWidget(form.current_widget)
    form.current_widget.hide()
    form.current_widget = widget
    form.verticalLayout.addWidget(widget)
    widget.show()
    widget.repaint()
    main_widget.repaint()

app = QtGui.QApplication([])
main_widget = QtGui.QWidget()

quota_widget = QtGui.QFrame(main_widget)
quota_widget.hide()
quota_frame = gui.disk.Ui_Frame()
quota_frame.setupUi(quota_widget)

quota_map = config.Config().getQuotasMap()
model_update = ModelUpdate(quota_frame, quota_widget, quota_map)
model_update.set_ui()

message_widget = QtGui.QFrame(main_widget)
message_widget.hide()
message_frame = gui.message.Ui_SendMailWidget()
message_frame.setupUi(message_widget)

faq_widget = QtGui.QFrame(main_widget)
faq_widget.hide()
gui.faq.Ui_Frame().setupUi(faq_widget)

form = gui.main.Ui_Form()
form.setupUi(main_widget)

QtCore.QObject.connect(form.quota_button, QtCore.SIGNAL("clicked()"), functools.partial(lambda x : new_widget(x), quota_widget))
QtCore.QObject.connect(form.message_button, QtCore.SIGNAL("clicked()"), functools.partial(lambda x : new_widget(x), message_widget))
QtCore.QObject.connect(form.faq_button, QtCore.SIGNAL("clicked()"), functools.partial(lambda x : new_widget(x), faq_widget))

def get_selection():
    return quota_frame.diskTreeView.selectedIndexes()[0].internalPointer()

def delete():
    src = get_selection()
    disk.recursive_delete(src)
    model_update.update()

def move():
    src = get_selection()
    dest_dir = QtGui.QFileDialog.getExistingDirectory()
    disk.move(src, dest_dir)
    model_update.update()

def compact():
    src = get_selection()
    dest_filename = QtGui.QFileDialog.getSaveFileName()
    disk.compact(src, dest_filename)
    model_update.update()

def send_mail():
    import os
    uid = unicode(os.getuid())
    subject = unicode(message_frame.lineEdit.text())
    message = unicode(message_frame.plainTextEdit.document().toPlainText())
    body = '\n' + 'uid - ' + uid + '\n' + 'subject - ' + subject + '\n' + message
    mail.MailToGuardians('gat_tool@lcc.ufcg.edu.br', body).send_mail()

QtCore.QObject.connect(quota_frame.deleteButton, QtCore.SIGNAL("clicked()"), delete)
QtCore.QObject.connect(quota_frame.moveButton, QtCore.SIGNAL("clicked()"), move)
QtCore.QObject.connect(quota_frame.compactButton, QtCore.SIGNAL("clicked()"), compact)

QtCore.QObject.connect(message_frame.pushButton, QtCore.SIGNAL("clicked()"), send_mail)

main_widget.show()
app.setStyle('cleanlooks')
app.exec_()
