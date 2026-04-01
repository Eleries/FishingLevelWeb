import os

class FileUploadDownloadManager:
    def __init__(self, upload_dir, logger):
        self.upload_dir = upload_dir
        self.logger = logger
        
    def upload_file(self, file):
        """处理文件上传并保存到指定目录"""
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)
        
        filename = file.filename
        file_path = os.path.join(self.upload_dir, filename)
        
        file.save(file_path)
        self.logger.log_message(f"文件上传成功: {file_path}")
        
        return file_path
    
    def download_file(self, file_path):
        """处理文件下载"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        return file_path