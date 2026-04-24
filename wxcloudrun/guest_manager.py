import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class GuestManager:
    """宾客信息管理：读取JSON中的姓名和桌号，提供查询功能"""

    def __init__(self, json_path: str = None):
        self.guest_dict = {}  # {姓名: 桌号}
        self._load_guests(json_path)

    def _load_guests(self, json_path: str = None):
        """从JSON文件加载宾客信息"""
        try:
            # 默认路径：wxcloudrun目录下的guest_data.json
            if json_path is None:
                json_path = os.path.join(
                    os.path.dirname(__file__),
                    "guest_data.json"
                )
            
            if not Path(json_path).exists():
                logger.warning(f"宾客JSON文件不存在: {json_path}")
                return
            
            with open(json_path, 'r', encoding='utf-8') as f:
                self.guest_dict = json.load(f)
            
            logger.info(f"成功加载 {len(self.guest_dict)} 位宾客信息")
            
        except Exception as e:
            logger.error(f"加载宾客信息失败: {str(e)}")

    def query_table(self, name: str) -> int:
        """根据姓名查询桌号"""
        return self.guest_dict.get(name)

    def find_guest(self, message: str) -> dict:
        """
        从消息中查找人名，返回桌号信息
        :param message: 用户发送的消息
        :return: {"name": 找到的姓名, "table": 桌号} 或 None
        """
        if not message:
            return None
        
        # 精确匹配优先（消息内容完全等于姓名）
        message_stripped = message.strip()
        if message_stripped in self.guest_dict:
            return {"name": message_stripped, "table": self.guest_dict[message_stripped]}
        
        # 遍历所有宾客姓名，检查是否包含在消息中（名字一般不超过3个字）
        for name, table in self.guest_dict.items():
            if len(name) <= 4 and name in message:  # 最多4个字的名字（含复姓）
                return {"name": name, "table": table}
        
        return None

    def get_table_info(self, name: str) -> str:
        """
        获取桌号信息文本
        :param name: 姓名
        :return: 回复文本
        """
        table = self.query_table(name)
        if table:
            return f"{name}您好！您的桌号是: {table}桌"
        return None
