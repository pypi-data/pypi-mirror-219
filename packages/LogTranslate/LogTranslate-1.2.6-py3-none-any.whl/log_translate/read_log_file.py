# This is a sample Python script.
import importlib
import os
import threading
import traceback
from collections import deque
from os import cpu_count

from rx.subject import Subject

from log_translate.config_default import translators
from log_translate.data_struct import Log

from log_translate.log_translate.data_struct import Level


# //必须定义在使用者前面
class LogReader(object):
    def __init__(self,
                 chunk_size=1024 * 1024 * 10,
                 process_num_for_log_parsing=cpu_count()):
        self.log_unparsed_queue = deque()  # 用于存储未解析日志
        self.log_line_parsed_queue = deque()  # 用于存储已解析日志行
        self.is_all_files_read = False  # 标识是否已读取所有日志文件
        self.process_num_for_log_parsing = process_num_for_log_parsing  # 并发解析日志文件进程数
        self.chunk_size = chunk_size  # 每次读取日志的日志块大小
        self.files_read_list = []  # 存放已读取日志文件
        self.log_parsing_finished = False  # 标识是否完成日志解析
        self.log_stream = Subject()
        # 翻译
        try:
            config = importlib.import_module("config")
            self.log_translators = getattr(config, "translators")
        except:
            traceback.print_exc()
            self.log_translators = translators

    @staticmethod
    def readFile(path="."):
        with open(path, "rb") as f:
            for fline in f:
                yield fline
            f.close()

    def analyze(self, path):
        # 分行读取数据
        for datas in self.readFile(path):
            # 对日志进行翻译
            try:
                str = datas.decode('ISO-8859-1').strip()
                for translator in self.log_translators:
                    try:
                        result = translator.translate(str)
                        # 翻译后的日志存起来
                        if result:
                            print(result)
                            result.origin = str
                            self.log_stream.on_next(result)
                            break
                    except Exception as e:
                        print('日志翻译发生异常：', e)
                        traceback.print_exc()
                        self.log_stream.on_next(
                            Log(translated="日志翻译发生异常：%s \n%s" % (str, traceback.format_exc()), level=Level.e)
                        )
            except Exception as e:
                print('文件解析发生异常：', e)
                traceback.print_exc()
                self.log_stream.on_next(Log(translated="文件解析发生异常：%s" % traceback.format_exc(), level=Level.e))
        self.log_stream.on_next(Log(translated=None))

    def concurrency(self, log_files):
        # 多线程 解析
        for file in log_files:
            abspath = os.path.abspath(file)
            print(abspath)
            threading_thread = threading.Thread(target=self.analyze, name="read_log_file", args=(abspath,))
            threading_thread.start()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_log = LogReader()
    # parse_log.concurrency(["D:\\main_log_1__2023_0429_100141"])
    parse_log.concurrency(["./main_log_1__2023_0429_100141"])
