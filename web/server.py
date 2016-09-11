#!/usr/bin/env python
from bottle import route, run, SimpleTemplate


@route('/courses')
def courses():
    tpl = SimpleTemplate(open("courses.tpl").read())
    return tpl.render()

run(host='0.0.0.0', port=8080, debug=True, reloader=True)
