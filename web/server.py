import os
import json
from bottle import route, run, SimpleTemplate, static_file, response, request
from model import Model

PATH = os.path.dirname(os.path.realpath(__file__))

def tpl(file_name, **kwargs):
    with open(os.path.join(PATH, file_name + ".tpl")) as tpl_file:
        template = SimpleTemplate(tpl_file.read())
        return template.render(
            **kwargs
        )
    return ""


model = Model()

@route('/courses')
def courses():
    items = []
    cur_aisle = ""
    for item_name, item_type in model.get_shop_list():
        if item_type == "aisle-name":
            cur_aisle = item_name
        elif item_type == "spacer":
            continue
        elif item_type.endswith("product"):
            items.append({"name": item_name,
                          "aisle": cur_aisle,
                          "simplified_name": model.remove_special_chars(item_name)})
        else:
            print("Unkown type: %s" % item_type)

    ret = tpl("header", title="Courses")
    ret += tpl("courses", items=items)
    ret += tpl("footer")
    return ret

@route('/courses/print/')
def courses_print():
    ret = tpl("header", title="Courses")
    ret += model.generate_html_user_list()
    ret += tpl("footer")
    return ret

@route('/api/user_list')
def get_user_list():
    ul = model.get_user_list()
    response.content_type = 'application/json'
    return json.dumps(ul)

@route('/api/shop_list')
def get_shop_list():
    sl = model.get_shop_list()
    response.content_type = 'application/json'
    return json.dumps(sl)

@route('/api/user_list/remove_item', method="POST")
def user_list_remove_item():
    item = request.json["item"]
    model.user_list_remove_item(item)
    model.save()

@route('/api/user_list/add_item', method="POST")
def user_list_add_item():
    item = request.json["item"]
    model.add_item(item)
    model.save()

@route('/api/user_list/update_comment', method="POST")
def update_product_comment():
    item = request.json
    model.update_product_comment(item["product"], item["comment"])
    model.save()

@route('/api/clear_list')
def clear_list():
    model.clear_user_list();
    model.save();

@route('/static/<path:path>')
def static(path):
    return static_file(path, root=os.path.join(PATH, 'static/'))

def run_server():
    run(host='0.0.0.0', server='cherrypy', port=8080, debug=True, reloader=True)
