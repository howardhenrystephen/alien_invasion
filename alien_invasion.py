import sys

import pygame

from setting import Settings
from ship import Ship

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        # 时钟控制帧率
        self.clock = pygame.time.Clock()

        # pygame's surface

        self.screen = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN
        )
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
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
                # 响应按下
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                # 响应释放
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按下"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        
    def _check_keyup_events(self, event):
        """响应释放"""
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