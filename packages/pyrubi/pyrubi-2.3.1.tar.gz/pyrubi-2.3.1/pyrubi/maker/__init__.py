from ..servers import get_server
from urllib3 import PoolManager
from json import dumps, loads
from requests import  post

class maker:
    
    def __init__(self, send_auth, crypto):
        self.auth = send_auth
        self.crypto = crypto
        self.http = PoolManager()
        self.server = get_server('api')
        self.req_clients = {
            'web': {
                'app_name': 'Main',
                'app_version': '4.3.3',
                'platform': 'Web',
                'package': 'web.rubika.ir',
                'lang_code': 'fa'
            },
            'android': {
                'app_name': 'Main',
                'app_version': '3.3.2',
                'platform': 'Android',
                'package': 'ir.resaneh1.iptv',
                'lang_code': 'fa'
            }
        }
        self.raise_info = {
            'INVALID_AUTH': 'The Auth entered is invalid !',
            'NOT_REGISTERED': 'Method input is not registered !',
            'INVALID_INPUT': 'Invalid method input !',
            'TOO_REQUESTS': 'Too much request ! Your account has been suspended.'
        }
        del send_auth

    def method(self, method:str, data:dict, tmp:str=None, api_version:int=6):
        if tmp:
            from ..cryption import cryption6
            self.crypto = cryption6(tmp)
        data = {
            'api_version': str(api_version),
            'tmp_session' if tmp else 'auth': tmp if tmp else self.auth,
            'data_enc': self.crypto.encrypt(
                dumps({
                    'method': method,
                    'input': data,
                    'client': self.req_clients['web']
                })
            )
        }
        if str(api_version) == "6" and not tmp:
            data['sign'] = self.crypto.makeSignFromData(data['data_enc'])

        while True:
            result = self.http.request(
                'POST',
                self.server,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'Origin': 'https://web.rubika.ir',
					'Referer': 'https://web.rubika.ir/',
					'Host': self.server.replace('https://','').replace('/','')
                },
                body = dumps(data).encode(),
            )
            result = loads(self.crypto.decrypt(loads(result.data.decode('UTF-8'))['data_enc']))
            if result['status'] == 'OK':
                return result['data']
            elif result['status'] in ['ERROR_GENERIC', 'ERROR_ACTION']:
                raise ConnectionError(self.raise_info[result['status_det']])
            continue

    def _upload(self, url, data, headers):
        while True:
            req = post(url=url, data=data, headers=headers)
            if req.status_code != 200:
                print('This file cannot be uploaded ! Trying to upload again ...')
                continue
            return req.json()
        
    def _download(self, url, headers):
        while True:
            try:
                return self.http.request(method='POST', url=url, headers=headers, preload_content=False)
            except:
                print('This file cannot be downloaded ! Trying to download again ...')
                continue