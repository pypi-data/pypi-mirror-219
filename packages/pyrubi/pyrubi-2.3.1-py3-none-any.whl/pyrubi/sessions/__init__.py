import os
from json import loads, dumps

class sessions:

    def __init__(self):
        pass

    def cheack_session(self, session_name):
        return os.path.exists(f'{session_name}.pyrubi')
    
    def session_data(self, session_name):
        return loads(open(f'{session_name}.pyrubi', encoding='UTF-8').read())
        
    def create_session(self, session_name, session_data):
        open(f'{session_name}.pyrubi', 'w', encoding='UTF-8').write(dumps(session_data, indent=4))