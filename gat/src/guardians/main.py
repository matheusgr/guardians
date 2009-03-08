import functools

from PyQt4 import QtCore, QtGui

import disk, quota
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
gui.message.Ui_SendMailWidget().setupUi(message_widget)

faq_widget = QtGui.QFrame(main_widget)
faq_widget.hide()
gui.faq.Ui_Frame().setupUi(faq_widget)

form = gui.main.Ui_Form()
form.setupUi(main_widget)

QtCore.QObject.connect(form.quota_button, QtCore.SIGNAL("clicked()"), functools.partial(lambda x : new_widget(x), quota_widget))
QtCore.QObject.connect(form.message_button, QtCore.SIGNAL("clicked()"), functools.partial(lambda x : new_widget(x), message_widget))
QtCore.QObject.connect(form.faq_button, QtCore.SIGNAL("clicked()"), functools.partial(lambda x : new_widget(x), faq_widget))

def test():
    """ TODO: Remove. Dont use in final version.... """
    import os.path
    dirs = set([ x.internalPointer() for x in quota_frame.diskTreeView.selectedIndexes() ])
    for dir in dirs:
        path = ''
        i_tmp = dir
        while i_tmp.parent:
            if i_tmp.parent.is_root():
                path = i_tmp.name + path
            else:
                path = os.path.sep + i_tmp.name + path
            i_tmp = i_tmp.parent
        #print path
    model_update.update()

QtCore.QObject.connect(quota_frame.deleteButton, QtCore.SIGNAL("clicked()"), test)

main_widget.show()
app.setStyle('cleanlooks')
app.exec_()
