import PAM

PAM_SERVICE = 'common-auth'

PAM_INTERNAL_ERROR = 1
PAM_ERROR = 2
PAM_OK = 0

class _PamConv:
    def __init__(self, password):
        self.password = password

    def __call__(self, auth, queryList, userData):
        resp = []
        for query, typ in queryList:
            if typ == PAM.PAM_PROMPT_ECHO_OFF: # PASS!
                resp.append((self.password, 0))
        return resp

class Result:
    def __init__(self, type, msg):
        self.type = type
        self.msg = msg
    def __str__(self):
    	return str(self.type) + ' ' + str(self.msg)

def pam_login(user, password):
    service = PAM_SERVICE
    auth = PAM.pam()
    auth.start(service)
    auth.set_item(PAM.PAM_USER, user)
    auth.set_item(PAM.PAM_CONV, _PamConv(password))
    try:
        auth.authenticate()
        auth.acct_mgmt()
    except PAM.error, resp:
        return Result(PAM_ERROR, resp[0]) # msg at 0
    except:
        return Result(PAM_INTERNAL_ERROR, '')
    else:
        return Result(PAM_OK, '')

def result_out(req, result):
    req.write(
    """
    <html>
    <body>
        <center>""" + result + \
    """ <br>
        <br>
        guardians-l@lcc.ufcg.edu.br
        </center>
    </body>
    </html>
    """
    )

