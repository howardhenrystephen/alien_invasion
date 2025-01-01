class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""
    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 800
        self.screen_length = 600
        self.bg_color = (230, 230, 230)

        self.ship_speed = 1.5