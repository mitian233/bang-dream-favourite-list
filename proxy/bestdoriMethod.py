import requests, json, os

def getPackageId(songId):
    if songId % 10 !=0:
        result = songId + (10 - songId % 10)
    else:
        result = songId
    return result

def getSongList():
    if not os.path.isfile('songList.json'):
        baseURL = 'https://bestdori.com/api/songs/all.5.json'
        r = requests.get(baseURL, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            with open('songList.json', 'w', encoding='UTF-8') as f:
                content = json.loads(r.content)
                f.write(json.dumps(content, indent=4, ensure_ascii=False))
                f.close()
    with open('songList.json', 'r', encoding='UTF-8') as f:
        content = json.load(f)
        f.close()
    return content

def downloadJacket(songId):
    apiBaseURL = 'https://bestdori.com/api'
    packageId = getPackageId(songId)
    r = requests.get(apiBaseURL + '/songs/'+str(songId)+'.json', headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        data = json.loads(r.text)
        jacketName = data['bgmFile']+'-jacket.png'
        if not os.path.exists('cache'):
            try:
                os.makedirs('cache')
            except OSError as e:
                return 'failed'
        if os.path.isfile("cache/"+jacketName):
            return jacketName
        else:
            _r = requests.get('https://bestdori.com/assets/jp/musicjacket/musicjacket' + str(
                packageId) + '_rip/assets-star-forassetbundle-startapp-musicjacket-musicjacket' + str(
                packageId) + '-' + str(jacketName))
            if _r.status_code == 200:
                with open("cache/"+jacketName, 'wb') as f:
                    f.write(_r.content)
                    f.close()
                return jacketName
            else:
                return 'failed'
    else:
        return 'failed'

def downloadFile(songId):
    apiBaseURL = 'https://bestdori.com/api'
    packageId = getPackageId(songId)
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
        return cache_path
    else:
        return 'failed'

#Todo: downloadJacketのcache機能を実装する

if __name__ == '__main__':
    getSongList()
    for i in range(1, 473):
        downloadFile(i)
        print(i)