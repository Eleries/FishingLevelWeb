import os
import re
import xml.etree.ElementTree as ET

class FileModifier:
    """文件内容修改接口"""
    def get_fishing_level(self, file_path):
        """获取钓鱼等级"""
        raise NotImplementedError
    
    def modify_fishing_level(self, file_path, target_dir=None):
        """修改钓鱼等级"""
        raise NotImplementedError

class FishingLevelModifier(FileModifier):
    """钓鱼等级修改器实现"""
    def __init__(self, logger):
        self.logger = logger
        
    def get_fishing_level(self, file_path):
        """获取钓鱼等级"""
        self.logger.log_message(f"开始读取文件以获取钓鱼等级: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        if os.path.getsize(file_path) == 0:
            raise ValueError(f"文件为空: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
            if not content.strip():
                raise ValueError(f"读取的文件内容为空或仅包含空白字符: {file_path}")
                
            content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', content)
            if not content.strip():
                raise ValueError(f"过滤后内容为空，可能文件包含非法字符: {file_path}")
                
            try:
                tree = ET.ElementTree(ET.fromstring(content))
            except ET.ParseError as e:
                raise ValueError(f"XML解析失败: {str(e)}")
                
        root = tree.getroot()
        if root is None:
            raise ValueError("XML解析失败：根节点为空，文件结构可能损坏")
            
        fishing_level = root.find('.//fishingLevel')
        if fishing_level is not None:
            self.logger.log_message(f"当前钓鱼等级值: {fishing_level.text}")
            return fishing_level.text
        else:
            raise ValueError("未找到钓鱼等级")
    
    def get_player_names(self, file_path):
        """获取所有玩家的名字"""
        self.logger.log_message(f"开始读取文件以获取玩家名字: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        if os.path.getsize(file_path) == 0:
            raise ValueError(f"文件为空: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
            if not content.strip():
                raise ValueError(f"读取的文件内容为空或仅包含空白字符: {file_path}")
            
            content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', content)
            if not content.strip():
                raise ValueError(f"过滤后内容为空，可能文件包含非法字符: {file_path}")
            
            try:
                tree = ET.ElementTree(ET.fromstring(content))
            except ET.ParseError as e:
                raise ValueError(f"XML解析失败: {str(e)}")
            
        root = tree.getroot()
        if root is None:
            raise ValueError("XML解析失败：根节点为空，文件结构可能损坏")
            
        names = []
        
        # 获取房主名字
        player = root.find('player')
        if player is not None:
            name = player.find('name')
            if name is not None and name.text and name.text.strip():
                names.append(name.text.strip())
        
        # 获取访客名字
        farmers = root.findall('.//Farmer')
        for farmer in farmers:
            name = farmer.find('name')
            if name is not None and name.text and name.text.strip():
                names.append(name.text.strip())
        
        self.logger.log_message(f"获取到玩家名字: {names}")
        return names

    def modify_fishing_level(self, file_path, selected_indices=None, target_dir=None):
        """修改钓鱼等级和经验值"""
        self.logger.log_message(f"开始处理文件: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        if os.path.getsize(file_path) == 0:
            raise ValueError(f"文件为空: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
            if not content.strip():
                raise ValueError(f"读取的文件内容为空或仅包含空白字符: {file_path}")
            
            content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', content)
            if not content.strip():
                raise ValueError(f"过滤后内容为空，可能文件包含非法字符: {file_path}")
            
            try:
                tree = ET.ElementTree(ET.fromstring(content))
            except ET.ParseError as e:
                raise ValueError(f"XML解析失败: {str(e)}")
            
        root = tree.getroot()
        if root is None:
            raise ValueError("XML解析失败：根节点为空，文件结构可能损坏")
            
        fishing_levels = root.findall('.//fishingLevel')
        experience_points = root.findall('.//experiencePoints')
        
        if selected_indices is None:
            selected_indices = [0]  # 默认修改第一个
            
        for idx in selected_indices:
            if idx < len(fishing_levels):
                fishing_level = fishing_levels[idx]
                old_level = fishing_level.text
                fishing_level.text = '59'
                self.logger.log_message(f"钓鱼等级从 {old_level} 修改为 59")
                
                # 修改对应的经验
                if idx < len(experience_points):
                    exp_block = experience_points[idx]
                    ints = exp_block.findall('int')
                    if len(ints) >= 2:
                        second_int = ints[1]
                        old_exp = second_int.text
                        second_int.text = '15001'
                        self.logger.log_message(f"钓鱼经验从 {old_exp} 修改为 15001")
        
        # 写回content
        content = ET.tostring(root, encoding='unicode', method='xml')
        
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)
        
        return content