"""
婚礼当天时间线数据与查询服务

时间线来源：26.05.16 全天流程（新）.pdf
日期：2026年05月16日
"""

import re
from datetime import date, datetime
from typing import Optional

# ------------------------------------------------------------------ #
# 时间线数据
# ------------------------------------------------------------------ #

# 新娘时间线
BRIDE_TIMELINE = [
    {"time": "05:30", "event": "新娘起床", "location": "新娘家（钱潮府）",
     "detail": "起床洗漱敷面膜，吃早餐"},
    {"time": "06:00", "event": "化妆师到达", "location": "新娘家（钱潮府）",
     "detail": "新娘开始新中式造型，约2h"},
    {"time": "07:00", "event": "伴娘到达", "location": "新娘家（钱潮府）",
     "detail": "自行底妆，化妆师辅助细节，管家协助换伴娘服"},
    {"time": "07:50", "event": "摄影摄像/管家到达", "location": "新娘家（钱潮府）",
     "detail": "拍静物素材，管家归整物料，核对堵门游戏"},
    {"time": "08:20", "event": "新中式拍摄", "location": "新娘家（钱潮府）",
     "detail": "与伴娘拍摄，与父母合影，录制出嫁前素材"},
    {"time": "09:00", "event": "堵门游戏", "location": "新娘家（钱潮府）",
     "detail": "亲友堵门，玩堵门游戏3~4个"},
    {"time": "09:28", "event": "献捧花·穿婚鞋", "location": "新娘家（钱潮府）",
     "detail": "新郎单膝下跪献捧花、告白，穿婚鞋"},
    {"time": "09:38", "event": "敬茶仪式", "location": "新娘家（钱潮府）",
     "detail": "新郎给新娘父母敬茶改口，拍全家福"},
    {"time": "09:50", "event": "新娘出门", "location": "新娘家（钱潮府）",
     "detail": "牵手出门，放礼炮*6，告别父母"},
    {"time": "10:08", "event": "出发去新郎家", "location": "前往新郎家（潮展云起）",
     "detail": "车队出发前往新郎家"},
    {"time": "10:28", "event": "新人进门", "location": "新郎家（潮展云起）",
     "detail": "走红毯进家门，放礼炮*6，长辈给新娘洗脸，喝甜汤圆"},
    {"time": "10:50", "event": "敬茶仪式", "location": "新郎家（潮展云起）",
     "detail": "新娘给新郎父母敬茶改口，拍全家福"},
    {"time": "11:00", "event": "午餐", "location": "新郎家（潮展云起）",
     "detail": "新人、伴团、工作人员家中统一订餐"},
    {"time": "11:40", "event": "换外景纱", "location": "新郎家（潮展云起）",
     "detail": "新娘换外景造型，新郎补妆"},
    {"time": "12:20", "event": "出发外景", "location": "前往上城区民政局",
     "detail": "出发前往婚姻登记处外景拍摄"},
    {"time": "13:00", "event": "拍摄外景", "location": "上城区民政局婚姻登记处",
     "detail": "新人外景拍摄，伴团配合拍摄"},
    {"time": "13:30", "event": "领证", "location": "上城区民政局婚姻登记处",
     "detail": "新人领证，结束后继续拍摄"},
    {"time": "14:20", "event": "返回晚宴酒店", "location": "前往黄龙饭店",
     "detail": "外景拍摄结束，返回晚宴酒店"},
    {"time": "15:00", "event": "换主纱", "location": "黄龙饭店",
     "detail": "新娘换主纱造型，新郎补妆，彩排人员集合"},
    {"time": "15:40", "event": "人像拍摄+彩排", "location": "黄龙饭店",
     "detail": "拍场布照片，新人+双方父母+司仪彩排"},
    {"time": "16:40", "event": "换迎宾纱", "location": "黄龙饭店",
     "detail": "新娘换外景纱，新郎补妆，准备迎宾"},
    {"time": "17:10", "event": "迎宾", "location": "黄龙饭店",
     "detail": "双方父母陪同迎宾，亲友合影留念"},
    {"time": "17:40", "event": "换主纱", "location": "黄龙饭店",
     "detail": "新娘换主纱造型，新郎回到厅内准备晚宴"},
    {"time": "18:18", "event": "晚宴仪式", "location": "黄龙饭店",
     "detail": "晚宴仪式开始"},
    {"time": "18:50", "event": "换敬酒服", "location": "黄龙饭店",
     "detail": "新娘换敬酒服，管家送餐，复核敬酒细节"},
    {"time": "19:10", "event": "敬酒", "location": "黄龙饭店",
     "detail": "双方父母分别陪同敬酒"},
    {"time": "20:30", "event": "婚礼礼成", "location": "黄龙饭店",
     "detail": "婚礼礼成，与宾客告别"},
]

