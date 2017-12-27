# coding: utf-8

from datetime import datetime

from flask import Flask, jsonify, make_response, request, abort
from flask import render_template
from flask_sockets import Sockets

from views.todos import todos_view
import leancloud
from utils import lc_dump


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
      block_start_string='{%',
      block_end_string='%}',
      variable_start_string='((',
      variable_end_string='))',
      comment_start_string='{#',
      comment_end_string='#}',
    ))


app = CustomFlask(__name__)
# app = Flask(__name__)
sockets = Sockets(app)

# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')

# 注册 API 蓝本
from api_1_0 import api as api_1_0_blueprint
from api_1_1 import api as api_1_1_blueprint
app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
app.register_blueprint(api_1_1_blueprint, url_prefix='/api/v1.1')


Prod = leancloud.Object.extend('Prod')
Cate = leancloud.Object.extend('Cate')


# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/time')
def time():
    return str(datetime.now())


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


# 静态文件的放置路径，可根据实际情况设置，这里设置为默认路径：'./static/'
# app = Flask(__name__, static_url_path='')

#模拟json数据
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

#设置根路由
@app.route('/')
def root():
    return app.send_static_file('index.html')


#GET方法api
@app.route('/todo/api/tasks', methods=['GET'])
def getTasks():
    tasks = Prod.query.limit(10).find()
    return jsonify(tasks=[lc_dump(task) for task in tasks])


@app.route('/goods', methods=['GET'])
def get_goods():
    tasks = Prod.query.limit(10).find()
    goods = [lc_dump(task) for task in tasks]
    data = {
        'data': goods,
        'code': 0
    }
    return jsonify(data)


@app.route('/goods/inner_category', methods=['GET'])
def get_cates():
    cates = Cate.query.find()
    categories = [lc_dump(cate) for cate in cates]
    data = {
        'data': categories,
        'code': 0
    }
    return jsonify(data)



#POST方法API，添加数据项
@app.route('/todo/api/addTask', methods=['POST'])
def add_task():
    if request.json['title'] == "":
        abort(400)
    task = {
        'id' : tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description' : request.json.get('description', ""),
        'done' : False
        }
    tasks.append(task)
    return jsonify({'tasks': tasks}), 201


#POST方法API，删除数据项
@app.route('/todo/api/deleteTask', methods=['POST'])
def delete_task():
    task_id = request.json['id']
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
    return jsonify({'tasks': tasks}), 201


#404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)

