from ctypes import *
from operator import contains
import os
import json

def nr_sdk():    
    cur_path = os.path.dirname(__file__)
    dll_path = cur_path + "/lib/QLNRSdk.dll"
    api = cdll.LoadLibrary(dll_path)
    
    # init
    api.QLNR_Init()
    return api

_api = nr_sdk()

class NRSDK(object):
    def __init__(self) :
        self.ip = r'127.0.0.1'
        self.login_handle = c_void_p(None)
        self.connected = False

    def connect(self, ip=None):
        if ip:
            self.ip = ip
        #login
        server_ip = c_char_p(self.ip.encode('utf-8'))
        res = _api.QLNR_Login(server_ip, pointer(self.login_handle))
        self.connected = (res == 0)

        #log
        print("connect to app server[{}] {}.".format(self.ip, "success" if self.connect else "fail"))

        return self
        
    def close(self):
        print("logout from app server[{}]".format(self.ip))
        _api.QLNR_Logout(self.login_handle)
        self.connected = False
    
    # 未连接时，自动连接一次
    def _assert_connected(self):
        if self.connected:
            return
        
        self.connect()

    # 开始刺激
    def _start_stimulation(self, param, device=None):
        self._assert_connected()

        # 字符串格式统一为dict
        if isinstance(param, str):
            param = json.loads(param)

        s = json.dumps(param, indent=4)
        print(s)

        param_2 = c_char_p(s.encode('utf-8'))
        p_resp = (c_char * 512)(0)
        len = 512
        device_code = c_char_p(device.encode('utf-8')) if device else c_char_p(None)
        res = -1
        try:
            res = _api.QLNR_StartStimulationEx(self.login_handle, param_2, p_resp, len, device_code)
            print("start stimulation {}".format(resp_result(res)))
            if res != _RESP_SUCCESS:
                print(p_resp.value.decode("utf-8"))
        except Exception as e:
            print(e)
    
        return _SUCCESS if res == _RESP_SUCCESS else _FAIL
        
    def _stop_stimulation(self, device=None):
        self._assert_connected()

        p_resp = (c_char * 512)(0)
        len = 512
        device_code = c_char_p(device.encode('utf-8')) if device else c_char_p(None)
        try:
            res = _api.QLNR_StopStimulationEx(self.login_handle, p_resp, len, device_code)
            print("stop stimulation {}".format(resp_result(res)))
            if res != _RESP_SUCCESS:
                print(p_resp.value.decode("utf-8"))
        except Exception as e:
            print(e)
        
        return _SUCCESS if res == _RESP_SUCCESS else _FAIL
        
    def _get_device_list(self):
        self._assert_connected()

        p_resp = (c_char * 512)(0)
        len1 = 512
        p_list = (c_char * 4096)(0)
        len2 = 4096
        res = -1
        try:
            res = _api.QLNR_GetDeviceListEx(self.login_handle, p_resp, len1, p_list, len2)
            print("get device list {}".format(resp_result(res)))
            if res == _RESP_SUCCESS:
                list = p_list.value.decode("utf-8")
                return json.loads(list)
            else:
                print(p_resp.value.decode("utf-8"))
        except Exception as e:
            print(e)
        
        return []

    def _set_wifi_config(self, ssid, skey, device=None):
        self._assert_connected()
        print(f"ssid:{ssid}, secret:{skey}: device:{device}")

        p_resp = (c_char * 512)(0)
        len = 512
        res = -1
        p_ssid = c_char_p(ssid.encode('utf-8')) if ssid else c_char_p(None)
        p_skey = c_char_p(skey.encode('utf-8')) if skey else c_char_p(None)
        p_device = c_char_p(device.encode('utf-8')) if device else c_char_p(None)
        try:
            res = _api.QLNR_SetDeviceWifiConfigEx(self.login_handle, p_ssid, p_skey, p_resp, len, p_device)
            print("set wifi config {} for device[{}]".format(resp_result(res), device))
            if res != _RESP_SUCCESS:
                print(p_resp.value.decode("utf-8"))
        except Exception as e:
            print(e)
        
        return _SUCCESS if res == _RESP_SUCCESS else _FAIL

    def _get_wifi_config(self, device=None):
        self._assert_connected()

        p_wifi_config = (c_char * 512)(0)
        wifi_config_len = 512
        p_resp = (c_char * 512)(0)
        len = 512
        res = -1
        p_device = c_char_p(device.encode('utf-8')) if device else c_char_p(None)

        ssid = None
        skey = None
        try:
            res = _api.QLNR_GetDeviceWifiConfigEx(self.login_handle, p_wifi_config, wifi_config_len, p_resp, len, p_device)
            print("get wifi config {} for device[{}]".format(resp_result(res), device))
            if res == _RESP_SUCCESS:
                wifi_config = p_wifi_config.value.decode("utf-8")
                print(wifi_config)
                if wifi_config.find( "currentssid") >= 0:
                    ssid = wifi_config["currentssid"]
                if wifi_config.find( "currentpassword") >= 0:
                    skey = wifi_config["currentpassword"]

            else:
                print(p_resp.value.decode("utf-8"))
            
        except Exception as e:
            print(e)
        
        return ssid, skey

_RESP_SUCCESS = 0
_SUCCESS = 1
_FAIL = 0

def resp_result(res):
    return 'success' if res == 0 else 'fail'

def show_result(res):
    return 'success' if res == 1 else 'fail'