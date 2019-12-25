# -*- coding:utf-8 -*-
# @Time  : 2019-11-29 10:50:35
# @Author: 程继瑞
# @Description NB烟感MQTT模块
# @File  : nb_smoke_mqtt

import json
from apply.MqttConfig import MQTT
from apply import MqttClient
# from guyuaninfo.COMM.log import Logger, LOG
from apply.smoke.service.smoke_service import SmokeService
from apply.smoke.service.smoke_data_service import SmokeDataService
from apply.device_now_warning.service.device_now_warning_service import DeviceNowWarningService
from apply.manually_cancel_log.service.manually_canael_log_service import ManuallyCancelLogService
from apply.device_warning.service.device_warning_service import DeviceWarningService
from apply.screen_wechat_push.service.screen_wechat_service import PushWx
from apply.screen_user_device_bind.service.device_screen_user_device_service import DeviceScreenUserDeviceService
from apply.unknown_device.service.unknown_device_service import UnknownDeviceService
from apply.mp3.mp3_service.mp3_service import Mp3Service
from apply.RestUrlConfig import RestUrlConfig
# from guyuaninfo.AL.device_driver.nb_smoke.mysql.nbsmoke import Smoke,SmokeData,SmokeWarn,Mp3DB,UnknownDB
# from guyuaninfo.AL.device_driver.nb_smoke.mqtt.pushwx import PushWx
# from guyuaninfo.AL.device_driver.nb_smoke.mqtt.mp3 import Mp3
from guyuaninfo.AL.device_driver.nb_smoke.mqtt.config import config as cfg
# from guyuaninfo.AL.device_driver.nb_smoke.mqtt.push_screen import PushScreen, ScreenData
import requests,time

class NbSmokeState:
    #  不报警,正常上报00 # smoke报警消除11 #故障消除 12 #低电量消除13 #手动消除 sx
    normal_nbsmoke_state = 0
    # 烟感报警01
    smoke_warning_state = 1
    # 低电量03
    low_battery_level_warning_state = 3
    # 传感器故障 02
    sensor_warning_state = 4
state_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
class NBSmokeCommand:
    normal_nbsmoke_comm = '00'
    smoke_warning_comm = '01'
    sensor_warning_comm = '02'
    low_battery_level_warning_comm = '03'
    smoke_warning_cancle = '11'
    fault_cancle = '12'
    low_battery_level_cancle = '13'
    smoke_sx_comm = 'sx'

