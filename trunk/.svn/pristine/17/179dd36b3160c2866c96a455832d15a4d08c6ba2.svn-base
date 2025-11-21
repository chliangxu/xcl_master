from src.core.event import EventSystem, Events


class StatusUtils:
    @staticmethod
    def show(message: str, timeout: int = 0):
        """
        显示状态栏消息
        Args:
            message: 要显示的消息文本
            timeout: 超时时间（毫秒），0表示永久显示
        """
        if timeout > 0:
            EventSystem.instance().send_event(Events.STATUS_BAR, {
                "message": message,
                "timeout": timeout
            })
        else:
            EventSystem.instance().send_event(Events.STATUS_BAR, message)

    @staticmethod
    def clear():
        EventSystem.instance().send_event(Events.STATUS_BAR, {"clear": True})
