#!/usr/bin/env python

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
    
class SendMessageGUI:
    """This is a GUI for the SendMessage application"""

    def __init__(self):
                
        #Set the Glade file
        self.gladefile = _r("ms_gui.glade")  
        self.wTree = gtk.glade.XML(self.gladefile) 
                 
        #Create our dictionary and connect it
        dic = { "on_cancel_clicked" : self.cancel_clicked,
                "on_sendMessage_clicked" : self.sendMessage_clicked,
                "on_dialog1_destroy" : gtk.main_quit }
        self.wTree.signal_autoconnect(dic)
        
    def cancel_clicked(self, widget):
           print "Hello World!"
    
    def sendMessage_clicked(self, widget):
           print "Hello World!"
            
if __name__ == "__main__":
    smg = SendMessageGUI()
    gtk.main()