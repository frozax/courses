import os
from bottle import route, run, SimpleTemplate, static_file
from model import Model

PATH = os.path.dirname(os.path.realpath(__file__))

def tpl(file_name, **kwargs):
    with open(os.path.join(PATH, file_name + ".tpl")) as tpl_file:
        template = SimpleTemplate(tpl_file.read())
        return template.render(
            **kwargs
        )
    return ""


@route('/courses')
def courses():
    model = Model()

    items = [{"name": "Yaourts", "aisle": 50}]

    ret = tpl("header", title="Courses")
    ret += tpl("courses", items=items)
    ret += tpl("footer")
    return ret

@route('/static/<path:path>')
def static(path):
    return static_file(path, root=os.path.join(PATH, 'static/'))

def run_server():
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
