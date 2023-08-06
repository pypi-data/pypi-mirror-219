import re
from abc import abstractmethod

from log_translate.gloable import pids


# 通过正则表达式匹配tag解析
# :param pattern_translators 是数据[tag,fun(tag, msg)] fun参数必须是(tag, msg)
class TagPatternTranslator(object):
    def __init__(self, pattern_translators):
        self.pattern_translators = pattern_translators

    def translate(self, tag, msg):
        for pattern in self.pattern_translators:
            match = re.compile(pattern, re.IGNORECASE).fullmatch(tag)
            if match:
                translator = self.pattern_translators[pattern]
                if callable(translator):
                    return translator(tag, msg)
                else:
                    return translator.translate(tag, msg)
        return None


# 字符串匹配tag  例子参考 BluetoothTranslator
# :param str_translators是数组[tag, fun(msg)] fun方法参数是 (msg)
class TagStrTranslator(object):
    def __init__(self, str_translators):
        self.str_translators = str_translators

    def translate(self, tag, msg):
        if tag in self.str_translators:
            translator = self.str_translators[tag]
            if callable(translator):
                return translator(msg)
            else:
                return translator.translate(msg)
        return None


class SubTagTranslator(TagPatternTranslator):
    """
    :param father表示上一级tag
    :param tag_from_str_fun 从字符串解析tag的方法
    :param tag_translators 用来解析二级tag的translator 是个数组必须是TagStrTranslator|TagPatternTranslator
    """

    def __init__(self, father, tag_from_str_fun, tag_translators):
        super().__init__({
            father: self.translate_sub_tag
        })
        self.tag_from_str_fun = tag_from_str_fun
        self.tag_translators = tag_translators

    def translate_sub_tag(self, tag, msg):
        log = self.tag_from_str_fun(msg)
        if log:
            sec_tag = log.group("tag")
            sec_msg = log.group("msg")
            for translator in self.tag_translators:
                result = translator.translate(sec_tag, sec_msg)
                if result:
                    return result
        return None


class StringTranslator(object):
    def __init__(self, tag_translators=None):
        # 这里是 TagStrTranslator
        if tag_translators is None:
            tag_translators = []
        self.tag_translators = tag_translators

    def translate(self, string):
        # 系统日志
        # 03-21 21:31:45.534 12980 15281 I ActivityManager   : START 0 ooooo:
        log = self.tag_from_str(string)
        if log:
            tag = log.group("tag")
            msg = log.group("msg")
            time = log.group("time")
            try:
                pid = log.group("pid")
            except:
                pid = "0000"
            for translator in self.tag_translators:
                show = translator.translate(tag, msg)
                if show:
                    show.time = time
                    show.oring = msg
                    show.process = pid
                    if pids.count(pid) == 0:
                        pids.append(pid)
                    return show
        return None

    @abstractmethod
    def tag_from_str(self, string):
        pass


class SysLogTranslator(StringTranslator):
    def tag_from_str(self, string):
        # 04-29 10:01:16.788935  1848  2303 D OGG_Detector: D:done mCurrStatus: 0
        return re.search(r"(?P<time>\d+.*\.\d{3,}) +(?P<pid>\d+).* [A-Z] (?P<tag>.*?) *:(?P<msg>.*)", string)


class LogcatTranslator(StringTranslator):

    def tag_from_str(self, string):
        pass


if __name__ == '__main__':
    result = re.search("device: (.*?),", "connect() - device: 34:47:9A:31:52:CF, auto: false, eattSupport: false")
    print(result.group(1))
    result = re.search("(?<=\*).*", "onReCreateBond: 24:*:35:06")

    # (?<=A).+?(?=B) 匹配规则A和B之间的元素 不包括A和B
    #
    print(result.group())

    str = "04-29 10:01:16.788935  1848  2303 D OGG_Detector: D:done mCurrStatus: 0"
    f = re.search(r"(?P<time>\d+.*\.\d{3,}) +(?P<pid>\d+).* [A-Z] (?P<tag>.*?) *:(?P<msg>.*)", str)
    print(f.group("pid"))
    print(f.group("tag"))

    print(re.compile("testb", re.IGNORECASE).fullmatch("testb").group())
