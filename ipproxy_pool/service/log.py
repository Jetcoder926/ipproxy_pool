import logging, os
from logging.handlers import RotatingFileHandler


class get_logger(object):

    def __init__(self, logger_module=None, dir=None, filename=None, maxByte=5 * 1024 * 1024, backup=5, format=None):
        if dir is None:
            dir = 'log/'

        if filename is None:
            filename = '%s/_log.txt' % dir

        if format is None:
            format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

        self._dir = dir
        self._filename = filename
        self._maxByte = maxByte
        self._backup = backup
        self._format = format
        self._logger_module = logger_module

        if not os.path.isdir(self._dir):
            os.mkdir(self._dir)

    def logger(self):

        fh = RotatingFileHandler('%s/%s' % (self._dir, self._filename), maxBytes=self._maxByte,
                                 backupCount=self._backup, encoding='utf-8')  # 创建一个文件流并设置编码utf8

        logger = logging.getLogger(self._logger_module)  # 获得一个logger对象，默认是root
        logger.setLevel(logging.INFO)
        fm = logging.Formatter(fmt=self._format, datefmt="%Y-%m-%d %H:%M:%S")  # 设置日志格式
        logger.addHandler(fh)  # 把文件流添加进来，流向写入到文件
        fh.setFormatter(fm)  # 把文件流添加写入格式
        return logger
