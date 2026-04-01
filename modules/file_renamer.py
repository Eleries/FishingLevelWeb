import os

class FileRenamer:
    def __init__(self, logger):
        self.logger = logger
        self.backup_suffix = "_FishBAK"
        
    def add_backup_suffix(self, file_path):
        """添加备份文件后缀"""
        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)
        
        backup_name = f"{name}{self.backup_suffix}{ext}"
        backup_path = os.path.join(file_dir, backup_name)
        
        self.logger.log_message(f"生成备份文件名: {backup_path}")
        return backup_path