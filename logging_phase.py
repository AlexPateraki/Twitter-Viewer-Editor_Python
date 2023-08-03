%%file myeditorlog.conf

[loggers]
keys=root,tuc_logger

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=fileFormatter,consoleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_tuc_logger]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=tuc_logger
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=WARNING
formatter=consoleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=INFO
formatter=fileFormatter
args=('logme.txt', 'w')

[formatter_fileFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=

[formatter_consoleFormatter]
format=%(levelname)s - %(message)s