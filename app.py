import json
import os

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                _id = int(os.path.splitext(file)[0])
                L.append(_id)
    return L


DIR_P = 'static/data'


def gen_p_id():
    L = file_name(DIR_P)
    return max(L) + 1


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/detail', methods=['GET'])
def detail():
    p_id = request.args.get('p_id')
    p_f = os.path.join(DIR_P, p_id + '.json')
    with open(p_f, 'r', encoding='utf8') as f:
        data = json.load(f)

    return render_template('detail.html', data=data, p_id=p_id)


# 增
@app.route('/add/person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        zz = request.form['zz']
        yf = request.form['yf']
        p_id = gen_p_id()
        person = {
            "name": name,
            "phone": phone,
            "cases": [
                {'zz': zz, 'yf': yf}
            ]
        }
        p_f = os.path.join(DIR_P, str(p_id) + '.json')
        with open(p_f, 'w', encoding='utf8') as f:
            json.dump(person, f)
        return redirect(url_for('detail', p_id=p_id))
    else:
        return render_template('person.html')


@app.route('/add/recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'GET':
        return render_template('recipe.html', msg='')
    else:
        zz = request.form['zz']
        yf = request.form['yf']
        p_id = gen_p_id()
        person = {
            "name": '',
            "phone": '',
            "cases": [
                {'zz': zz, 'yf': yf}
            ]
        }
        p_f = os.path.join(DIR_P, str(p_id) + '.json')
        with open(p_f, 'w', encoding='utf8') as f:
            json.dump(person, f)
        return render_template('recipe.html',
                               msg='成功新增一药方：症状为【' + person['cases'][0]['zz'] + '】,药方为【' + person['cases'][0]['yf'] + '】')


@app.route('/add/case', methods=['GET', 'POST'])
def add_case():
    p_id = request.form['p_id']
    zz = request.form['zz']
    yf = request.form['yf']
    p_f = os.path.join(DIR_P, str(p_id) + '.json')
    with open(p_f, 'r', encoding='utf8') as f:
        data = json.load(f)
    data['cases'].append({'zz': zz, 'yf': yf})
    with open(p_f, 'w', encoding='utf8') as f:
        json.dump(data, f)
    return redirect(url_for('detail', p_id=p_id))


# 删
@app.route('/del/person', methods=['POST'])
def del_person():
    return 'hello'


@app.route('/del/recipe', methods=['POST'])
def del_recipe():
    return 'hello'


@app.route('/del/case', methods=['POST'])
def del_case():
    return 'hello'


# 改
@app.route('/update/person', methods=['POST'])
def update_person():
    return 'hello'


@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    return 'hello'


@app.route('/update/case', methods=['POST'])
def update_case():
    return 'hello'


# 查
@app.route('/query/person', methods=['GET', 'POST'])
def query_person():
    if request.method == 'GET':
        return render_template('query_person.html')
    else:
        name = request.form['name']
        data = []
        for root, dirs, files in os.walk(DIR_P):
            for file in files:
                file_t = os.path.join(DIR_P, file)
                with open(file_t, 'r', encoding='utf8') as f:
                    name_t = json.load(f).get('name')
                    if name in name_t:
                        p_id = file.replace('.json', '')
                        data.append({'name': name_t, "p_id": p_id})
        res = {'data': data}
        return jsonify(res)


@app.route('/query/yf', methods=['GET'])
def query_recipe():
    zz = request.args.get('zz')
    if not zz:
        return jsonify({'data': []})
    data = []
    for root, dirs, files in os.walk(DIR_P):
        for file in files:
            file = os.path.join(DIR_P, file)
            with open(file, 'r', encoding='utf8') as f:
                cases = json.load(f).get('cases')
                for case in cases:
                    if zz in case['zz']:
                        data.append(case)
        res = {'data': data}
    return jsonify(res)


@app.route('/query/zz', methods=['GET'])
def query_zz():
    return render_template('zz.html')


if __name__ == '__main__':
    app.run()
