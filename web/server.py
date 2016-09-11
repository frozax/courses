#!/usr/bin/env python
from bottle import route, run, SimpleTemplate, static_file

def tpl(file_name, **kwargs):
    template = SimpleTemplate(open(file_name + ".tpl").read())
    return template.render(
        **kwargs
    )


@route('/courses')
def courses():

    items = [{"name": "Yaourts", "aisle": 50}]

    ret = tpl("header", title="Courses")
    ret += tpl("courses", items=items)
    ret += tpl("footer")
    return ret

@route('/static/<path:path>')
def static(path):
    return static_file(path, root='static/')

run(host='0.0.0.0', port=8080, debug=True, reloader=True)
