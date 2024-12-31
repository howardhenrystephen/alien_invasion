import sys

import pygame

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()

        # 时钟控制帧率
        self.clock = pygame.time.Clock()

        # pygame's surface
        self.screen = pygame.display.set_mode((900, 600))
        # 窗口名
        pygame.display.set_caption("Alien Invasion")

        # 设置背景色
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监听键盘和鼠标事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # 每次循环时都重新绘制屏幕
            # RGB - Red, Green, Blue
            self.screen.fill(self.bg_color)
            
            # 让最近绘制的屏幕可见
            pygame.display.flip()

            # 时钟计时
            self.clock.tick(60)


if __name__ == "__main__":
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()