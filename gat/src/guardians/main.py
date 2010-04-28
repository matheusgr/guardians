import functools

from PyQt4 import QtCore, QtGui

import disk, quota
import gui
import config

from gui.disk_model import DiskModel

"""
ModelUpdate is responsible to create the initial view
of disk tree and also to react at each update to
find the new quota values.

Any action that may change a quota must invoke an update.
"""
class ModelUpdate:

    """
    frame - contains the DiskTreeView to be updated
    quota_widget - widget that holds the frame and buttons
    quotas_map - dict with servers/disks to be checked
    """
    def __init__(self, frame, quota_widget, quotas_map):
        self.quotas = quotas_map
        self.frame = frame
        self.models = {}
        self.buttons = {}
        # Quota_model invokes the RPC quota at remote servers
        self.quota_model = quota.QuotaCheck(quota_map.keys())
        
        # preparing buttons and DiskModels
        i = 0
        font = QtGui.QFont()
        font.setPointSize(6)
        for server in quotas_map.keys():
            # There is one model for mapping
            model = DiskModel(disk.get_list(quotas_map[server]), \
                              lambda x : ' '.join(disk.translate_size(x)))
            self.models[server] = model
            # Preparing button for this mapping
            button = QtGui.QToolButton(quota_widget)
            button.setFont(font)
            button.setObjectName("quota_button" + str(i))
            self.buttons[server] = button
            # function to set the model of the diskTreeView and define to the
            # ModelUpdate, which disk model is currently used.  
            f = functools.partial(
                lambda x, y : frame.diskTreeView.setModel(x[y]) or \
                    frame.diskTreeView.setColumnWidth(0, 280) or \
                    frame.diskTreeView.setColumnWidth(1, 100) or \
                    self.set_current_model(y), \
                self.models, server)
            QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), f)
            i += 1
        self._set_buttons()
        for button in self.buttons.values():
            self.frame.quotaLayout.addWidget(button)

    # Invoked by a button click setting which is the current diskModel
    def set_current_model(self, server):
        self.server = server

    # Set buttons in the widget
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

    # Update GUI to evaluate any update
    def update(self):
        self._set_buttons()
        # Recreate DiskModel
        model = DiskModel(disk.get_list(self.quotas[self.server]), \
                          lambda x : ' '.join(disk.translate_size(x)))
        self.models[self.server] = model
        self.frame.diskTreeView.setModel(model) 

# Prepare GUI
app = QtGui.QApplication([])
main_widget = QtGui.QWidget()

quota_widget = QtGui.QFrame(main_widget)
quota_frame = gui.disk.Ui_Frame()
quota_frame.setupUi(quota_widget)

quota_map = config.Config().getQuotasMap()
model_update = ModelUpdate(quota_frame, quota_widget, quota_map)

form = gui.main.Ui_Form()
form.setupUi(quota_widget)

"""
Gets the current selected directory at the DiskTreeView
"""
def get_selection():
    return quota_frame.diskTreeView.selectedIndexes()[0].internalPointer().path()

"""
Action to delete a directory
"""
def delete():
    src = get_selection()
    disk.recursive_delete(src)
    model_update.update()

"""
Action to move a directory
"""
def move():
    src = get_selection()
    dest_dir = unicode(QtGui.QFileDialog.getExistingDirectory())
    disk.move(src, dest_dir)
    model_update.update()

"""
Action to compact a directory
"""
def compact():
    src = get_selection()
    dest_filename = unicode(QtGui.QFileDialog.getSaveFileName())
    disk.compact(src, dest_filename)
    model_update.update()

QtCore.QObject.connect(quota_frame.deleteButton, QtCore.SIGNAL("clicked()"), delete)
QtCore.QObject.connect(quota_frame.moveButton, QtCore.SIGNAL("clicked()"), move)
QtCore.QObject.connect(quota_frame.compactButton, QtCore.SIGNAL("clicked()"), compact)

main_widget.show()
app.setStyle('cleanlooks')
app.exec_()
