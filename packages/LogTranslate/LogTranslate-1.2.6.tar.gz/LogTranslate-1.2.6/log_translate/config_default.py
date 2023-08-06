from log_translate.business.AndroidCrashPattern_translator import CrashPatternTranslator
from log_translate.business.bluetooth_translator import BluetoothTranslator
from log_translate.log_translator import SysLogTranslator

translators = [SysLogTranslator(tag_translators=[BluetoothTranslator(), CrashPatternTranslator()])]
