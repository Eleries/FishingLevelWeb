from datetime import datetime

class FileLogger:
    def __init__(self):
        self.logs = []
        
    def log_message(self, message, level='info'):
        """记录日志消息"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'level': level.upper(),
            'message': message
        }
        
        self.logs.append(log_entry)
        print(f"[{timestamp}] [{level.upper()}] {message}")
        
    def get_logs(self):
        """获取所有日志"""
        return self.logs
    
    def clear_logs(self):
        """清空日志"""
        self.logs = []    