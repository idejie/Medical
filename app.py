import json
import os

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__, static_folder='static')


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                _id = int(os.path.splitext(file)[0])
                L.append(_id)
    return L


DIR_P = 'static/data/user'
DIR_M = 'static/data/medicine'
DIR_YF = 'static/data/recipe'


def gen_p_id():
    L = file_name(DIR_P)
    return max(L) + 1


def gen_m_id():
    L = file_name(DIR_M)
    return max(L) + 1


def gen_yf_id():
    L = file_name(DIR_YF)
    return max(L) + 1


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


# 添加药品
@app.route('/add/yp', methods=['GET', 'POST'])
def add_yp():
    if request.method == "GET":
        return render_template('yaopin.html')
    else:
        name = request.form['name']
        func = request.form['func']
        desc = request.form['desc']
        m_id = gen_m_id()
        yp = {
            'id': m_id,
            'name': name,
            'func': func,
            'desc': desc
        }
        yp_f = os.path.join(DIR_M, str(m_id) + '.json')
        with open(yp_f, 'w', encoding='utf8') as f:
            json.dump(yp, f, ensure_ascii=False)
        return render_template('yaopin.html', msg='药品【' + name + '】已添加。')


# 查询药品
@app.route('/query/yp', methods=['GET', 'POST'])
def query_yp():
    if request.method == "GET":
        return render_template('query_yp.html')
    else:
        all_ = request.form['all']
        name = request.form['name']
        func = request.form['func']
        desc = request.form['desc']

        data = []
        for root, dirs, files in os.walk(DIR_M):
            for file in files:
                file = os.path.join(DIR_M, file)
                with open(file, 'r', encoding='utf8') as f:
                    yp = json.load(f)
                    if all_ == "true":
                        data.append(yp)
                    elif (name is not '' and name in yp.get('name', '')) \
                            or (func is not '' and func in yp.get('func', '')) \
                            or (desc is not '' and desc in yp.get('desc', '')):
                        data.append(yp)
            res = {'data': data}
        return jsonify(res)


# 删除药品
@app.route('/del/yp', methods=['GET', 'POST'])
def del_yp():
    m_id = request.args.get('mid')
    print(m_id)
    yp_f = os.path.join(DIR_M, str(m_id) + '.json')
    with open(yp_f, 'r', encoding='utf8') as f:
        yp = json.load(f)
    name = yp.get('name', '')
    try:
        os.remove(yp_f)
        print(yp_f, "已删除")
        return render_template('result.html', msg='药品【' + str(name) + '】,id【' + m_id + '】已删除。')
    except OSError as e:
        return render_template('result.html', msg=str(e))


# 修改药品
@app.route('/detail/yp', methods=['GET', 'POST'])
def detail_yp():
    if request.method == 'GET':
        m_id = request.args.get('mid')
        yp_f = os.path.join(DIR_M, str(m_id) + '.json')
        with open(yp_f, 'r', encoding='utf8') as f:
            yp = json.load(f)
        return render_template('detail_yp.html', yp=yp)
    else:
        m_id = request.form['mid']
        print(m_id)
        name = request.form['name']
        func = request.form['func']
        desc = request.form['desc']
        yp = {
            'id': m_id,
            'name': name,
            'func': func,
            'desc': desc
        }
        yp_f = os.path.join(DIR_M, str(m_id) + '.json')
        with open(yp_f, 'w', encoding='utf8') as f:
            json.dump(yp, f, ensure_ascii=False)
        return render_template('result.html', msg='药品【' + name + '】,id【' + str(m_id) + '】修改。')


# 增加药方
@app.route('/add/yf', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'GET':
        return render_template('yaofang_add.html', msg='')
    else:
        print(request.form)
        name = request.form['name']
        yf = request.form['yf']
        yf_id = gen_yf_id()
        yaofang = {
            "id": yf_id,
            "name": name,
            "zz": "",
            "cases": [
                {'zz': "", 'yf': yf}
            ]
        }
        yf_f = os.path.join(DIR_YF, str(yf_id) + '.json')
        with open(yf_f, 'w', encoding='utf8') as f:
            json.dump(yaofang, f, ensure_ascii=False)
        return render_template('yaofang_add.html', msg='ss')


# 查询药方
@app.route('/query/yf', methods=['GET'])
def query_recipe():
    zz = request.args.get('zz')
    if not zz:
        return jsonify({'data': []})
    data = []
    for root, dirs, files in os.walk(DIR_YF):
        for file in files:
            file = os.path.join(DIR_YF, file)
            print(file)
            with open(file, 'r', encoding='utf8') as f:
                yf = json.load(f)
                if zz in yf.get('zz'):
                    data.append(yf)
        res = {'data': data}
        print(res)
    return jsonify(res)


@app.route('/detail', methods=['GET'])
def detail():
    p_id = request.args.get('p_id')
    p_f = os.path.join(DIR_P, p_id + '.json')
    with open(p_f, 'r', encoding='utf8') as f:
        data = json.load(f)

    return render_template('detail_br.html', data=data, p_id=p_id)


# 增
@app.route('/add/br', methods=['GET', 'POST'])
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
            json.dump(person, f, ensure_ascii=False)
        return redirect(url_for('detail', p_id=p_id))
    else:
        return render_template('person.html')


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
        json.dump(data, f, ensure_ascii=False)
    return redirect(url_for('detail', p_id=p_id))


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


@app.route('/query/zz', methods=['GET'])
def query_zz():
    return render_template('zz.html')


if __name__ == '__main__':
    app.run()
