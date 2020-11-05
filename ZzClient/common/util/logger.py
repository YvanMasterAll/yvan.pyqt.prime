import logging
from ZzClient.config.const import Config

'''
日志记录
'''

logger = logging.getLogger("debug")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(Config().log_path)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(console)

logger_err = logging.getLogger("error")
logger_err.setLevel(logging.ERROR)
handler_err = logging.FileHandler(Config().error_path)
handler_err.setLevel(logging.ERROR)
handler_err.setFormatter(formatter)
console_err = logging.StreamHandler()
console_err.setLevel(logging.ERROR)
console_err.setFormatter(formatter)
logger_err.addHandler(handler_err)
logger_err.addHandler(console_err)