import sys
from time import sleep

import pygame

from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

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
            (self.settings.screen_width, self.settings.screen_height)
        )
        # self.screen = pygame.display.set_mode(
        #     (0, 0),
        #     pygame.FULLSCREEN
        # )
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        # 窗口名
        pygame.display.set_caption("Alien Invasion")

        # 游戏启动后处于活动妆台
        self.game_active = True

        # 初始化飞船类
        self.ship = Ship(self)

        # 初始化外星人类（编组）
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # 初始化子弹组（编组）
        self.bullets = pygame.sprite.Group()

        # 初始化游戏统计信息类
        self.stats = GameStats(self)        

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 每次循环时都重新绘制屏幕
            # 响应事件
            self._check_events()
            
            if self.game_active:
                # 更新飞船
                self.ship.update()
                # 更新子弹
                self._update_bullets()
                # 更新外星人
                self._update_aliens()
            else: 
                sys.exit()
            
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
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
        
    def _check_keyup_events(self, event):
        """响应释放"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def _fire_bullet(self):
        """创建一颗子弹，并将其加入到编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()   

    def _check_bullet_alien_collision(self):
        """响应子弹和外星人的碰撞"""
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        collissions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # 删除现有的子弹并创建一个新的舰队
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """创建一个外星人舰队"""
        # 创建一个外星人
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            # 添加一行外星人后，重置x值并递增y值
            current_x = alien_width
            current_y += 2 * alien_height  

    def _create_alien(self, x_position, y_position):
        """创建新外星人"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x =  x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """更新外星舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查外星人是否到达了屏幕的下边缘
        self._check_alien_buttom()

    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # RGB - Red, Green, Blue
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()

        self.aliens.draw(self.screen)
        
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            # 将ships_left减1
            self.stats.ships_left -= 1

            # 清空外星人列表和子弹列表
            self.aliens.empty()
            self.bullets.empty()

            # 创建一个新的外星舰队，并将飞船放在屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.game_active = False

    def _check_alien_buttom(self):
        """检查是否有外星人到达了下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break


if __name__ == "__main__":
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()