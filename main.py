from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类


# 注册插件
@register(name="CuteVideo", description="langbot插件lagrange看妹妹", version="0.1", author="doubleJazzCat")
class CuteVideo(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.command_pattern = re.compile(r'^\s*看妹妹\s*$')

    # 异步初始化
    async def initialize(self):
        pass

    async def send_msg(self, msg_type, id_type, id):
        try:
            conn = http.client.HTTPConnection("lagrange", 2333)
            payload = json.dumps({
                "message_type" : msg_type,
                id_type: id,
                "message": {
                    "type": "video",
                    "data": {
                        "file": "https://api.dwo.cc/api/videos",
                        "url": "https://api.dwo.cc/api/videos"
                    }
                }
            })
            headers = {
                'Content-Type': 'application/json'
            }
            conn.request("POST", "/send_msg", payload, headers)
            res = conn.getresponse()
            data = json.loads(res.read().decode('utf-8'))
            if data.get('retcode') == 0:
                message_id = data.get('data', {}).get('message_id')
                self.ap.logger.debug(f"消息发送成功，message_id: {message_id}")
                return True
            else:
                self.ap.logger.error(f"API请求失败: {data}")
                return False
        except Exception as e:
            self.ap.logger.error(f"发送消息时发生错误: {str(e)}")
            return False

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        # 这里的 event 即为 PersonNormalMessageReceived 的对象
        if self.command_pattern.match(ctx.event.text_message):
            if not await self.send_msg("private", "user_id", ctx.event.launcher_id):
                # 回复消息
                ctx.add_return("reply", ["抱歉，发送视频失败了，请稍后再试~"])
            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        # 这里的 event 即为 PersonNormalMessageReceived 的对象
        if self.command_pattern.match(ctx.event.text_message):
            if not await self.send_msg("group", "group_id", ctx.event.launcher_id):
                # 回复消息
                ctx.add_return("reply", ["抱歉，发送视频失败了，请稍后再试~"])
            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass
