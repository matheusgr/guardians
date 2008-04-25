#!/usr/bin/env python
from guardians import dc_model

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
        dic = { "on_tree_row_collapsed" : self.tree_row_collapsed,
                "on_tree_row_expanded" : self.tree_row_expanded,
                "on_dialog1_destroy" : gtk.main_quit }
        self.wTree.signal_autoconnect(dic)
        diskView = self.prepare_disk_view()
        diskTree = self.prepare_disk_tree(diskView)
        r = dc_model.DiskCleanModel(".").get_list()
        self.build_tree(r, None, diskTree, 150000)
        
    def prepare_disk_view(self):
        diskView = self.wTree.get_widget("tree")
        
        column_file = gtk.TreeViewColumn("Diretorio/Arquivo", gtk.CellRendererText(), text=0)
        column_file.set_sort_column_id(0)
        column_file.set_sort_indicator(True)
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
                
    def tree_row_collapsed(self, widget, something, blah):
           print (widget, something, blah)
    
    def tree_row_expanded(self, widget, something, blah):
           print (widget, something, blah)
            
if __name__ == "__main__":
    smg = DiskCleanGUI()
    gtk.main()