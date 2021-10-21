import logging, os, threading
from logging.handlers import RotatingFileHandler


# def logger():
#     LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     DATA_FORMAT = '%Y-%m-%d %H:%M:%S'
#
#     # 封装的基本方法，方便配置
#     logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATA_FORMAT)
#
#     return logging

class Log:
    def __init__(self):
        resultPath = os.path.join(os.getcwd().split("APItest")[0],"APItest/logs")

        if not os.path.exists(resultPath):
            os.mkdir(resultPath)

        # 定义logger
        self.logger = logging.getLogger()

        # 设置最低日志级别
        self.logger.setLevel(logging.INFO)

        # 2.定义handler：日志输出方式

        #FileHandler:将日志信息输出到磁盘文件
        # handler = logging.FileHandler(os.path.join(logpath,"out.log))

        # 追加，知道达到10M，别分数量为10个
        file_handler = RotatingFileHandler(os.path.join(resultPath,"out.log"), maxBytes=10*1024*1024, backupCount=10)

        # 将日志打印到工作台
        stream_handler = logging.StreamHandler()

        # 3.定义handler格式(日志格式)
        formatter = logging.Formatter("%(asctime)s-%(pathname)s[line:%(lineno)d]-%(levelname)s:%(message)s")

        # 4.设置屏幕上显示的格式
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # 5.把对象加到logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

class Mylog:
    """单独线程"""
    log = None

    # 锁对象
    lock = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if Mylog.log is None:
            # 加锁
            Mylog.lock.acquire()
            Mylog.log = Log()
            # 释放锁
            Mylog.lock.release()
        return Mylog.log


def logger():
    # 使用线程
    return Mylog.get_log().logger


if __name__ == '__main__':
    logger = logger()
    logger.info("haha")



