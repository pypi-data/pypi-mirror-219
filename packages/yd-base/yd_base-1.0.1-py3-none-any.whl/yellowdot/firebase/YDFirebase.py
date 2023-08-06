from firebase_admin import credentials, _apps


class YDFirebase(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(YDFirebase, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def get_instance():
        if not YDFirebase._instance:
            YDFirebase._instance = YDFirebase(YDFirebase._instance.servie_account_json_path)
        return YDFirebase._instance

    def __init__(self, servie_account_json_path: str):
        self.servie_account_json_path = servie_account_json_path
        self.firebaseInitialized = False

        try:
            cred = credentials.Certificate(self.servie_account_json_path)
            if not _apps or len(_apps) == 0:
                firebase_admin.initialize_app(cred)
            else:
                firebase_is_init = False
                for app in _apps:
                    if app.name == cred.project_id:
                        firebase_is_init = True
                        break
                if not firebase_is_init:
                    firebase_admin.initialize_app(cred)
            self.firebaseInitialized = True
        except Exception as e:
            print(e)
            self.firebaseInitialized = False

    def get_firebase_initialized(self):
        return self.firebaseInitialized
