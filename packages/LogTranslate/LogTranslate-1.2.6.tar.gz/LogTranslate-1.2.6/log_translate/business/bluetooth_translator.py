import re

from log_translate.data_struct import Log, Level

from log_translate.log_translator import SubTagTranslator, TagStrTranslator


class SecTagDemoTranslator(SubTagTranslator):
    def __init__(self):
        super().__init__("DFJ",
                         lambda string: re.search(r"(?P<tag>.*?) *:(?P<msg>.*)", string),
                         [
                             TagStrTranslator({
                                 "sec_tag": self.new_tag
                             })
                         ])

    def new_tag(self, tag, msg):
        return Log(translated=msg)


class BluetoothTranslator(TagStrTranslator):
    def __init__(self):
        super().__init__({
            "BluetoothAdapter": bluetooth_adapter,
            "BluetoothGatt": bluetooth_gatt,
            "bt_rfcomm": bt_rfcomm,
            "WS_BT_BluetoothPairingRequest": bluetooth_pairing_request,
            "ActivityTaskManager": bluetooth_pairing_dialog
        })


code_state = {
    "10": "手机系统蓝牙 已关闭",
    "12": "手机系统蓝牙 已打开",
    "OFF": "手机系统蓝牙 已关闭",
    "ON": "手机系统蓝牙 已打开"
}


def bluetooth_pairing_dialog(msg):
    # ActivityTaskManager: Displayed com.oplus.wirelesssettings/com.android.settings.bluetooth.BluetoothPairingDialog
    # port_rfc_closed: RFCOMM connection closed, index=3, state=2 reason=Closed[19], UUID=111F, bd_addr=ac:73:52:3f:5b:0a, is_server=1
    if "BluetoothPairingDialog" in msg:
        result = re.search("Displayed.*BluetoothPairingDialog", msg)
        if result:
            return Log(translated=" ----------------------- 配对PIN码弹窗弹出 ----------------------- ")
    return None


def bluetooth_pairing_request(msg):
    # port_rfc_closed: RFCOMM connection closed, index=3, state=2 reason=Closed[19], UUID=111F, bd_addr=ac:73:52:3f:5b:0a, is_server=1
    if "PAIRING_REQUEST" in msg:
        return Log(translated=" ----------------------- 设备请求配对 ----------------------- ")
    return None


def bt_rfcomm(msg):
    # port_rfc_closed: RFCOMM connection closed, index=3, state=2 reason=Closed[19], UUID=111F, bd_addr=ac:73:52:3f:5b:0a, is_server=1
    if "port_rfc_closed" in msg:
        result = re.search(".*: (ON|OFF)", msg)
        if result:
            if result.group(1) in code_state:
                return Log(translated=">>>>>>>>>>  %s  <<<<<<<< " % (code_state[result.group(1)]), level=Level.i)

    return None


def bluetooth_adapter(msg):
    if "isLeEnabled" in msg:
        result = re.search(".*: (ON|OFF)", msg)
        if result:
            if result.group(1) in code_state:
                return Log(translated=">>>>>>>>>>  %s  <<<<<<<< " % (code_state[result.group(1)]), level=Level.i)

    return None


# noinspection PyTypeChecker
def bluetooth_gatt(msg: object) -> object:
    if "cancelOpen()" in msg:
        result = re.search("device: (.*?)", msg)
        return Log(translated=">>>>>>>>>>  gatt 手机主动断开连接 %s  <<<<<<<< " % (result.group(1)), level=Level.w)
    if "close()" in msg:
        return Log(translated=">>>>>>>>>>  gatt 手机主动关闭连接  <<<<<<<< ", level=Level.w)
    if "connect()" in msg:
        # connect() - device: 34:47:9A:31:52:CF, auto: false, eattSupport: false
        result = re.search("device: (.*?),", msg)
        return Log(translated=">>>>>>>>>>  gatt 发起设备连接 %s  <<<<<<<< " % (result.group(1)), level=Level.w)
    return None


if __name__ == '__main__':
    result = re.search("device: (.*?),", "connect() - device: 34:47:9A:31:52:CF, auto: false, eattSupport: false")
    print(result.group(1))
    result = re.search("(?<=\*).*", "onReCreateBond: 24:*:35:06")

    # (?<=A).+?(?=B) 匹配规则A和B之间的元素 不包括A和B
    #
    print(result.group())
