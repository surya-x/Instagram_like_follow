import logging

log_filePath = r"logs/"
logname = log_filePath + 'Instagram-like-follow-logs.log'

logging.basicConfig(level=logging.INFO,
                   # format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                   format='%(asctime)s,%(msecs)d %(levelname)-5s [%(filename)s:%(lineno)d] %(message)s',
                   datefmt='%Y-%m-%d %H:%M:%S',
                   filemode='a+',
                   filename=logname)

logging = logging.getLogger()
