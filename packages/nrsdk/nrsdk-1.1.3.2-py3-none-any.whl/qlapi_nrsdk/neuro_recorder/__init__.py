from ctypes import *
from ..nrsdk import NRSDK

class NeuroRecorder(NRSDK):
    # 直流刺激
    DC_STIM = 0
    # 交流刺激
    AC_STIM = 1
        
    # 开始刺激
    def stim_start(self, param, device=None):
        return self._start_stimulation(param, device)

    # 停止刺激
    def stim_stop(self, device=None):
        return self._stop_stimulation(device)

    # 设备列表
    def device_list(self):
        return self._get_device_list()

    # 设置wifi
    def set_wifi_config(self, ssid, skey, device=None):
        return self._set_wifi_config(ssid, skey, device)

    # 查询wifi
    def get_wifi_config(self, device=None):
        return self._get_wifi_config(device)

    # 刺激
    def __stim_start(self, channels_p, channels_n, current, duration, waveform, frequency=0, phase_pos=0, ramp_up=0, ramp_down=0, device=None):
        ch_num = len(channels_p) + len(channels_n)
        if ch_num == 0:
            print("请至少指定一个刺激通道！")
            return 0

        # 参数转换为范式格式，统一参数
        jsonParam = {}
        jsonParam["channels"] =  [{}] * ch_num
        jsonParam["params"] = [{}]
        jsonParam["params"][0]["channels"] = [{}] * ch_num
        i = 0
        for ch in channels_p:
            jsonParam["channels"][i] = {}
            jsonParam["channels"][i]["channel_id"] = int(ch)
            jsonParam["params"][0]["channels"][i] = {}
            jsonParam["params"][0]["channels"][i]["waveform"] = waveform
            jsonParam["params"][0]["channels"][i]["current"] = current
            jsonParam["params"][0]["channels"][i]["frequecy"] = int(frequency)
            jsonParam["params"][0]["channels"][i]["duration"] = int(duration)
            jsonParam["params"][0]["channels"][i]["ramp_up"] = int(ramp_up)
            jsonParam["params"][0]["channels"][i]["ramp_down"] = int(ramp_down)
            jsonParam["params"][0]["channels"][i]["phase_position"] = int(phase_pos)
            jsonParam["params"][0]["channels"][i]["channel_id"] = int(ch)
            i += 1
        
        for ch in channels_n:
            jsonParam["channels"][i] = {}
            jsonParam["channels"][i]["channel_id"] = int(ch)
            jsonParam["params"][0]["channels"][i] = {}
            jsonParam["params"][0]["channels"][i]["waveform"] = waveform
            jsonParam["params"][0]["channels"][i]["current"] = -current
            jsonParam["params"][0]["channels"][i]["frequecy"] = int(frequency)
            jsonParam["params"][0]["channels"][i]["duration"] = int(duration)
            jsonParam["params"][0]["channels"][i]["ramp_up"] = int(ramp_up)
            jsonParam["params"][0]["channels"][i]["ramp_down"] = int(ramp_down)
            jsonParam["params"][0]["channels"][i]["phase_position"] = int(phase_pos)
            jsonParam["params"][0]["channels"][i]["channel_id"] = int(ch)
            i += 1
            
        return self.stim_start(jsonParam, device)

    # 直流电刺激
    def dc_start(self, channels_p, channels_n, current, duration, ramp_up=0, ramp_down=0, device=None):
        print("dc stim start")

        return self.__stim_start(channels_p, channels_n, current, duration, Stimulator.DC_STIM, 0, 0, ramp_up, ramp_down, device)

    # 交流电刺激
    def ac_start(self, channels_p, channels_n, current, duration, frequency, phase_pos=0, ramp_up=0, ramp_down=0, device=None):
        print("ac stim start")
        if frequency <= 0:
            print("交流电刺激必须指定频率值(频率单位Hz，值为正整数)")
            return 0;

        return self.__stim_start(channels_p, channels_n, current, duration, Stimulator.AC_STIM, frequency, phase_pos, ramp_up, ramp_down, device)