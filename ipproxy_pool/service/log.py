import logging, os
from logging.handlers import RotatingFileHandler

class get_logger(object):

    def __init__(self, dir=None, filename=None, maxByte=5 * 1024 * 1024, backup=5, format=None):
        self.dir = dir
        self.filename = filename
        self.maxByte = maxByte
        self.backup = backup
        self.format = format

    def logger(self):
        if not self.dir:
            self.dir = 'log/'

        if not self.filename:
            self.filename = '%s/_log.txt' % dir
        else:
            self.filename = '%s/%s' % (self.dir, self.filename)

        if not self.format:
            self.format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)

        fh = RotatingFileHandler(self.filename, maxBytes=self.maxByte, backupCount=self.backup, encoding='utf-8')  # 创建一个文件流并设置编码utf8

        logger = logging.getLogger()  # 获得一个logger对象，默认是root
        logger.setLevel(logging.INFO)
        fm = logging.Formatter(fmt=self.format, datefmt="%Y-%m-%d %H:%M:%S")  # 设置日志格式
        logger.addHandler(fh)  # 把文件流添加进来，流向写入到文件
        fh.setFormatter(fm)  # 把文件流添加写入格式
        return logger
