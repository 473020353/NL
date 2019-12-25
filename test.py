import requests
import time

url_pre = "127.0.0.1:1999"

requests.session().keep_alive = False

def get_device_info():
    ''' test al/api/getdevinfo '''
    url = url_pre + "getdevinfo"

    data = {'devid': '867725035999873', 'token': '12345'}
    print(requests.get(url, json=data).json())

    #data['devid'] = '4B0D000010FFFFFF'
    #print(requests.get(url, json=data).json())

    #data['devid'] = 'FFFFFF1000008875'
    #print(requests.get(url, json=data).json())

    #data['devid'] = '866971030425552'
    #print(requests.get(url, json=data).json())

    #data['devid'] = 'E830000010FFFFFF'
    #print(requests.get(url, json=data).json())


def get_device_state():
    ''' test al/api/getdevstate '''
    url = url_pre + "getdevstate"

    data = {'devid': '867725035999873', 'token': '12345'}
    print(requests.get(url, json=data).json())

    data['devid'] = '865352034085059'
    print(requests.get(url, json=data).json())

    data['devid'] = 'E830000010FFFFFF'
    print(requests.get(url, json=data).json())

    data['devid'] = '866971030425552'
    print(requests.get(url, json=data).json())

    data['devid'] = '4B0D000010FFFFFF'
    print(requests.get(url, json=data).json())


def get_regulatory():
    ''' test al/api/getdevinfo '''
    url = url_pre + "getregulatory"

    data = {'userid': '1624047198567291', 'token': '12345'}
    print(requests.get(url, json=data).json())

    data['userid'] = '123443'
    print(requests.get(url, json=data).json())


def auth_regulatory():
    url = url_pre + "regulatory/auth"

    data = {"userid": "1624047198567291", 'token': '12345'}
    print(requests.get(url, json=data).json())

    data['userid'] = '123'
    print(requests.get(url, json=data).json())


def get_applycode():
    url = url_pre + "applycode"
    data = {"userid": "2343432432", "token": "234234"}
    print(requests.get(url, json=data).json())


def test_get_warning():
    url = url_pre + "getwarning"
    data = {"devids": ["E830000010FFFFFF", "E830000010FFFFFF"], "time": "2019-01-01 00:00:00"}
    print(requests.get(url, json=data).json())


def test_verify():
    url = url_pre + "device/verify"
    data = {"devid": "E830000010FFFFFF", "token": "2019-01-01 00:00:00"}
    print(requests.get(url, json=data).json())

    data['devid'] = '123'
    print(requests.get(url, json=data).json())


def test_get_count():
    url = url_pre + "device/getcount"
    data = {
        "devids": ["FFFFFF1000008E58"],
        "token": "2019-01-01 00:00:00"
    }
    print(requests.get(url, json=data).json())

def smoke_test():
    url= "http://127.0.0.1:8000/al/api/device/smoke/get-list"
    data = {
        "devid": ["FFFFFF1000008E58"],
        "token": "OTk5OTk5OTk5OWJlWW1SWjEwNDNiZDc5MTM3ODM2NTE2"
    }
    return requests.post(url, json=data).json()

def smoke_del():
    url= "http://127.0.0.1:8000/al/api/device/smoke/smoke_device_delete"
    data = {
        "devid": "FFFFFF1000008E9B",
        "token": "OTk5OTk5OTk5OWJlWW1SWjEwNDNiZDc5MTM3ODM2NTE2"
    }
    return requests.post(url, json=data).json()

def smoke_find():
    url = "http://127.0.0.1:8000/al/api/device/smoke/devid_get_id"
    data = {
          "devid": "FFFFFF1000008E9B",
          "token": "OTk5OTk5OTk5OWJlWW1SWjEwNDNiZDc5MTM3ODM2NTE2"
    }
    return requests.post(url,json=data).json()

def smoke_add():
    url = "http://127.0.0.1:8000/device/smoke/smoke_device_add"
    data = {
        "device_id": "FFFFFF1000008E9B",
        "category_id": "1111",
        "name": "设备FFFFFF1000008E9B",
        "address": "jn",
        "gps": "0,0",
        "voltage": "123",
        "temperature": "9",
        "state": 0,
        "created_at": 1000008,
        "updated_at": 1000008,
        "token": "OTk5OTk5OTk5OWJlWW1SWjEwNDNiZDc5MTM3ODM2NTE2"
    }
    return requests.post(url, json=data).json()


def smoke_edit():
    url = "http://127.0.0.1:8000/device/smoke/smoke_device_edit"
    data = {
        "devid": "FFFFFF1000008E9B",
        "category_id": "23232",
        "name": "设备FFFFFF1000008E9B",
        "address": "jn",
        "state": 0,
        "token": "OTk5OTk5OTk5OWJlWW1SWjEwNDNiZDc5MTM3ODM2NTE2"
    }
    return requests.post(url, json=data).json()



def login():
    url = "http://127.0.0.1:8000/login/index"
    data = {
        "devid": "FFFFFF1000008E9B",
        "category_id": "23232",
        "name": "设备FFFFFF1000008E9B",
        "address": "jn",
        "state": 0,
        "token": "OTk5OTk5OTk5OWJlWW1SWjEwNDNiZDc5MTM3ODM2NTE2"
    }
    return requests.post(url, json=data).json()


if __name__ == '__main__':
    print(login())
    # print(smoke_edit())
    # print(smoke_del())
    # get_device_info()
    # get_device_state()
    # get_regulatory()
    # auth_regulatory()
    # get_applycode()
    # test_push()
    # test_get_warning()
    # test_verify()
    #test_get_count()
