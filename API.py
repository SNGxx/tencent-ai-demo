import requests
import time
from urllib import parse
import hashlib
import base64

class API():
    def __init__(self, base_path):
        self.url = 'https://api.ai.qq.com/fcgi-bin/'
        self.base_path = base_path
        self.app_key = 'xx'
        self.app_id = 123

    def face_age(self, pic_name, res_name):
        url = self.url + 'ptu/ptu_faceage'
        time_stamp = int(time.time());
        f = open(self.base_path + pic_name, 'rb')
        image_data = base64.b64encode(f.read()).decode("utf-8")
        f.close()
        params = {
            'app_id': self.app_id,
            'time_stamp': time_stamp,
            'nonce_str': 'fa577ce340859f9fe',
            'image': image_data
        }
        params.update({'sign': self.produce_sign(params)})
        try:
            response = requests.post(url, data=params)
            response_json = response.json()
        except Exception as e:
            print("出现异常！")
            return
        if response_json.get("ret") != 0:
            print(pic_name + "====>" +response_json.get("msg"))
            return
        res_image_str = response_json.get("data").get("image")
        res_image_data = base64.b64decode(res_image_str)
        file = open(self.base_path + res_name, 'wb')
        file.write(res_image_data)
        file.close()

    def face_detect(self, pic_name):
        url = self.url + 'face/face_detectface'
        time_stamp = int(time.time());
        f = open(self.base_path + pic_name, 'rb')
        image_data = base64.b64encode(f.read()).decode("utf-8")
        f.close()
        params = {
            'app_id': self.app_id,
            'time_stamp': time_stamp,
            'nonce_str': 'fa577ce340859f9fe',
            'image': image_data,
            'mode': 1
        }
        params.update({'sign': self.produce_sign(params)})
        try:
            response = requests.post(url, data=params)
            response_json = response.json()
        except Exception as e:
            print("出现异常！")
            return
        if response_json.get("ret") != 0:
            print("error code: %s" % response_json.get("ret"))
            print(pic_name + "====>" +response_json.get("msg"))
            return
        res_beauty = response_json.get("data").get("face_list")[0].get("beauty")
        print("%s 颜值=%s" % (pic_name, res_beauty))

    def produce_sign(self, params={}):
        uri_str = ''
        for key in sorted(params.keys()):
            uri_str += '%s=%s&' % (key, parse.quote(str(params[key]), safe=''))
        sign = uri_str + 'app_key=' + self.app_key
        md5 = hashlib.md5(sign.encode("utf-8"))
        sign = md5.hexdigest().upper()
        #print(sign)
        return sign
