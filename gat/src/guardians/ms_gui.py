#!/usr/bin/env python

import sys, os
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
    
class SendMessageGUI:
    """This is a GUI for the SendMessage application"""

    def __init__(self):
                
        #Set the Glade file
        self.gladefile = _r("ms_gui.glade")  
        self.wTree = gtk.glade.XML(self.gladefile)
        
        # accessing windows
        self.principalWindow = self.wTree.get_widget('sMessageWindow')
        self.dialogWindow = self.wTree.get_widget('waitWindow')
        
        # accessing widgets => principalWindow
        self.txtMessage = self.wTree.get_widget('txtMessage')
        self.btnCancel = self.wTree.get_widget('cancel')
        self.btnSMessage = self.wTree.get_widget('sendMessage')
        
        # accessing widgets => dialogWindow
        self.lblInformation = self.wTree.get_widget('lblInformation')
        self.btnOk = self.wTree.get_widget('btnOk')
                 
        #Create our dictionary and connect it
        dic = { "on_cancel_clicked" : self.cancel_clicked,
                "on_sendMessage_clicked" : self.sendMessage_clicked,
                "on_dialog1_destroy" : gtk.main_quit }
        self.wTree.signal_autoconnect(dic)
        
    def cancel_clicked(self, widget):
        gtk.main_quit()
           
    
    def sendMessage_clicked(self, widget):
        messageBuffer = self.txtMessage.get_buffer()
        mailBody = messageBuffer.get_text(messageBuffer.get_start_iter(), messageBuffer.get_end_iter())
        
        # making and sending mail        
        mail = chat.MailToGuardians(self.get_remitter(), mailBody)
        sent = mail.send_mail()
                    
        self.clean_message()
        
    def clean_message(self):
        self.txtMessage.get_buffer().set_text('')
        
    def get_remitter(self):
        return os.getuid() + '@lcc.ufcg.edu.br'
            
if __name__ == "__main__":
    smg = SendMessageGUI()
    gtk.main()