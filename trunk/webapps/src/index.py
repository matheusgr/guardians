from mod_python import apache, util
import forward

SUBMIT = 'submit'

def error_handler(req, form):
    req.write('Unknown app')

def forward_handler(req, form):
    if form.has_key(SUBMIT):
        forward.forward_submit(req, form)
    else:
        forward.forward_page(req)

HANDLERS = { 'forward' : forward_handler }

def handler(req):
    form = util.FieldStorage(req)
    req.content_type = 'text/html'
    if form.has_key('app'):
        app = form.getfirst('app')
        HANDLERS.get(app, error_handler)(req, form)
    return apache.OK