# 新郎时间线
GROOM_TIMELINE = [
    {"time": "06:30", "event": "新郎起床", "location": "新郎家（潮展云起）",
     "detail": "起床洗头洗漱换西装，吃早餐"},
    {"time": "07:00", "event": "化妆师到达", "location": "新郎家（潮展云起）",
     "detail": "新郎妆造，妈妈妆造"},
    {"time": "07:20", "event": "伴郎到达", "location": "新郎家（潮展云起）",
     "detail": "伴郎自行造型，换伴郎服"},
    {"time": "07:30", "event": "摄影摄像到达", "location": "新郎家（潮展云起）",
     "detail": "拍摄新郎伴郎晨间花絮"},
    {"time": "07:50", "event": "婚车集合", "location": "新郎家（潮展云起）",
     "detail": "车辆装饰完毕，等待新郎和伴郎"},
    {"time": "08:08", "event": "准备出发", "location": "新郎家（潮展云起）",
     "detail": "分发喜烟喜糖，拍婚车出发镜头，准备出发接亲"},
    {"time": "08:28", "event": "出发接亲", "location": "前往新娘家（钱潮府）",
     "detail": "男方素材拍摄完毕，出发前往新娘家"},
    {"time": "08:50", "event": "到达新娘家", "location": "新娘家（钱潮府）",
     "detail": "新郎伴郎到达，拍下车镜头，上楼堵门"},
    {"time": "09:00", "event": "堵门游戏", "location": "新娘家（钱潮府）",
     "detail": "伴团亲友堵门，玩堵门游戏3~4个"},
    {"time": "09:28", "event": "献捧花·穿婚鞋", "location": "新娘家（钱潮府）",
     "detail": "新郎单膝下跪献捧花、告白，给新娘穿婚鞋"},
    {"time": "09:38", "event": "敬茶仪式", "location": "新娘家（钱潮府）",
     "detail": "新郎给新娘父母敬茶改口，拍全家福"},
    {"time": "09:50", "event": "新娘出门", "location": "新娘家（钱潮府）",
     "detail": "牵手出门，放礼炮*6，告别父母"},
    {"time": "10:08", "event": "出发回新郎家", "location": "前往新郎家（潮展云起）",
     "detail": "车队出发回新郎家"},
    {"time": "10:28", "event": "新人进门", "location": "新郎家（潮展云起）",
     "detail": "走红毯进家门，放礼炮*6，长辈给新娘洗脸，喝甜汤圆"},
    {"time": "10:50", "event": "敬茶仪式", "location": "新郎家（潮展云起）",
     "detail": "新娘给新郎父母敬茶改口，拍全家福"},
    {"time": "11:00", "event": "午餐", "location": "新郎家（潮展云起）",
     "detail": "新人、伴团、工作人员家中统一订餐"},
    {"time": "11:40", "event": "补妆休息", "location": "新郎家（潮展云起）",
     "detail": "新郎补妆，伴团稍作休息"},
    {"time": "12:20", "event": "出发外景", "location": "前往上城区民政局",
     "detail": "出发前往婚姻登记处外景拍摄"},
    {"time": "13:00", "event": "拍摄外景", "location": "上城区民政局婚姻登记处",
     "detail": "新人外景拍摄，伴团配合拍摄"},
    {"time": "13:30", "event": "领证", "location": "上城区民政局婚姻登记处",
     "detail": "新人领证，结束后继续拍摄"},
    {"time": "14:20", "event": "返回晚宴酒店", "location": "前往黄龙饭店",
     "detail": "外景拍摄结束，返回晚宴酒店"},
    {"time": "15:00", "event": "补妆", "location": "黄龙饭店",
     "detail": "新郎补妆，彩排人员集合"},
    {"time": "15:40", "event": "人像拍摄+彩排", "location": "黄龙饭店",
     "detail": "拍场布照片，新人+双方父母+司仪彩排"},
    {"time": "16:40", "event": "准备迎宾", "location": "黄龙饭店",
     "detail": "新郎补妆，准备迎宾"},
    {"time": "17:10", "event": "迎宾", "location": "黄龙饭店",
     "detail": "双方父母陪同迎宾，亲友合影留念"},
    {"time": "17:40", "event": "准备晚宴", "location": "黄龙饭店",
     "detail": "新郎回到厅内出场位，管家核对开场时间"},
    {"time": "18:18", "event": "晚宴仪式", "location": "黄龙饭店",
     "detail": "晚宴仪式开始"},
    {"time": "18:50", "event": "准备敬酒", "location": "黄龙饭店",
     "detail": "等新娘换敬酒服"},
    {"time": "19:10", "event": "敬酒", "location": "黄龙饭店",
     "detail": "双方父母分别陪同敬酒，伴娘拿婚包+伴郎拿分酒器"},
    {"time": "20:30", "event": "婚礼礼成", "location": "黄龙饭店",
     "detail": "婚礼礼成，与宾客告别"},
]

