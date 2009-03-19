import utils
from utils import result_out
from subprocess import call

FORWARD_APP = '/usr/local/sbin/pywebapp-forward'

def forward_submit(req, form):
    login = form.getfirst('login')
    password = form.getfirst('password')
    email = form.getfirst('forward')
    result = utils.pam_login(login, password)
    if result.type == utils.PAM_OK:
        call_result = call([FORWARD_APP, login] + email.split())
        if call_result == 0:
            result_out(req, "Operation Successful!");
        else:
            result_out(req, "ERROR: Code " + str(call_result));
    elif result.type == utils.PAM_ERROR:
        result_out(req, "Could not authenticate: " + result.msg)
    else:
        result_out(req, "ERROR! Internal PAM failure.")

def forward_page(req):
    req.write("""
            <html>
            <body>
            <form name="forward" action="forward.py" method="POST">
            <div align="center"><br>
            <input type="hidden" name="app" value="forward"><br>
            <input type="hidden" name="submit" value="true"><br>
            Login: <input type="text" name="login" value="login"><br>
            Password: <input type="password" name="password" value=""><br>
            <br>
            <textarea cols="40" rows="5" name="forward">email@gmail.com</textarea><br>
            <input type="submit" value="submit"><br>
            </div>
            </form>
            </body>
            </html>
        """)
