from flask import Flask, request, send_file, abort
import json, requests, io, os
import bestdoriMethod as bm
app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False  # json出力のソートを無効化

def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return resp

app.after_request(after_request)

@app.route('/')
def indexRoute():  # put application's code here
    returnData = json.loads('{"message": "working"}')
    if request.args.get('name'):
        returnData['message'] = "Hello " + request.args.get('name')
    return returnData

@app.route('/songs')
def getSongList():
    raw = bm.getSongList()
    return raw

@app.route('/jacket/<int:songId>')
def getSongJacket(songId):
    apiBaseURL = 'https://bestdori.com/api'
    packageId = bm.getPackageId(songId)
    r = requests.get(apiBaseURL + '/songs/' + str(songId) + '.json', headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        data = json.loads(r.text)
        jacket_name = data['bgmFile'] + '-jacket.png'
        file_url = 'https://bestdori.com/assets/jp/musicjacket/musicjacket' + str(
            packageId) + '_rip/assets-star-forassetbundle-startapp-musicjacket-musicjacket' + str(
            packageId) + '-' + str(jacket_name)
        cache_dir = 'cache'
        cache_path = os.path.join(cache_dir, jacket_name)
        if not os.path.exists(cache_path):
            # 如果缓存文件不存在，从 URL 下载文件并保存到缓存文件夹中
            r = requests.get(file_url, headers={'User-Agent': 'Mozilla/5.0'})
            with open(cache_path, 'wb') as f:
                f.write(r.content)
                f.close()
        return send_file(cache_path, mimetype="image", as_attachment=False)
    else:
        return abort(404)

if __name__ == '__main__':
    app.run()