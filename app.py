from flask import Flask, render_template, request, jsonify, send_file
import os
from modules.file_upload_download import FileUploadDownloadManager
from modules.file_validator import FileValidator
from modules.file_renamer import FileRenamer
from modules.file_modifier import FishingLevelModifier
from modules.file_logger import FileLogger
from modules.file_processor import FileProcessor

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# 初始化各个模块
upload_dir = 'uploads'
logger = FileLogger()
file_validator = FileValidator(logger)
file_renamer = FileRenamer(logger)
file_modifier = FishingLevelModifier(logger)
file_upload_download = FileUploadDownloadManager(upload_dir, logger)
file_processor = FileProcessor(file_validator, file_renamer, file_modifier, 
                               file_upload_download, logger)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contract')
def contract():
    return render_template('contract.html')

@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        logger.log_message('上传失败，未提供文件', level='error')
        return jsonify({'message': '上传失败，未提供文件'}), 400

    try:
        file_name = file.filename
        file_validator._validate_file_name(file_name)  # 验证文件名
        file_path = file_upload_download.upload_file(file)
        names = file_modifier.get_player_names(file_path)
        logger.log_message('上传文件成功')
        return jsonify({'message': '上传文件成功', 'file_path': file_path, 'names': names})
    except Exception as e:
        logger.log_message(f'上传失败: {str(e)}', level='error')
        return jsonify({'message': f'上传失败: {str(e)}'}), 500

@app.route('/modify', methods=['POST'])
def modify():
    file_path = request.form.get('file_path')
    selected_indices = request.form.getlist('selected_indices')
    if selected_indices:
        selected_indices = [int(i) for i in selected_indices]
    else:
        selected_indices = None
    if not file_path:
        return jsonify({'message': '修改失败，未提供文件路径'}), 400

    try:
        if not file_validator.validate_file(file_path):
            return jsonify({'message': '文件校验失败，无法处理'}), 400

        modified_path = file_processor.modify_file(file_path, selected_indices=selected_indices)
        backup_path = file_processor.create_backup(file_path)  # 只有修改成功才创建备份
        return jsonify({
            'message': '文件修改成功', 
            'backup_path': backup_path, 
            'modified_path': modified_path
        })
    except Exception as e:
        return jsonify({'message': f'修改失败，请重新上传存档: {str(e)}'}), 500

@app.route('/restore', methods=['POST'])
def restore():
    backup_path = request.form.get('backup_path')
    if not backup_path:
        return jsonify({'message': '还原失败，未提供备份文件路径'}), 400

    try:
        file_name = os.path.basename(backup_path)
        file_validator._validate_file_name(file_name)  # 验证文件名
        restored_path = file_processor.restore_from_backup(backup_path)
        return jsonify({'message': '文件还原成功', 'original_path': restored_path})
    except Exception as e:
        return jsonify({'message': f'还原失败: {str(e)}'}), 500

@app.route('/download')
def download():
    file_path = request.args.get('file_path')
    if not file_path or not os.path.exists(file_path):
        return jsonify({'message': '下载失败，文件不存在'}), 404

    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'message': f'下载失败: {str(e)}'}), 500

if __name__ == '__main__':
    # 创建上传目录
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        os.chmod(upload_dir, 0o755)
        logger.log_message(f"创建上传目录: {upload_dir}，权限设置为755")

    logger.log_message(f"应用将运行在 http://127.0.0.1:18650/")
    logger.log_message("按 CTRL+C 停止应用")

    try:
        app.run(host='127.0.0.1', port=18650)
    except KeyboardInterrupt:
        logger.log_message("\n应用已停止")
    except Exception as e:
        logger.log_message(f"应用运行出错: {str(e)}", level='error')