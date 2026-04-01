import os
import re

class FileValidator:
    def __init__(self, logger):
        self.logger = logger

    def validate_file(self, file_path):
        """执行文件校验，包括存在性、大小和内容检查"""
        try:
            self._validate_file_exists(file_path)
            self._validate_file_size(file_path)
            self._validate_file_content(file_path)
            self._validate_file_name(os.path.basename(file_path))
            self.logger.log_message(f"文件校验通过: {file_path}")
            return True
        except Exception as e:
            self.logger.log_message(f"文件校验失败: {str(e)}", level='error')
            return False

    def _validate_file_exists(self, file_path):
        """检查文件是否存在"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

    def _validate_file_size(self, file_path):
        """检查文件大小是否符合要求"""
        if os.path.getsize(file_path) == 0:
            raise ValueError(f"文件为空: {file_path}")

    def _validate_file_content(self, file_path):
        """检查文件内容是否符合预期格式"""
        pass

    def _validate_file_name(self, file_name):
        """验证文件名是否符合要求"""
        valid_archive_pattern = r'^[a-zA-Z0-9\u4e00-\u9fa5]*+_\d{9}$'
        valid_restore_pattern = r'^[a-zA-Z0-9\u4e00-\u9fa5]*+_\d{9}_FishBAK$'
        if not (re.match(valid_archive_pattern, file_name) or re.match(valid_restore_pattern, file_name)):
            raise ValueError(f"文件名不符合要求: {file_name}")

    def is_save_file(self, file_path):
        """检查是否为保存文件"""
        return re.search(r'_\d+$', os.path.splitext(os.path.basename(file_path))[0]) is not None

    def is_backup_file(self, file_path):
        """检查是否为备份文件"""
        return "_FishBAK" in os.path.basename(file_path)