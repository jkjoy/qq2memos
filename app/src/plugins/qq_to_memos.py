from nonebot import on_command, on_message, get_driver
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.params import CommandArg
import json
import os
import httpx
from typing import Dict, Any
import logging

# 确保日志目录存在
log_dir = "/app/data"
os.makedirs(log_dir, exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(log_dir, 'memos_bot.log'),
    filemode='a'
)
logger = logging.getLogger(__name__)

# 文件路径
JSON_FILE = "/app/data/data.json"

# 从环境变量获取 MEMOS_API，如果未设置则使用默认值
MEMOS_API = os.getenv("MEMOS_API", "https://memos.ee/api/v1/memos")

# 读取 JSON 数据
def read_json() -> Dict[str, Any]:
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 写入 JSON 数据
def write_json(data: Dict[str, Any]):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 初始化函数
async def init():
    if not os.path.exists(JSON_FILE):
        write_json({})
        logger.info(f"Created new JSON file: {JSON_FILE}")
    logger.info(f"Using Memos API: {MEMOS_API}")

# 注册命令
start = on_command("start", rule=to_me(), priority=5)

@start.handle()
async def handle_start(bot: Bot, event: Event, args: Message = CommandArg()):
    user_id = event.get_user_id()
    token = args.extract_plain_text().strip()
    if not token:
        await start.finish("请提供 Token，格式：/start <token>")
        logger.warning(f"User {user_id} failed to start due to missing token")
        return

    users_data = read_json()
    users_data[user_id] = {"token": token}
    write_json(users_data)

    logger.info(f"User {user_id} started successfully")
    await start.finish("绑定成功！现在您可以直接发送消息，我会将其保存到 Memos。")

# 处理所有消息
memo = on_message(priority=5)

@memo.handle()
async def handle_memo(bot: Bot, event: Event):
    user_id = event.get_user_id()
    message = event.get_message()

    # 检查消息是否在群聊中
    is_group_message = event.message_type == "group"

    # 如果是群聊消息，检查消息是否包含 @ 机器人
    if is_group_message:
        if not any(seg.type == "at" and seg.data.get("qq") == bot.self_id for seg in message):
            return

    users_data = read_json()
    user_info = users_data.get(user_id)

    if not user_info:
        await memo.finish("您还未绑定，请先使用 /start <token> 命令绑定。")
        logger.warning(f"Unstarted user {user_id} attempted to send a memo")
        return

    token = user_info["token"]

    text_content = message.extract_plain_text()

    # 如果消息为空，不处理
    if not text_content.strip():
        return

    # 发送到 Memos
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "content": text_content,  # 直接使用原始文本
                "visibility": "PUBLIC"
            }
            response = await client.post(
                MEMOS_API,
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            logger.info(f"Memo sent successfully for user {user_id}")

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred for user {user_id}: {e}")
            logger.error(f"Response content: {e.response.text}")
            await memo.finish(f"发送失败，错误代码：{e.response.status_code}，请检查您的 Token 和网络连接。")
            return
        except httpx.RequestError as e:
            logger.error(f"Request error occurred for user {user_id}: {e}")
            await memo.finish(f"发送失败，网络请求错误：{str(e)}")
            return
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error occurred for user {user_id}: {e}")
            await memo.finish("发送失败，服务器返回了无效的 JSON 数据。")
            return
        except Exception as e:
            logger.error(f"Unexpected error occurred for user {user_id}: {e}")
            await memo.finish(f"发送过程中发生意外错误：{str(e)}，请稍后重试。")
            return

    await memo.finish("已成功发送到 Memos！")

# 获取驱动器并注册启动事件
driver = get_driver()
driver.on_startup(init)

logger.info("Memos bot plugin initialized")
