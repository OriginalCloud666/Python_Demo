import sys  # 引入sys模块
import random  # 引入random模块
import pygame  # 引入pygame模块
import schedule  # 引入schedule模块
from pygame.locals import *  # 引入全局常量


class Model:
    """游戏类：游戏主体界面"""

    cur_time = 0  # 记录当期时间

    # 图片对象
    live = pygame.image.load(r'./resource/picture/live.png')
    role = pygame.image.load(r'./resource/picture/role.png')
    boom = pygame.image.load(r'./resource/picture/boom.png')

    # 字体对象
    pygame.font.init()  # 初始化
    font1 = pygame.font.Font("./resource/font/my_font.ttf", 22)
    font2 = pygame.font.Font("./resource/font/my_font.ttf", 45)
    font3 = pygame.font.Font("./resource/font/my_font.ttf", 25)

    # 音效对象
    pygame.mixer.init()  # 初始化
    sound1 = pygame.mixer.Sound(r'./resource/music/boom.wav')
    sound2 = pygame.mixer.Sound(r'./resource/music/explode.wav')

    def __init__(self):
        pass

    @staticmethod
    def bgm():  # 音乐模块，播放音乐背景
        pygame.mixer.music.load(r'./resource/music/bk.mp3')
        pygame.mixer.music.set_volume(0.5)  # 设置播放音量
        pygame.mixer.music.play()  # 播放背景音乐

    @staticmethod
    def set():  # 设置模块，设置界面
        icon = pygame.image.load(r'./resource/picture/logo.ico')
        pygame.display.set_icon(icon)  # 设置窗口图标
        pygame.display.set_caption('Python躲避障碍')  # 设置窗口标题

    @staticmethod
    def task(obstacles, role, width):  # 任务模块，定时器执行的任务
        Model.cur_time = Model.cur_time + 1

        x = width / 2  # 障碍物x坐标
        y = 5  # 障碍物y坐标
        speed_x = random.choice([-3, -2, -1, 1, 2, 3]) / 10  # 障碍物x方向速度
        speed_y = random.randint(1, 3) / 10  # 障碍物y方向速度

        # 每间隔两秒，产生一个小球，并且小球数目不超过20
        if Model.cur_time % 2 == 0 and len(obstacles) <= 20:
            radius = 3  # 障碍物半径
            color_r, color_g, color_b = 0, 0, 0  # 障碍物颜色
            obstacle = Obstacle(x, y, speed_x, speed_y, radius, color_r, color_g, color_b)
            obstacles.append(obstacle)

        # 每间隔20秒，增加一种智能障碍物
        if Model.cur_time % 20 == 0 and 10 <= len(obstacles) <= 25:
            radius = 5  # 障碍物半径
            color_r, color_g, color_b = 255, 0, 0  # 障碍物颜色
            intelligent_obstacle = IntelligentObstacle(x, y, speed_x, speed_y, radius, color_r, color_g, color_b)
            obstacles.append(intelligent_obstacle)

        # 每秒更新智能障碍物速度
        for item in obstacles:
            if isinstance(item, IntelligentObstacle):  # 判断是智能障碍物对象
                item.target_point = role.point  # 智能障碍物目标位置
                item.update_for_target()  # 通过目标更新智能障碍物速度

    @staticmethod
    def draw(screen, obstacles, role, width, height):  # 绘制模块，绘制界面
        text1 = Model.font1.render("生命值（Live）：" + str(role.live), True,
                                   pygame.Color(100, 100, 100), pygame.Color(235, 235, 235))
        text2 = Model.font2.render("Game Over!", True,
                                   pygame.Color(100, 100, 100), pygame.Color(235, 235, 235))
        text3 = Model.font3.render("Time：" + str(Model.cur_time) + "（s）", True,
                                   pygame.Color(100, 100, 100), pygame.Color(235, 235, 235))

        screen.fill((235, 235, 235))  # 填充背景颜色，清空旧画面
        screen.blit(text3, (280, 3))  # 显示程序运行时间
        screen.blit(text1, (5, 7))  # 显示角色生命值
        for item in range(role.live):
            screen.blit(role.pic_live, (12 + item * 60, 40))  # 显示生命值图片
        if role.live <= 0:
            screen.blit(text2, (190, 320))  # 显示游戏结束文本
        role.draw(screen)  # 显示角色

        for item in obstacles:
            item.draw(screen)  # 绘制障碍物
            item.update(width, height)  # 更新障碍物位置


class Role:
    """角色类：游戏主要角色"""

    def __init__(self, pic_role, pic_live, x=0, y=0, width=0, height=0, live=3):
        self.__x = x  # 角色x坐标
        self.__y = y  # 角色y坐标
        self.__width = width  # 角色宽度
        self.__height = height  # 角色高度
        self.__live = live  # 角色的生命值
        self.__pic_role = pic_role  # 角色图片
        self.__pic_live = pic_live  # 角色生命值图片

    def draw(self, screen):  # 绘制模块，绘制角色
        screen.blit(self.__pic_role, (self.__x - self.__width / 2, self.__y - self.__height / 2))

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def point(self):
        return self.__x, self.__y

    @property
    def live(self):
        return self.__live

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def pic_role(self):
        return self.__pic_role

    @property
    def pic_live(self):
        return self.__pic_live

    @point.setter
    def point(self, value):
        x, y, width, height = value
        if 0 < x < width and 0 < y < height:
            self.__x = x
            self.__y = y
        else:
            if self.__x < 0:
                self.__x = 1
            elif self.__x > width:
                self.__x = width - 1
            if self.__y < 0:
                self.__y = 1
            elif self.__y > height:
                self.__y = height - 1

    @live.setter
    def live(self, live):
        self.__live = live

    @pic_role.setter
    def pic_role(self, picture):
        self.__pic_role = picture

    @pic_live.setter
    def pic_live(self, picture):
        self.__pic_live = picture


