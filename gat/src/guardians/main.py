from gui import main, quota, disk, message, faq
from PyQt4 import QtCore, QtGui
import dc_model

class DiskModel(QtCore.QAbstractItemModel):
    def __init__(self, result):
        QtCore.QAbstractItemModel.__init__(self)
        self.root = result
    def index(self, row, col, parent):
        if not self.hasIndex(row, col, parent):
            return QtCore.QModelIndex()
        if not parent.isValid():
            parent_item = self.root
        else:
            parent_item = parent.internalPointer()
        child = parent_item.child[row]
        if child:
            return self.createIndex(row, col, child)
        else:
            return QtCore.QModelIndex()
    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        parent = index.internalPointer().parent
        if parent == self.root:
            return QtCore.QModelIndex()
        if not parent.parent:
            return 0
        return self.createIndex(parent.parent.child.index(parent), 0, parent)
    def rowCount(self, index):
        if index.column() > 0:
            return 0
        if not index.isValid():
            parentItem = self.root
        else:
            parentItem = index.internalPointer()
        return len(parentItem.child)
    def columnCount(self, model_index):
        return 2
    def data(self, model_index, role):
        if not model_index.isValid() or not role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        col = model_index.column()
        if col == 0:
            return QtCore.QVariant(QtCore.QString(model_index.internalPointer().name))
        kb = 1024
        mb = 1024 * kb
        gb = 1024 * mb
        tb = 1024 * gb
        bytes = model_index.internalPointer().size
        if bytes >= tb:
            return QtCore.QVariant(str(bytes / tb) + " TB")
        if bytes >= gb:
            return QtCore.QVariant(str(bytes / gb) + " GB")
        if bytes >= mb:
            return QtCore.QVariant(str(bytes / mb) + " MB")
        if bytes >= kb:
            return QtCore.QVariant(str(bytes / kb) + " KB")
        return QtCore.QVariant(str(bytes) + " bytes")
    def flags(self, index):
        if not index.isValid():
            return 0
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section == 0:
                return QtCore.QVariant('Name')
            else:
                return QtCore.QVariant('Size')
        return QtCore.QVariant()

def new_widget(widget):
    form.verticalLayout.removeWidget(form.current_widget)
    form.current_widget.hide()
    form.current_widget = widget
    form.verticalLayout.addWidget(widget)
    widget.show()
    widget.repaint()
    main_widget.repaint()

def quota_clicked():
    new_widget(quota_widget)

def disk_clicked():
    new_widget(disk_widget)

def message_clicked():
    new_widget(message_widget)

def faq_clicked():
    new_widget(faq_widget)

app = QtGui.QApplication([])
main_widget = QtGui.QWidget()

disk_widget = QtGui.QFrame(main_widget)
disk_widget.hide()
d_frame = disk.Ui_Frame()
d_frame.setupUi(disk_widget)
model = DiskModel(dc_model.get_list('.'))
d_frame.treeView.setModel(model)
d_frame.treeView.setColumnWidth(0, 280)
d_frame.treeView.setColumnWidth(1, 100)

quota_widget = QtGui.QFrame(main_widget)
quota_widget.hide()
quota.Ui_Frame().setupUi(quota_widget)

message_widget = QtGui.QFrame(main_widget)
message_widget.hide()
message.Ui_SendMailWidget().setupUi(message_widget)

faq_widget = QtGui.QFrame(main_widget)
faq_widget.hide()
faq.Ui_Frame().setupUi(faq_widget)

form = main.Ui_Form()
form.setupUi(main_widget)

QtCore.QObject.connect(form.quota_button, QtCore.SIGNAL("clicked()"), quota_clicked)
QtCore.QObject.connect(form.home_button, QtCore.SIGNAL("clicked()"), disk_clicked)
QtCore.QObject.connect(form.mail_button, QtCore.SIGNAL("clicked()"), message_clicked)
QtCore.QObject.connect(form.faq_button, QtCore.SIGNAL("clicked()"), faq_clicked)
main_widget.show()
app.exec_()
