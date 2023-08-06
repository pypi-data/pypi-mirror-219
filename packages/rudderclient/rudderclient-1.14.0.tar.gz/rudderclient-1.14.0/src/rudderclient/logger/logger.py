import logging
import json
from datetime import datetime
from logging import LoggerAdapter


class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        log_object = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "filename": record.filename,
            "lineno": record.lineno,
            "funcName": record.funcName,
            "userUUID": getattr(record, "userUUID", ""),
            "correlationID": getattr(record, "correlationID", ""),
        }
        return json.dumps(log_object)


class CustomLoggerAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        return (
            "[%s] [%s] %s"
            % (self.extra["userUUID"], self.extra["correlationID"], msg),
            kwargs,
        )


def get_custom_logger(name, userUUID="", correlationID=""):
    handler = logging.StreamHandler()
    handler.setFormatter(CustomJsonFormatter())
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return CustomLoggerAdapter(
        logger, {"userUUID": userUUID, "correlationID": correlationID}
    )
