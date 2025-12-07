import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_entry)


# Create logger
logger = logging.getLogger("ml-api-logger")
logger.setLevel(logging.INFO)

# Stream handler (prints to console / Docker logs)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

# Avoid duplicate handlers
if not logger.handlers:
    logger.addHandler(handler)
