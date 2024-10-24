from nonebot import on_request, RequestSession
from nonebot.permission import SUPERUSER

# 创建一个处理好友请求的事件响应器
friend_request = on_request(priority=1, block=True)

@friend_request.handle()
async def handle_friend_request(session: RequestSession):
    # 检查请求类型是否为好友请求
    if session.event.request_type == "friend":
        # 自动通过好友请求
        await session.approve()
        await session.send("好友请求已通过，欢迎加入！")
