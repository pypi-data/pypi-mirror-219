import sys
from typing import Any, Dict, List, Optional
from .logger import Logger

class TestLogger(Logger):
    def __init__(self, output_path = sys.stderr, buffer_logs = True):
        if isinstance(output_path, str):
            output_path = open(output_path, 'w')

        self.output_file = output_path
        self.buffer_logs = buffer_logs
        self.logs: List[Dict[str, Any]] = []

    def log(self, level: str, message: str, context: Optional[Dict[str, Any]] = None):
        if context is None:
            context = {}

        if self.buffer_logs:
            self.logs.append({'level': level, 'message': message, 'context': context})
        else:
            log = self.format_log(level, message, context)
            print(log, file=self.output_file)

    def format_log(self, level: str, message: str, context: Dict[str, Any]) -> str:
        return f"{level}: {message} [{repr(context)}]"

    def clear_logs(self):
        self.logs = []

    def flush_logs(self):
        logs = self.get_logs()

        self.logs = []
        print(logs, file=self.output_file)

    def get_logs(self):
        logs = ''
        for log in self.logs:
            logs += self.format_log(log['level'], log['message'], log['context']) + "\n"

        return logs

    def emergency(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.log('emergency', message, context)

    def alert(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.log('alert', message, context)

    def critical(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.log('critical', message, context)

    def error(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.log('error', message, context)

    def warning(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.log('warning', message, context)

    def notice(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.log('notice', message, context)

    def info(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.log('info', message, context)

    def debug(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.log('debug', message, context)