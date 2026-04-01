import os
import shutil
from datetime import datetime, timedelta

class FileProcessor:
    def __init__(self, file_validator, file_renamer, file_modifier, 
                 file_upload_download, logger):
        self.file_validator = file_validator
        self.file_renamer = file_renamer
        self.file_modifier = file_modifier
        self.file_upload_download = file_upload_download
        self.logger = logger
        
    def create_backup(self, file_path):
        """创建文件备份"""
        if not self.file_validator.validate_file(file_path):
            raise ValueError(f"无法备份，文件校验失败: {file_path}")
            
        backup_path = self.file_renamer.add_backup_suffix(file_path)
        
        try:
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            shutil.copy2(file_path, backup_path)
            self.logger.log_message(f"备份文件创建成功: {backup_path}")
            return backup_path
        except Exception as e:
            self.logger.log_message(f"备份文件创建失败: {str(e)}", level='error')
            raise
    
    def restore_from_backup(self, backup_path):
        """从备份恢复文件"""
        if not self.file_validator.is_backup_file(backup_path):
            raise ValueError(f"不是有效的备份文件: {backup_path}")
            
        original_path = backup_path.replace("_FishBAK", "")
        
        try:
            if os.path.exists(original_path):
                os.remove(original_path)
                self.logger.log_message(f"原文件已删除: {original_path}")
                
            shutil.copy2(backup_path, original_path)
            self.logger.log_message(f"文件还原成功: {original_path}")
            return original_path
        except Exception as e:
            self.logger.log_message(f"文件还原失败: {str(e)}", level='error')
            raise
    
    def modify_file(self, file_path, selected_indices=None, target_dir=None):
        """修改文件内容"""
        if not self.file_validator.validate_file(file_path):
            raise ValueError(f"无法修改，文件校验失败: {file_path}")
            
        try:
            modified_content = self.file_modifier.modify_fishing_level(file_path, selected_indices=selected_indices)
            modified_path = file_path
            with open(modified_path, 'w', encoding='utf-8-sig') as f:
                f.write(modified_content)
            self.logger.log_message(f"文件修改成功: {modified_path}")
            return modified_path
        except Exception as e:
            self.logger.log_message(f"文件修改失败: {str(e)}", level='error')
            raise
    
    def delete_expired_files(self):
        """删除超过24小时的文件"""
        upload_dir = self.file_upload_download.upload_dir
        self.logger.log_message(f"开始检查过期文件，目录: {upload_dir}")
    
        if not os.path.exists(upload_dir):
            self.logger.log_message(f"上传目录不存在: {upload_dir}")
            return
        
        now = datetime.now()
    
        for root, dirs, files in os.walk(upload_dir, topdown=False):
            if root == upload_dir:
                continue
            
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    ctime = datetime.fromtimestamp(os.path.getctime(file_path))
                    age = now - ctime
                
                    if age >= timedelta(hours=24):
                        # 删除了获取文件权限的代码
                        self.logger.log_message(f"准备删除过期文件: {file_path} (创建时间: {ctime})")
                        os.remove(file_path)
                        self.logger.log_message(f"成功删除过期文件: {file_path}")
                except PermissionError as e:
                    self.logger.log_message(f"权限不足，无法删除文件: {file_path} - {str(e)}", level='error')
                except Exception as e:
                    self.logger.log_message(f"删除文件 {file_path} 失败: {str(e)}", level='error')
            
            if not os.listdir(root):
                try:
                    os.rmdir(root)
                    self.logger.log_message(f"删除空文件夹: {root}")
                except Exception as e:
                    self.logger.log_message(f"删除空文件夹 {root} 失败: {str(e)}", level='error')

        for file in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, file)
            if os.path.isfile(file_path):
                try:
                    ctime = datetime.fromtimestamp(os.path.getctime(file_path))
                    age = now - ctime
                
                    if age >= timedelta(hours=24):
                        # 删除了获取文件权限的代码
                        self.logger.log_message(f"准备删除根目录中的过期文件: {file_path} (创建时间: {ctime})")
                        os.remove(file_path)
                        self.logger.log_message(f"成功删除根目录中的过期文件: {file_path}")
                except PermissionError as e:
                    self.logger.log_message(f"权限不足，无法删除根目录中的文件: {file_path} - {str(e)}", level='error')
                except Exception as e:
                    self.logger.log_message(f"删除根目录中的文件 {file_path} 失败: {str(e)}", level='error')