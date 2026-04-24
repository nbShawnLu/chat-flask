import hashlib
import json
import logging
import os
import time
import xml.etree.ElementTree as ET

from flask import request, Response

logger = logging.getLogger(__name__)


class WechatService:
    """
    微信公众号消息服务：负责URL鉴权和消息回复
    """

    def __init__(self, token: str = None):
        # 优先使用传入的token，否则读取环境变量，最后使用默认值
        self.token = token or os.getenv("WECHAT_TOKEN", "wedding2026")

    # ------------------------------------------------------------------ #
    # 公共入口
    # ------------------------------------------------------------------ #

    def handle(self):
        """统一入口，根据请求方法分发"""
        if request.method == "GET":
            return self._handle_get()
        return self._handle_post()

    # ------------------------------------------------------------------ #
    # GET：微信服务器URL验证
    # ------------------------------------------------------------------ #

    def _handle_get(self):
        signature = request.args.get("signature", "")
        timestamp = request.args.get("timestamp", "")
        nonce = request.args.get("nonce", "")
        echostr = request.args.get("echostr", "")

        if echostr and signature and timestamp and nonce:
            if self._verify_signature(timestamp, nonce, signature):
                logger.info(f"[WechatService GET] 验证成功, 返回echostr: {echostr}")
                return Response(echostr, mimetype="text/plain")
            else:
                logger.warning(
                    f"[WechatService GET] 签名验证失败, "
                    f"signature={signature}, timestamp={timestamp}, nonce={nonce}"
                )
                return Response("signature verify failed", status=403, mimetype="text/plain")

        logger.info("[WechatService GET] 无验证参数, 返回运行状态")
        return Response("wechat bot is running", mimetype="text/plain")

    # ------------------------------------------------------------------ #
    # POST：处理微信消息
    # ------------------------------------------------------------------ #

    def _handle_post(self):
        try:
            msg = request.get_json()

            if msg and msg.get("MsgType") == "text":
                reply_content = self._gen_reply(msg)
                logger.info(
                    f"[WechatService POST] 文本消息回复: "
                    f"From={msg.get('FromUserName', '')}, Content={reply_content}"
                )
                return Response(
                    self._build_text_reply(msg, reply_content),
                    mimetype="application/json",
                )
            else:
                msg_type = msg.get('MsgType', 'unknown') if msg else 'empty'
                logger.info(f"[WechatService POST] 暂不处理, MsgType={msg_type}")
                return "success"
        except Exception as e:
            logger.error(f"[WechatService POST] 异常: {str(e)}")
            return str(e)

    # ------------------------------------------------------------------ #
    # 工具方法
    # ------------------------------------------------------------------ #

    def _verify_signature(self, timestamp: str, nonce: str, signature: str) -> bool:
        """验证微信服务器签名"""
        tmp = sorted([self.token, timestamp, nonce])
        return hashlib.sha1("".join(tmp).encode()).hexdigest() == signature

    @staticmethod
    def _parse_xml(xml_data: str) -> dict:
        """将微信推送的XML消息解析为字典（保留以兼容旧格式）"""
        root = ET.fromstring(xml_data)
        return {child.tag: child.text for child in root}

    @staticmethod
    def _gen_reply(msg: dict) -> str:
        """根据消息内容生成回复文本，可在此处扩展业务逻辑"""
        return "你好，欢迎参加我们的婚礼！"

    @staticmethod
    def _build_text_reply(msg: dict, content: str) -> str:
        """构造文本类型的JSON回复报文"""
        return json.dumps({
            "ToUserName": msg.get("FromUserName", ""),
            "FromUserName": msg.get("ToUserName", ""),
            "CreateTime": int(time.time()),
            "MsgType": "text",
            "Content": content,
        }, ensure_ascii=False)
