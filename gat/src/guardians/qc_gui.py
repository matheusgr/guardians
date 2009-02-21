#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade    
from resource import find_resource as _r
import qc_model

class QuotaCheckGUI:
    """QuotaChecking GUI"""

    def __init__(self, model):
        self.qc_model = model
        
        #Set the Glade file
        self.gladefile = _r("qc_gui.glade")
        self.wTree = gtk.glade.XML(self.gladefile) 
                 
        #Create our dictionary and connect it
        dic = { "on_clean_disk_clicked" : self.clean_disk,
                "on_continue_login_clicked" : self.continue_login,
                "on_window1_destroy" : gtk.main_quit }
        self.wTree.signal_autoconnect(dic)
        
        # Update VBOX with disk quotas
        vbox2 = self.wTree.get_widget('vbox2')
        for box in self.create_disks_hbox():
            vbox2.pack_start(box, False, False, 0)
        vbox2.show()

    # Clean disk button callback
    def clean_disk(self, widget):
        print "button CD was pressed"

    # Continue login button callback
    def continue_login(self, widget):
        print "button CL was pressed"

    # Create a box for all disks
    def create_disks_hbox(self):
        quotas = self.qc_model.getQuota()
        result = []
        for quota in quotas:
            host = quota[0]
            disk = quota[1] 
            if quota[2] == qc_model.STATUS_OK:
                hardlimit = float(quota[5])
                curblocks = float(quota[7])
                result.append(self.create_disk_hbox(host + ':' + disk, quota[2], curblocks/hardlimit))
            else:
                result.append(self.create_disk_hbox(host + ':' + disk, quota[2]))
        return result

    # Create a box for each disk/use
    def create_disk_hbox(self, label_text, status, use_value=0):
        box = gtk.HBox(False, 0)
        
        label = gtk.Label(label_text)
        label.show()
        box.pack_start(label, True, False, 10)
        
        if status == qc_model.STATUS_OK:
            use = gtk.ProgressBar()
            use.set_fraction(use_value)
            use.set_text(str((int) (use_value * 100)) + '%')
            use.show()
            box.pack_start(use, True, True, 0)
    
            if use_value < 0.75:
                file = _r('green.png')
            elif use_value > 0.95:
                file = _r('red.png')
            else:
                file = _r('yellow.png')
            image = gtk.Image()
            image.set_from_file(file)
            image.show()
            box.pack_start(image, False, False, 10)
        else:
            use = gtk.ProgressBar()
            use.set_fraction(0)
            use.set_text('Inacessivel')
            use.show()
            box.pack_start(use, True, True, 0)
        box.show()
        return box
            
if __name__ == "__main__":
    QuotaCheckGUI(qc_model.QuotaCheckModelTest())
    gtk.main()