import smtplib

class Mail:
    
    default_port_smtp = 25
    
    def __init__(self,smtp_server, remitter, receiver, subject, body):
        self.address_server = smtp_server
        self.rem = remitter
        self.rec = receiver
        self.subj = subject
        self.body = body
    
    def make_message(self):
        return 'From: '+self.rem+'\nTo: '+self.rec+'\nSubject: '+self.subj+'\n'+self.body
    
    def connect_server(self):
        self.server = smtplib.SMTP(self.address_server,self.default_port_smtp)               

    def disconnect_server(self):
        self.server.close()
    
    def send_mail(self):
        self.connect_server()
        self.server.sendmail(self.rem, self.rec, self.make_message())
        self.disconnect_server()

class MailToGuardians(Mail):
    def __init__(self,remitter,body):
        Mail.__init__(self,'lcc.ufcg.edu.br',remitter,'guardians-l@lcc.ufcg.edu.br','[Guardians] chat - lcc',body)