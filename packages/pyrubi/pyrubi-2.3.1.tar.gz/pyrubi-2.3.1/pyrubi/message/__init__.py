class message:

    def __init__(self, data):
        self.data = data
        del data

    def chat_id(self):
        return self.data['message_updates'][0]['object_guid'] if 'message_updates' in self.data else self.data['object_guid']

    def author_id(self):
        return self.data['message_updates'][0]['message']['author_object_guid'] if 'message_updates' in self.data else self.data['last_message']['author_object_guid']

    def message_id(self):
        return self.data['message_updates'][0]['message_id'] if 'message_updates' in self.data else self.data['last_message']['message_id']

    def reply_to_message_id(self):
        return self.data['message_updates'][0]['message'].get('reply_to_message_id')

    def text(self):
        return str(self.data['message_updates'][0]['message'].get('text') if 'message_updates' in self.data else self.data['last_message'].get('text'))

    def chat_type(self):
        try:
            return self.data['message_updates'][0].get('type') if 'message_updates' in self.data else self.data['abs_object'].get('type')
        except:
            pass

    def author_type(self):
        return self.data['message_updates'][0]['message']['author_type'] if 'message_updates' in self.data else self.data['last_message']['author_type']

    def message_type(self):
        try:
            return self.data['message_updates'][0]['message'].get('type') if 'message_updates' in self.data else self.data['last_message'].get('type')
        except:
            pass

    def is_forward(self):
        return 'forwarded_from' in self.data['message_updates'][0]['message'].keys() if 'message_updates' in self.data else None
        
    def forward_type(self):
        if self.is_forward():
            return self.data['message_updates'][0]['message']['forwarded_from'].get('type_from') if 'message_updates' in self.data else None
        
    def forward_id(self):
        if self.is_forward():
            return self.data['message_updates'][0]['message']['forwarded_from'].get('object_guid') if 'message_updates' in self.data else None
        
    def forward_message_id(self):
        if self.is_forward():
            return self.data['message_updates'][0]['message']['forwarded_from'].get('message_id') if 'message_updates' in self.data else None

    def is_user_chat(self):
        return self.chat_type() == 'User'

    def is_group_chat(self):
        return self.chat_type() == 'Group'

    def is_channel_chat(self):
        return self.chat_type() == 'Channel'

    def chat_title(self):
        return str(self.data['show_notifications'][0].get('title') if 'show_notifications' in self.data else self.data['abs_object'].get('title', f"{self.data['abs_object']['first_name']} {self.data['abs_object']['last_name']}") if "abs_object" in self.data else None)

    def author_title(self):
        return self.data['chat_updates'][0]['chat']['last_message'].get('author_title', self.chat_title()) if 'message_updates' in self.data else self.data['last_message'].get('author_title', self.chat_title())

    def is_event(self):
        return 'event_data' in self.data['message_updates'][0]['message'].keys() if 'message_updates' in self.data else self.message_type() == 'Other'

    def event_type(self):
        if self.is_event():
            return self.data['message_updates'][0]['message']['event_data'].get('type') if 'message_updates' in self.data else None

    def event_id(self):
        if self.is_event():
            return self.data['message_updates'][0]['message']['event_data']['performer_object'].get('object_guid') if 'message_updates' in self.data else None
        
    def count_unseen(self):
        return self.data['chat_updates'][0]['chat'].get('count_unseen', '0') if 'message_updates' in self.data else None