class NbSmokeMqtt():
    def __init__(self, va_topic, user, passwd):
        self.mqtt_username = user
        self.mqtt_userpass = passwd
        self._auth = {"username": user, "password": passwd}
        self.varx_topic = va_topic

    def receive_device_message(self):
        client = MqttClient.MqttClient(userName=self.mqtt_username, userPass=self.mqtt_userpass, host=MQTT.MQTTSERVER,
                                       port=MQTT.MQTTPORT)
        client.connect(self.device_message)
        client.subcribe(self.varx_topic)

    def device_message(self, msg):
        data = str(msg.payload, 'utf-8')
        data = json.loads(data)
        self.device_data_parser(data)

    #  数据解析
    def device_data_parser(self, data):
        smoke_state = data.get('state')
        time = data.get('datetime')
        device_id = data.get('devid')
        head = data.get('data')[0:4]
        #  手动消除
        if smoke_state == NBSmokeCommand.smoke_sx_comm:
            state = NbSmokeState.normal_nbsmoke_state
            self.device_manually_cancle_warning(data)
            warning_type = '手动消除'
            push_type = '0101'
            self.device_add_db(device_id, 'sx', data, time,warning_type,push_type)

        # 判断消息头是否为0401 0402 不是则不解析数据
        if head == MQTT.message_head_first or head == MQTT.message_head_second:
            # 当前烟感设备信息
            smoke_info = SmokeService().device_get_id(device_id)
            if smoke_info.get('category_id') is not None:
                if smoke_state == NBSmokeCommand.normal_nbsmoke_comm:
                    if smoke_info.get('state') == 0:
                        state = NbSmokeState.normal_nbsmoke_state
                        self.add_device_data(device_id,time,state,data)
                        DeviceNowWarningService().delete_now_warning(device_id)
                    else:
                        state = NbSmokeState.normal_nbsmoke_state
                        warning_type = '报警消除'
                        push_type = '0101'
                        self.device_add_db(device_id, state, data, time,warning_type,push_type)
                elif smoke_state == NBSmokeCommand.smoke_warning_comm:
                    state = NbSmokeState.smoke_warning_state
                    warning_type = '烟感报警'
                    push_type = '0101'
                    self.device_add_db(device_id, state, data, time,warning_type,push_type)
                elif smoke_state == NBSmokeCommand.sensor_warning_comm:
                    state = NbSmokeState.sensor_warning_state
                    warning_type = '传感器故障'
                    push_type = '0300'
                    self.device_add_db(device_id, state, data, time,warning_type,push_type)
                elif smoke_state == NBSmokeCommand.low_battery_level_warning_comm:
                    state = NbSmokeState.low_battery_level_warning_state
                    warning_type = '低电量'
                    push_type = '0200'
                    self.device_add_db(device_id, state, data, time,warning_type,push_type)
                elif smoke_state == NBSmokeCommand.smoke_warning_cancle:
                    state = NbSmokeState.normal_nbsmoke_state
                    warning_type = '烟感报警消除'
                    push_type = '0100'
                    self.device_add_db(device_id, state, data, time,warning_type,push_type)
                elif smoke_state == NBSmokeCommand.fault_cancle:
                    warning_type = '故障消除'
                    push_type = '0100'
                    state = NbSmokeState.normal_nbsmoke_state
                    self.device_add_db(device_id, state, data, time,warning_type,push_type)
                elif smoke_state == NBSmokeCommand.low_battery_level_cancle:
                    state = NbSmokeState.normal_nbsmoke_state
                    warning_type = '低电量消除'
                    push_type = '0100'
                    self.device_add_db(device_id, state, data, time,warning_type,push_type)
            else:
                data = {
                    'device_id': device_id,
                    'time': time
                }
                UnknownDeviceService().add_unknown_device(data)

    def device_add_db(self, device_id, state, data, time, warning_type, push_type):
        self.update_device_state(device_id, state)
        self.add_device_data(device_id, time,state, data)
        self.device_warning(device_id, time, state, warning_type,push_type)
        Mp3Service().create_mp3(device_id, time,state)

    def device_warning(self, device_id, time, state, warning_type,push_type):
        smoke_info = SmokeService().device_get_id(device_id)
        content = "报警通知： 烟感监测设备 ：{} 报警地址：{} 报警时间:{}".format(warning_type, smoke_info.get('address'), time)
        data = {
            'device_id': device_id,
            'address': smoke_info.get('address'),
            'name': smoke_info.get('name'),
            'category_id': smoke_info.get('category_id'),
            'type': 0,
            'time': time,
            'content': content
        }

        if not state:
            DeviceWarningService().device_warning_add(data)
            PushWx().pushwx(device_id, time, push_type,'')
        else:
            device_type = 'x0'
            if state == 'sx':
                device_type = 's0'
            data['type'] = device_type
            DeviceWarningService().device_warning_add(data)
            DeviceNowWarningService().delete_now_warning(device_id)
            PushWx().pushwx(device_id, time, push_type,'')
        push_list = DeviceScreenUserDeviceService().get_bind(device_id)
        for push in push_list:
            push['info'] = content
            res = PushWx().push_screen(state='0', **push)



    def device_manually_cancle_warning(self, data):
        device_id = data.get('devid')
        smoke_info = SmokeService().device_get_id(device_id)
        split_data=data.get('data').split(',')
        data = {
                'userid': split_data[1],
                'name': smoke_info.get('name'),
                'content': data.get('data'),
                'time': data.get('datetime'),
                'remark': split_data[3],
                'device_id': device_id,
                'address': smoke_info.get('address'),
                'type': 0
                }
        ManuallyCancelLogService().manually_cancel_log_add(data)

    # 声光报警
    def exe_sl_alarm(self,devid,smoke_state):
        data = {
            'devid': devid,
            'state': smoke_state,
            'token': 'OTk5OTk5OTk5OWI5VVRQODY2ZGIzZDJjZTNiZWNhMTk='
        }
        req = requests.post('http://server.guyuaninfo.com:8000/al/api/sl_alarm/notify', json=data, timeout=60).json()
        print(req)

    # 修改主表状态
    def update_device_state(self, device_id,  smoke_state):
        smoke_info = SmokeService().device_get_id(device_id)
        data = {
            'state': smoke_state
        }
        SmokeService().update_smoke_device(smoke_info,data)

    # 添加数据表
    def add_device_data(self, device_id, time, smoke_state, data):
        voltage = NbSmokeAnalys.hex_to_short(data)
        voltage = "{}%".format(voltage)
        data = {
                'device_id': device_id,
                'state': smoke_state,
                'time': time,
                'voltage': voltage,
                'temperature': "",
        }
        SmokeDataService().add_smoke_device_data(data)

    def template_content(self,data: dict, state: str):
        state_map = {
            "00": "设备正常",
            "01": "烟感报警",
            "02": "传感器故障",
            "03": "低电量",
            "11": "烟感报警消除",
            "12": "故障消除",
            "13": "低电量消除",
            "sx": "手动消除"
            }
        voltage=NbSmokeAnalys.hex_to_short(data)
        return (f"烟感监测设备：{state_map.get(state, '')}   "
                f"设备剩余电量：{voltage}% ")


class NbSmokeAnalys():
    @staticmethod
    def is_warning(smoke_state):
        if smoke_state == NbSmokeState.sensor_warning_state or smoke_state == NbSmokeState.low_battery_level_warning_state or smoke_state==NbSmokeState.smoke_warning_state:
            return True
        return False

    @staticmethod
    def hex_to_short(data):
        # PL层data数据大小端转换
        voltage_data = data.get('data')[4:6]
        result = requests.post(
            RestUrlConfig.short_address,
            json={"tool": "lhex2short",
                  "param": voltage_data,
                  "token": "OTk5OTk5OTk5OWJlWW1SWjEwNDNiZDc5MTM3ODM2NTE2"}).json()
        return result.get('data')



# if __name__ == '__main__':
#     test()
    # va.update_mp3_warning('867726033067150','2019-04-22 15:20:45',[2])
    # va.receive_device_message()