class Obstacle:
    """"障碍类：移动弹跳的障碍物"""

    def __init__(self, x=0, y=0, speed_x=0.0, speed_y=0.0, radius=0, color_r=0, color_g=0, color_b=0):
        self._x = x  # 障碍物x坐标
        self._y = y  # 障碍物y坐标
        self._speed_x = speed_x  # 障碍物x轴速度分量
        self._speed_y = speed_y  # 障碍物y轴速度分量
        self._radius = radius  # 障碍物半径
        self._color_R = color_r  # RGB中的R
        self._color_G = color_g  # RGB中的G
        self._color_B = color_b  # RGB中的B

    def update(self, width, height):  # 更新模块，更新障碍物位置
        self._x = self._x + self._speed_x  # 利用x方向速度更新x坐标
        self._y = self._y + self._speed_y  # 利用y方向速度更新y坐标
        if self._x > width - self._radius or self._x < self._radius:  # 当小球碰到左右边界时，x方向速度反转
            self._speed_x = - self._speed_x
        if self._y > height - self._radius or self._y < self._radius:  # 当小球碰到上下边界时，y方向速度反转
            self._speed_y = - self._speed_y

    def draw(self, screen):  # 绘制模块，绘制障碍物图形
        pygame.draw.circle(screen, (self._color_R, self._color_G, self._color_B),
                           (self._x, self._y), self._radius, self._radius)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def point(self):
        return self._x, self._y

    @property
    def speed(self):
        return self._speed_x, self._speed_y

    @property
    def radius(self):
        return self._radius

    @property
    def color(self):
        return self._color_R, self._color_G, self._color_B

    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y


class IntelligentObstacle(Obstacle):
    """智能障碍物类：继承自Obstacle类，能够根据目标位置移动，向着角色移动"""

    def __init__(self, x=0, y=0, speed_x=0.0, speed_y=0.0, radius=0,
                 color_r=0, color_g=0, color_b=0, target_x=0, target_y=0):
        super().__init__(x, y, speed_x, speed_y, radius, color_r, color_g, color_b)
        self._target_x = target_x  # 目标x坐标
        self._target_y = target_y  # 目标y坐标

    def update_for_target(self):  # 更新模块，根据目标位置更新小球速度
        if self._target_x > self._x:
            self._speed_x = random.randint(1, 2) / 10
        elif self._target_x < self._x:
            self._speed_x = random.randint(-2, -1) / 10
        if self._target_y > self._y:
            self._speed_y = random.randint(1, 2) / 10
        elif self._target_y < self._y:
            self._speed_y = random.randint(-2, -1) / 10

    @property
    def target_point(self):
        return self._target_x, self._target_y

    @target_point.setter
    def target_point(self, value):
        x, y = value
        self._target_x = x
        self._target_y = y


def main():
    """The main method"""

    width = 640  # 窗口宽度
    height = 720  # 窗口高度
    obstacles = []  # 存储所有障碍物信息，初始为空列表

    # 初始化
    pygame.init()

    # 屏幕对象
    screen = pygame.display.set_mode((width, height), 0, 0)  # 创建窗口
    screen.fill((235, 235, 235))  # 设置窗口背景颜色

    # 游戏对象
    model = Model()
    model.set()  # 设置界面
    model.bgm()  # 播放音乐

    # 角色对象
    role = Role(Model.role, Model.live, 0, 0, 80, 68)

    # 每秒执行一次task函数
    schedule.every(1).seconds.do(Model.task, obstacles, role, width)

    # 窗口主循环
    while True:
        # 遍历事件队列
        for event in pygame.event.get():
            if event.type == QUIT:  # 点击右上角的'X'，终止主循环
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # 按下'Esc'键，终止主循环
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEMOTION:  # 鼠标移动，获取鼠标坐标
                if role.live >= 1:  # 生命值还有
                    x, y = pygame.mouse.get_pos()
                    role.point = [x, y, width, height]

        # 角色与障碍物碰撞
        for item in obstacles:
            item.update(width, height)
            if abs(role.x - item.x) <= 25 and abs(role.y - item.y) <= 30:
                role.live -= 1  # 生命值减一
                if role.live >= 1:
                    Model.sound1.play()  # 播放音效
                else:
                    role.pic_role = Model.boom  # 切换图片
                    Model.sound2.play()  # 播放音效
                item.y = 5  # 避免重复碰撞

        # 运行所有可以运行的任务
        schedule.run_pending()

        # 显示整体界面
        Model.draw(screen, obstacles, role, width, height)

        # 重新绘制
        pygame.display.flip()


if __name__ == "__main__":
    main()
