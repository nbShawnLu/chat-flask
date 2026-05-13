import json
import logging
import os
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class GuestManager:
    """宾客信息管理：读取座位安排数据，提供查询功能"""

    # 后缀模式：(后缀文本, 回复描述) —— 按长度降序排列，避免"父女"被"夫妇"误匹配
    SUFFIX_PATTERNS = [
        ("全家", "您和家人"),
        ("夫妇", "您和爱人"),
        ("父子", "您和儿子"),
        ("母女", "您和女儿"),
        ("父女", "您和女儿"),
    ]

    def __init__(self, json_path: str = None):
        self.guest_dict = {}   # {姓名: 桌号}  向后兼容
        self.guest_detail = {}  # {姓名: {"table": 桌号, "suffix": 后缀或None}}
        self._load_guests(json_path)

    def _load_guests(self, json_path: str = None):
        """从座位安排数据JSON加载宾客信息"""
        try:
            # 默认路径：wxcloudrun目录下的seating_data.json
            if json_path is None:
                json_path = os.path.join(
                    os.path.dirname(__file__),
                    "seating_data.json"
                )

            if not Path(json_path).exists():
                logger.warning(f"座位安排数据文件不存在: {json_path}")
                return

            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for key, table_data in data.items():
                table_number = int(table_data["number"])
                members_str = table_data.get("members", "")

                if not members_str:
                    continue

                members = members_str.split("、")
                for member in members:
                    member = member.strip()
                    if not member:
                        continue

                    # 尝试匹配后缀（全家/夫妇/父子/母女/父女）
                    suffix = None
                    name = member
                    for suffix_text, _ in self.SUFFIX_PATTERNS:
                        if member.endswith(suffix_text):
                            suffix = suffix_text
                            name = member[:-len(suffix_text)]
                            break

                    self.guest_dict[name] = table_number
                    self.guest_detail[name] = {
                        "table": table_number,
                        "suffix": suffix,
                    }

            logger.info(f"成功加载 {len(self.guest_dict)} 位宾客信息")

        except Exception as e:
            logger.error(f"加载宾客信息失败: {str(e)}")

    def query_table(self, name: str) -> int:
        """根据姓名查询桌号"""
        return self.guest_dict.get(name)

    def _get_suffix_desc(self, suffix: str) -> str:
        """获取后缀对应的回复描述"""
        for suffix_text, desc in self.SUFFIX_PATTERNS:
            if suffix == suffix_text:
                return desc
        return ""

    def find_guest(self, message: str) -> dict:
        """
        从消息中查找人名，返回桌号信息
        :param message: 用户发送的消息
        :return: {"name": 姓名, "table": 桌号, "suffix": 后缀或None} 或 None
        """
        if not message:
            return None

        # 移除所有空白字符（空格、换行、制表符等）
        message_clean = re.sub(r'\s+', '', message)
        # 移除零宽字符和其他不可见Unicode字符
        message_clean = re.sub(r'[\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufeff]', '', message_clean)

        message_stripped = message_clean.strip()
        if not message_stripped:
            return None

        # 精确匹配优先（消息内容完全等于姓名）
        if message_stripped in self.guest_dict:
            detail = self.guest_detail.get(message_stripped, {})
            return {
                "name": message_stripped,
                "table": self.guest_dict[message_stripped],
                "suffix": detail.get("suffix"),
            }

        # 遍历所有宾客姓名，检查是否包含在消息中（名字一般不超过4个字）
        for name, table in self.guest_dict.items():
            if len(name) <= 4 and name in message_stripped:
                detail = self.guest_detail.get(name, {})
                return {
                    "name": name,
                    "table": table,
                    "suffix": detail.get("suffix"),
                }

        return None

    def get_table_info(self, name: str) -> str:
        """
        获取桌号信息文本
        :param name: 姓名
        :return: 回复文本
        """
        detail = self.guest_detail.get(name)
        if not detail:
            return None

        table = detail["table"]
        suffix = detail.get("suffix")

        if suffix:
            suffix_desc = self._get_suffix_desc(suffix)
            reply = f"{name}您好！{suffix_desc}的桌号是: {table}桌"
        else:
            reply = f"{name}您好！您的桌号是: {table}桌"

        return reply
