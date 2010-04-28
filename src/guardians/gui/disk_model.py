from PyQt4 import QtCore, QtGui

class DiskModel(QtCore.QAbstractItemModel):
    def __init__(self, result, translate_size):
        QtCore.QAbstractItemModel.__init__(self)
        self.root = result
        self.translate_size = translate_size
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
        bytes = model_index.internalPointer().size
        return QtCore.QVariant(QtCore.QString(self.translate_size(bytes)))
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
