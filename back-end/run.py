from flask import Flask, request
import json
import cfg
import util

# 实例化
app = Flask(__name__, template_folder='../front-end', static_folder='../front-end')

@app.route('/hi')
def hi():
    return 'hi~'

# api接口前缀
apiPrefix = '/api/v1/'

##################  Stock接口  ##################

@app.route(apiPrefix + 'search', methods=['POST'])
def searchQuery():
    query = request.get_data(as_text=True)
    query = json.loads(query)['query']
    print("后端数据：", query)
    result = util.search_by_token(query)
    with open('./tmp_query.txt', 'w') as f:
        f.write(query)
    with open('./tmp_res.json', 'w') as f:
        json.dump(result, f)
    re = {'code': 0, 'message': "成功"}
    return json.dumps(re)

@app.route(apiPrefix + 'list')
def getList():
    with open('./tmp_res.json', 'r') as f:
        re = json.load(f)
    # print(re)
    return json.dumps(re)

@app.route(apiPrefix + 'feedback', methods=['POST'])
def feedback():
    feedback = request.get_data(as_text=True)
    feedback = json.loads(feedback)['feedback'].split()
    print("后端数据：", feedback)
    with open('./tmp_query.txt', 'r') as f:
        query = f.read()
    with open('./tmp_res.json', 'r') as f:
        matches = json.load(f)
    with open('./dataset.txt', 'a+') as f:
        for idx in feedback:
            f.write(query + ' ' + matches[int(idx) - 1]['match'] + '\n')
    re = {'code': 0, 'message': "成功"}
    return json.dumps(re)


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=False, port=3001)