import sys

import pygame

from setting import Settings
from ship import Ship

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()

        # 时钟控制帧率
        self.clock = pygame.time.Clock()

        # pygame's surface
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_length)
        )
        # 窗口名
        pygame.display.set_caption("Alien Invasion")


        # 初始化飞船类
        self.ship = Ship(self)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 每次循环时都重新绘制屏幕
            # 响应事件
            self._check_events()
            self.ship.update()
            # 更新屏幕
            self._update_screen()
            # 时钟计时
            self.clock.tick(60)
        
    def _check_events(self):
        """响应按键和鼠标事件"""
        # 监听键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
            
    
    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # RGB - Red, Green, Blue
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        
        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == "__main__":
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()