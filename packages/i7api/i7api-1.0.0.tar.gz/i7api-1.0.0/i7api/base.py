import requests
import base64
class Storage:
    def __init__(self, url = "127.0.0.1"):
        self.url = url
        self.api = None
        self.password = None
    def signin(self, email=None, password=None):
        r = requests.post(f"http://{self.url}:2707/api",
                          json={"type": "signin", "username": email, "password": password})
        try:
            self.api = r.json()['api_key']
            self.password = r.json()['api_password']
            return r.json()
        except:
            print(r.content)
            return r.content
    def signup(self, email=None, password=None):
        r = requests.post(f"http://{self.url}:2707/api",
                          json={"type": "signup", "username": email, "password": password})
        print("Enter the OTP in Terminal")
        try:
            self.api = r.json()['api_key']
            self.password = r.json()['api_password']
            return r.json()
        except:
            return r.content
    def upload(self, file=None):
        if self.api is not None and self.password is not None:
            f = open(file, "rb")
            data = f.read()
            f.close()
            data_b64 = base64.b64encode(data).decode()
            r = requests.post(f"http://{self.url}:2707/api", json={"type": "upload", "api_key": self.api,
                                                                 'api_password': self.password,
                                                                 "file_name": f.name,
                                                                 "bytes": data_b64})

            return r.json()
        else:
            print("First Login or Signup")
    def download(self,file_id, file_path=None):
        r = requests.post(f"http://{self.url}:2707/api", json={"type": "download", "api_key": self.api,
                                                               'api_password': self.password,
                                                               "file_id": file_id})
        f = open(file_path, "wb")
        data_bytes = base64.b64decode(r.json().get('base64', None))
        f.write(data_bytes)
        f.close()
    def delete(self, file_id):
        r = requests.post(f"http://{self.url}:2707/api", json={"type": "delete", "api_key": self.api,
                                                               'api_password': self.password,
                                                               "file_id": file_id})
        return r.json()
    def get_all(self):
        r = requests.post(f"http://{self.url}:2707/api", json={"type": "getallid", "api_key": self.api,
                                                               'api_password': self.password})
        print(r.json())
    def search(self, file_name):
        r = requests.post(f"http://{self.url}:2707/api", json={"type": "search", "api_key": self.api,
                                                               'api_password': self.password, "file_name": file_name})
        print(r.json())

