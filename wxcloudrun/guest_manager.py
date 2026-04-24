import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class GuestManager:
    """宾客信息管理：读取Excel中的姓名和桌号，提供查询功能"""

    def __init__(self, excel_path: str = None):
        self.guest_dict = {}  # {姓名: 桌号}
        self._load_guests(excel_path)

    def _load_guests(self, excel_path: str = None):
        """从Excel文件加载宾客信息"""
        try:
            import pandas as pd
            
            # 默认路径：项目根目录下的Excel文件
            if excel_path is None:
                excel_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "2026.05.16_陆啸.xlsx"
                )
            
            if not Path(excel_path).exists():
                logger.warning(f"宾客Excel文件不存在: {excel_path}")
                return
            
            df = pd.read_excel(excel_path)
            
            # 遍历每一行，建立姓名到桌号的映射
            for _, row in df.iterrows():
                name = row.get("姓名")
                table = row.get("桌号")
                
                if pd.notna(name) and pd.notna(table):
                    # 处理多人情况（如"毛裕谷，陈群"）
                    names = str(name).replace("，", ",").replace("、", ",").replace("夫妻", "").strip()
                    for n in names.split(","):
                        n = n.strip()
                        if n:
                            self.guest_dict[n] = int(table)
            
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
        
        # 遍历所有宾客姓名，检查是否包含在消息中
        for name, table in self.guest_dict.items():
            if name in message:
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
