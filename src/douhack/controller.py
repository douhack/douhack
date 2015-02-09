import cherrypy
from blueberrypy.template_engine import get_template

# decorator. apply to certain methods after 'exposed'
def render(template = None, page_id = None, ):
    def dec(func):
        @functools.wraps(func)
        def wrapper(obj):
            '''
            obj is an object with context of func
            '''
            tmpl = get_template(template)
            return tmpl.render(webpage = { 'content': func(obj), 'menu': obj.menu if hasattr(obj, 'menu') else menu, 'current_page': page_id })
        return wrapper
    return dec

class Root(object):
    @cherrypy.expose
    def default(self):
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def index(self):
        tmpl = get_template("index.html")
        return tmpl.render()
