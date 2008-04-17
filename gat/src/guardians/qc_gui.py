#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import qc_model

# GUI description:
# disk1 use situation
# disk2 use situation
# ...
# run clean disk | continue login
#
# Where:
# - "disk" is a label
# - "use" is a progress bar
# - "situation" is a picture (like a semaphore light)
# - "run clean disk" is a button
# - "continue login" is another button
class QuotaCheckGUI:

    # Clean disk button callback
    def clean_disk(self, widget, data):
        print "button %s was pressed" % data

    # Continue login button callback
    def continue_login(self, widget, data):
        print "THE button %s was pressed" % data

    # delete_event callback
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    # Create a box for all disks
    def create_disks_hbox(self):
        quotas = self.qc_model.getQuota()
        result = []
        for quota in quotas:
            if quota[2] == qc_model.STATUS_OK:
                host = quota[0]
                disk = quota[1] 
                hardlimit = float(quota[5])
                curblocks = float(quota[7])
                result.append(self.create_disk_hbox(host + ':' + disk, curblocks/hardlimit))
        # box = self.create_disk_hbox('Disk1', 0.99)
        return result

    # Create a box for each disk/use
    def create_disk_hbox(self, label_text, use_value):
        box = gtk.HBox(False, 0)
        
        label = gtk.Label(label_text)
        label.show()
        box.pack_start(label, True, False, 10)
        
        use = gtk.ProgressBar()
        use.set_fraction(use_value)
        use.set_text(str((int) (use_value * 100)) + '%')
        use.show()
        box.pack_start(use, True, True, 0)

        if use_value < 0.75:
            file = 'green.png'
        elif use_value > 0.95:
            file = 'red.png'
        else:
            file = 'yellow.png'
        image = gtk.Image()
        image.set_from_file(file)
        image.show()
        box.pack_start(image, False, False, 10)
        box.show()
        return box

    def __init__(self):
        self.qc_model = qc_model.QuotaCheckModel()
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Checagem de Cota")
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(10)

        # VBox
        self.vbox = gtk.VBox(True, 0)

        for box in self.create_disks_hbox():
            self.vbox.pack_start(box, False, False, 0)

        separator = gtk.HSeparator()
        separator.show()
        self.vbox.pack_start(separator, False, False, 0)

        # HBox - Buttons
        self.button_hbox = gtk.HBox(True, 10)
        
        self.clean_disk_button = gtk.Button("Limpeza de Conta")
        self.clean_disk_button.connect("clicked", self.clean_disk, "clean_disk")
        self.clean_disk_button.show()
        self.button_hbox.pack_start(self.clean_disk_button, True, True, 0)
        
        self.continue_login_button = gtk.Button("Continuar o login")
        self.continue_login_button.connect("clicked", self.continue_login, "continue_login")
        self.continue_login_button.show()
        self.button_hbox.pack_start(self.continue_login_button, True, True, 0)

        self.vbox.pack_start(self.button_hbox, False, False, 0)

        self.window.add(self.vbox)

        # The order in which we show the buttons is not really important, but I
        # recommend showing the window last, so it all pops up at once.
        self.button_hbox.show()
        self.vbox.show()
        self.window.show()

def main():
    gtk.main()

if __name__ == "__main__":
    hello = QuotaCheckGUI()
    main()
