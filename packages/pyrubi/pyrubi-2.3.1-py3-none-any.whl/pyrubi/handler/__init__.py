from websocket import create_connection
from json import dumps, loads
from ..servers import get_server
from ..cryption import cryption5
from threading import Thread
from time import sleep

class handler:

    def __init__(self, auth):
        self.crypto = cryption5(auth) if auth else None
        self.auth = auth
        self.hs_data = {
            'api_version': '5',
            'auth': auth,
            'method': 'handShake'
        }
        del auth
    
    def hand_shake(self):
        global ws
        print('connecting to the web socket...')
        ws = create_connection(get_server('socket'))
        ws.send(dumps(self.hs_data))
        ws.recv()
        ws.send(dumps({}))
        Thread(target=self.keep_hand_shake_alive).start()
        print('connected !')
        while True:
            try:
                recv = loads(ws.recv())
                if recv != {"status":"OK", "status_det":"OK"}:
                    if recv['type'] == 'messenger':
                        yield loads(self.crypto.decrypt(recv['data_enc']))
            except:
                ws.close()
                ws = create_connection(get_server('socket'))
                ws.send(dumps(self.hs_data))
                continue
    
    def keep_hand_shake_alive(self):
        while True:
            sleep(60)
            ws.send(dumps({}))
            ws.recv()