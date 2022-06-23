import sys  # 引入sys模块
import random  # 引入random模块
import pygame  # 引入pygame模块
from pygame.locals import *  # 引入全局常量


class Model:
    """游戏类：游戏主体界面"""

    def __init__(self):
        pass

    @staticmethod
    def bgm():  # 音乐模块，播放背景音乐
        file = r'./resource/music/bk.mp3'  # 音乐路径
        pygame.mixer.music.load(file)  # 加载音乐文件
        pygame.mixer.music.set_volume(0.5)  # 设置播放音量
        pygame.mixer.music.play()  # 播放背景音乐

    @staticmethod
    def set():  # 设置模块，设置界面
        icon = pygame.image.load("./resource/picture/logo.ico")
        pygame.display.set_icon(icon)  # 设置窗口图标
        pygame.display.set_caption('Python疯狂线条')  # 设置窗口标题

    @staticmethod
    def draw(screen, balls, width, height):  # 绘制模块，绘制界面
        for ball in balls:
            ball.draw(screen)
            ball.update(width, height)


class Ball:
    """小球类：弹跳的小球"""

    def __init__(self, x=0, y=0, speed_x=0.0, speed_y=0.0, radius=0, color_r=0, color_g=0, color_b=0):
        self.__x = x  # 圆圈x坐标
        self.__y = y  # 圆圈y坐标
        self.__speed_x = speed_x  # 圆圈x轴速度分量
        self.__speed_y = speed_y  # 圆圈y轴速度分量
        self.__radius = radius  # 圆圈半径
        self.__color_R = color_r  # RGB中的R
        self.__color_G = color_g  # RGB中的G
        self.__color_B = color_b  # RGB中的B

    def update(self, width, height):  # 更新模块，更新小球位置
        self.__x = self.__x + self.__speed_x  # 利用x方向速度更新x坐标
        self.__y = self.__y + self.__speed_y  # 利用y方向速度更新y坐标
        if self.__x > width - self.__radius or self.__x < self.__radius:  # 当小球碰到左右边界时，x方向速度反转
            self.__speed_x = -self.__speed_x
        if self.__y > height - self.__radius or self.__y < self.__radius:  # 当小球碰到上下边界时，y方向速度反转
            self.__speed_y = -self.__speed_y

    def draw(self, screen):  # 绘制模块，绘制小球图形
        pygame.draw.circle(screen, (self.__color_R, self.__color_G, self.__color_B),
                           (self.__x, self.__y), self.__radius, self.__radius)

    @property
    def point(self):
        return self.__x, self.__y

    @property
    def speed(self):
        return self.__speed_x, self.__speed_y

    @property
    def radius(self):
        return self.__radius

    @property
    def color(self):
        return self.__color_R, self.__color_G, self.__color_B


def main():
    """The main method"""

    width = 640  # 窗口宽度
    height = 720  # 窗口高度
    balls = []  # 列表用于存放小球

    # 初始化
    pygame.init()

    # 屏幕对象
    screen = pygame.display.set_mode((width, height), 0, 0)  # 创建窗口
    screen.fill((245, 215, 215))  # 设置窗口背景颜色

    # 游戏对象
    model = Model()
    model.set()  # 设置界面
    model.bgm()  # 播放音乐

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 按下鼠标'左'键，产生小球
                    x, y = pygame.mouse.get_pos()
                    ball = Ball(x, y, random.randint(60, 80) / 100, random.randint(60, 80) / 100, 15,
                                random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                    balls.append(ball)

        # 显示整体界面
        Model.draw(screen, balls, width, height)

        # 重新绘制
        pygame.display.flip()


if __name__ == "__main__":
    main()
