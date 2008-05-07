#!/usr/bin/env python
from guardians import dc_model
from tarfile import TarFile
import os

import sys
try:
     import pygtk
     pygtk.require("2.0")
except:
      pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

from resource import find_resource as _r

class DiskCleanGUI:
    """This is a GUI for DiskClean application"""

    def __init__(self):

        #Set the Glade file
        self.gladefile = _r("dc_gui.glade")  
        self.wTree = gtk.glade.XML(self.gladefile) 
                 
        #Create our dictionary and connect it
        dic = { "on_delete_clicked" : self.delete_clicked,
                "on_compact_clicked" : self.compact_clicked,
                "on_move_clicked" : self.move_clicked,
                "on_tree_cursor_changed" : self.tree_cursor_changed,
                "on_exit_clicked" : gtk.main_quit,
                "on_dc_gui_destroy" : gtk.main_quit }
        self.wTree.signal_autoconnect(dic)
        diskView = self.prepare_disk_view()
        diskTree = self.prepare_disk_tree(diskView)
        r = dc_model.DiskCleanModel("/home/matheusgr/videos").get_list()
        self.build_tree(r, None, diskTree, 30000000000)
        self.selected_dir = None

    def prepare_disk_view(self):
        diskView = self.wTree.get_widget("tree")
        
        column_file = gtk.TreeViewColumn("Diretorio/Arquivo", gtk.CellRendererText(), text=0)
        column_file.set_sort_column_id(0)
        column_file.set_sort_indicator(True)
        column_file.set_max_width(400)
        column_file.set_min_width(400)
        diskView.append_column(column_file)
        
        column_space = gtk.TreeViewColumn("Espaco", gtk.CellRendererProgress(), value=1)
        column_space.set_sort_column_id(1)
        column_space.set_sort_indicator(True)
        diskView.append_column(column_space)
        return diskView
    
    def prepare_disk_tree(self, diskView):
        diskTree = gtk.TreeStore(str, int)
        diskView.set_model(diskTree)
        return diskTree
    
    def build_tree(self, model, parent, disktree, max):
        for a in model:
            if len(a) == 3:
                insert = disktree.insert(parent, 0, [a[0], float(a[2])/max * 100])
                self.build_tree(a[1], insert, disktree, max)
            else:
                insert = disktree.insert(parent, 0, [a[0], float(a[1])/max * 100])

    def tree_cursor_changed(self, widget):
        if type(widget) is None:
            return
        model, iter = widget.get_selection().get_selected()
        self.selected_dir = model.get_value(iter, 0)
    
    def delete_clicked(self, widget):
        if not (self.selected_dir is None):
            confirmDialog = gtk.Dialog("Confirma apagar?", self.wTree.get_widget("dc_gui"), gtk.DIALOG_DESTROY_WITH_PARENT, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
            response = confirmDialog.run()
            if response == gtk.RESPONSE_OK:
                self.recursive_delete(self.selected_dir)
            elif response == gtk.RESPONSE_CANCEL:
                pass
            confirmDialog.destroy()

    def recursive_delete(self, directory):
        try:
            listdir = os.listdir(directory)
            for dir in listdir:
                self.recursive_delete(directory + os.sep + dir)
            os.rmdir(directory)
        except (OSError):
            os.remove(directory)
    
    def compact_clicked(self, widget):
        if not (self.selected_dir is None):
            fileChooserDialog = gtk.FileChooserDialog("Salvar arquivo", self.wTree.get_widget("dc_gui"), gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
            fileChooserDialog.set_current_name(self.selected_dir + ".tar.bz2")
            response = fileChooserDialog.run()
            if response == gtk.RESPONSE_OK:
                tmpname = os.tmpnam()
                t = TarFile.open(tmpname, "w:bz2")
                t.add(self.selected_dir)
                t.close()
                os.rename(tmpname, fileChooserDialog.get_filename())
                self.recursive_delete(self.selected_dir)
            elif response == gtk.RESPONSE_CANCEL:
                pass
            fileChooserDialog.destroy()

    def move_clicked(self, widget):
        if not (self.selected_dir is None):
            fileChooserDialog = gtk.FileChooserDialog("Mover para", self.wTree.get_widget("dc_gui"), gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
            response = fileChooserDialog.run()
            if response == gtk.RESPONSE_OK:
                os.rename(self.selected_dir, fileChooserDialog.get_filename() + os.sep + self.selected_dir.split(os.sep)[-1])
            elif response == gtk.RESPONSE_CANCEL:
                pass
            fileChooserDialog.destroy()
    
if __name__ == "__main__":
    smg = DiskCleanGUI()
    gtk.main()