TIMELINE = {
    "bride": BRIDE_TIMELINE,
    "groom": GROOM_TIMELINE,
}

# 角色别名映射
ROLE_ALIASES = {
    "新娘": "bride",
    "老婆": "bride",
    "女方": "bride",
    "新郎": "groom",
    "老公": "groom",
    "男方": "groom",
}

# 位置查询关键词
LOCATION_KEYWORDS = ["在哪", "在哪里", "位置", "地点", "在哪儿", "去哪了", "在哪了"]


class TimelineManager:
    """婚礼时间线查询服务"""

    def __init__(self):
        self.timeline = TIMELINE

    @staticmethod
    def _time_to_minutes(time_str: str) -> int:
        """将 HH:MM 转为当天的分钟数"""
        parts = time_str.split(":")
        return int(parts[0]) * 60 + int(parts[1])

    def _parse_query_time(self, message: str) -> Optional[int]:
        """
        从消息中解析查询时间，返回分钟数（距0:00）。
        如果没有指定时间，返回 None（表示使用当前时间）。
        """
        # 清理消息
        msg = message.strip()

        # "现在" -> 返回 None，由调用方使用当前时间
        if "现在" in msg or "目前" in msg or "当前" in msg:
            return None

        # 尝试匹配时间模式
        # 优先匹配 "下午3点半" / "上午8点20" / "15点" 等中文表达

        # 模式1：下午/晚上/傍晚 X点Y分(半)
        m = re.search(r'(下午|晚上|傍晚|pm|PM)\s*(\d{1,2})\s*点\s*(?:(\d{1,2})\s*分?|半)?', msg)
        if m:
            hour = int(m.group(2))
            minute = 30 if m.group(0).endswith("半") else (int(m.group(3)) if m.group(3) else 0)
            if hour < 12:
                hour += 12
            return hour * 60 + minute

        # 模式2：上午/早上/凌晨 X点Y分(半)
        m = re.search(r'(上午|早上|凌晨|am|AM)\s*(\d{1,2})\s*点\s*(?:(\d{1,2})\s*分?|半)?', msg)
        if m:
            hour = int(m.group(2))
            minute = 30 if m.group(0).endswith("半") else (int(m.group(3)) if m.group(3) else 0)
            if hour == 12:
                hour = 0
            return hour * 60 + minute

        # 模式3：纯数字时间 "15点20" / "3点半" / "8点"
        m = re.search(r'(\d{1,2})\s*点\s*(?:(\d{1,2})\s*分?|半)?', msg)
        if m:
            hour = int(m.group(1))
            minute = 30 if m.group(0).endswith("半") else (int(m.group(2)) if m.group(2) else 0)
            # 婚礼日语境：1-5点默认为下午，6-12点默认为上午
            if 1 <= hour <= 5 and minute == 0:
                # 仅在整点时模糊推断，有分/半的时间更精确，不做推断
                # 但婚礼日语境，如果只有"3点"更可能指下午
                hour += 12
            elif hour == 12 and minute == 0:
                pass  # 12点 = 中午12点
            return hour * 60 + minute

        # 模式4：HH:MM / HH：MM 格式（支持半角/全角冒号）
        m = re.search(r'(\d{1,2})[：:](\d{2})', msg)
        if m:
            hour = int(m.group(1))
            minute = int(m.group(2))
            return hour * 60 + minute

        # 没有匹配到时间，返回 None
        return None

    def _parse_role(self, message: str) -> Optional[str]:
        """从消息中解析角色（bride/groom），未匹配返回 None"""
        for alias, role in ROLE_ALIASES.items():
            if alias in message:
                return role
        return None

    def is_timeline_query(self, message: str) -> bool:
        """判断消息是否为时间线位置查询"""
        msg = message.strip()
        has_role = any(alias in msg for alias in ROLE_ALIASES)
        has_location = any(kw in msg for kw in LOCATION_KEYWORDS)
        return has_role and has_location

    def query(self, message: str) -> Optional[str]:
        """
        处理时间线位置查询，返回回复文本。
        如果消息不匹配时间线查询，返回 None。

        支持的查询格式：
        - 新郎现在在哪
        - 新娘3点在哪
        - 新郎下午3点半在哪
        - 新娘8点20在哪
        """
        if not self.is_timeline_query(message):
            return None

        role = self._parse_role(message)
        if role is None:
            return None

        # 查找时间线
        timeline = self.timeline[role]
        role_label = "新娘" if role == "bride" else "新郎"

        query_minutes = self._parse_query_time(message)
        is_now_query = query_minutes is None  # 是否为"现在"查询
        not_wedding_day = False
        if is_now_query:
            # "现在"查询：使用当前时间，非婚礼当天加提示
            now = datetime.now()
            query_minutes = now.hour * 60 + now.minute
            wedding_date = date(2026, 5, 16)
            if date.today() != wedding_date:
                not_wedding_day = True

        # 找到查询时间点所在的时间段
        matched_entry = None
        next_entry = None

        for i, entry in enumerate(timeline):
            entry_minutes = self._time_to_minutes(entry["time"])
            if entry_minutes <= query_minutes:
                matched_entry = entry
                next_entry = timeline[i + 1] if i + 1 < len(timeline) else None
            else:
                break

        # 如果查询时间早于第一个时间点
        if matched_entry is None:
            return f"{role_label}在{timeline[0]['time']}之前还未开始准备哦～"

        # 生成回复
        time_display = f"{query_minutes // 60:02d}:{query_minutes % 60:02d}"
        location = matched_entry["location"]
        event = matched_entry["event"]
        detail = matched_entry["detail"]
        entry_time = matched_entry["time"]

        # 判断是否在移动中
        is_transit = location.startswith("前往")

        # 位置措辞："现在在" vs "8:00在"
        loc_prefix = f"{role_label}现在在{location}" if is_now_query else f"{role_label}{time_display}在{location}"

        if is_transit:
            dest = location[2:]  # 去掉"前往"
            transit_status = "在途中🚗" if is_now_query else f"{time_display}在途中🚗"
            if next_entry:
                reply = (
                    f"{role_label}{entry_time}出发{dest}，"
                    f"预计{next_entry['time']}到达，"
                    f"{transit_status}"
                )
            else:
                reply = f"{role_label}{entry_time}出发{dest}，{transit_status}"
        else:
            # 构建活动描述
            time_prefix = f"从{entry_time}开始" if entry_time != time_display else f"在{entry_time}"
            reply = f"{loc_prefix}，{time_prefix}{event}"
            if detail:
                reply += f"（{detail}）"
            # 如果有下一个节点，提示接下来的安排
            if next_entry:
                reply += f"\n📅 下一站：{next_entry['time']} {next_entry['event']}"
                if next_entry["location"] != location:
                    reply += f"（{next_entry['location']}）"

        # 非婚礼当天加提示前缀
        prefix = "（今天不是婚礼日，以下为5月16日同时间段安排）\n" if not_wedding_day else ""
        return prefix + reply
