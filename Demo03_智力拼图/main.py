import sys  # 引入sys模块
import random  # 引入random模块
import pygame  # 引入pygame模块
import schedule  # 引入schedule模块
from pygame.locals import *  # 引入全局常量


class Model:
    """游戏类：游戏主体界面"""

    cur_time = 0  # 记录当前时间
    flag = True  # 游戏结束标记
    MousePoint = [-1, -1]  # 记录鼠标坐标位置
    curPoint = [-1, -1]  # 记录鼠标点击当前图块坐标
    lastPoint = [-1, -1]  # 记录鼠标点击此前图块坐标

    # 图片对象
    background = pygame.image.load(r"./resource/picture/bk.jpg")
    background = pygame.transform.scale(background, (640, 720))

    # 字体对象
    pygame.font.init()  # 初始化
    font1 = pygame.font.Font("./resource/font/my_font.ttf", 25)
    font2 = pygame.font.Font("./resource/font/my_font.ttf", 32)

    # 音效对象
    pygame.mixer.init()  # 初始化
    sound1 = pygame.mixer.Sound(r"./resource/music/click.wav")
    sound2 = pygame.mixer.Sound(r"./resource/music/win.wav")

    def __init__(self):
        pass

    @staticmethod
    def bgm():  # 音乐模块：播放音乐
        pygame.mixer.music.load(r"./resource/music/bk.mp3")
        pygame.mixer.music.set_volume(0.5)  # 设置播放音量
        pygame.mixer.music.play()  # 播放背景音乐

    @staticmethod
    def set():  # 设置模块。设置界面
        icon = pygame.image.load(r"./resource/picture/logo.ico")
        pygame.display.set_icon(icon)  # 设置窗口图标
        pygame.display.set_caption("Python智力拼图")  # 设置窗口标题

    @staticmethod
    def task():  # 任务模块，定时器执行的任务
        Model.cur_time = Model.cur_time + 1

    @staticmethod  # 判断模块。游戏结束条件判断
    def judge(tiles):
        for item in range(0, 16):
            row = item // 4  # 确定行
            col = item % 4  # 确定列
            if tiles.get(item)[0] != row or tiles.get(item)[1] != col:
                Model.flag = False
        return Model.flag

    @staticmethod
    def draw(screen, tiles, size_width, size_height):  # 绘制模块，绘制界面
        # 依照key的值对tiles字典中的value小块图片进行显示
        for i in range(0, 4):
            for j in range(0, 4):
                x = size_width * j
                y = size_height * i
                screen.blit(tiles.get(i * 4 + j)[-1], (x, y))

        # 绘制图块选择框
        if Model.curPoint[0] != -1 and Model.curPoint[1] != -1:
            pygame.draw.circle(screen, pygame.Color(245, 245, 245),
                               (Model.curPoint[0] + size_width / 2, Model.curPoint[1] + size_height / 2), 15, 0)
            pygame.draw.circle(screen, pygame.Color(245, 245, 245),
                               (Model.curPoint[0] + size_width / 2, Model.curPoint[1] + size_height / 2), 30, 5)

        text1 = Model.font1.render("Time：" + str(Model.cur_time) + "（s）", True,
                                   pygame.Color(100, 100, 100), pygame.Color(245, 245, 245))
        text2 = Model.font2.render("You Win!", True,
                                   pygame.Color(100, 100, 100), pygame.Color(245, 245, 245))

        # 绘制程序整体运行时间
        pygame.draw.ellipse(screen, pygame.Color(245, 245, 245), (160, -40, 320, 80), 0)
        screen.blit(text1, (240, 1))

        # 绘制游戏结束文本
        Model.flag = True
        if Model.judge(tiles):
            pygame.draw.ellipse(screen, pygame.Color(245, 245, 245), (160, 320, 320, 80), 0)
            screen.blit(text2, (250, 340))

    @staticmethod
    def get_image(target, x, y, width, height):  # 分割模块，对图片进行分割
        image = pygame.Surface((width, height))
        image.blit(target, (0, 0), (x, y, width, height))
        return image

    @staticmethod
    def swap_image(tiles, i, j):  # 交换模块，交换两个小图块的值value
        temp1 = tiles.get(i)
        temp2 = tiles.get(j)
        tiles[i] = temp2
        tiles[j] = temp1


def main():
    """The main method"""

    width = 640  # 窗口高度
    height = 720  # 窗口宽度
    size_width = 160  # 切割后小块图片宽度
    size_height = 180  # 切割后小块图片高度
    tiles = {}  # 存储图片信息

    # 初始化
    pygame.init()

    # 屏幕对象
    screen = pygame.display.set_mode((width, height), 0, 0)  # 创建窗口
    screen.fill((255, 255, 255))

    # 游戏对象
    model = Model()
    model.set()  # 设置界面
    model.bgm()  # 播放音乐

    # 获取分割后的图片对象并存入tiles字典中
    for item in range(0, 16):
        img = Model.get_image(
            Model.background, (item % 4) * size_width, (item // 4) * size_height, size_width, size_height
        )
        tiles[item] = ((item // 4), (item % 4), img)

    # 重复多次交换小图块的位置
    for item in range(0, 15):
        i = random.randint(0, 15)  # 第一个拼图块序号
        j = random.randint(0, 15)  # 第二个拼图块序号
        Model.swap_image(tiles, i, j)

    # 每秒执行一次task函数
    schedule.every(1).seconds.do(Model.task)

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
            elif event.type == pygame.MOUSEMOTION:
                Model.MousePoint = pygame.mouse.get_pos()  # 鼠标移动，获取鼠标坐标
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 按下鼠标'左'键

                    # 记录前一个当前点的位置
                    Model.lastPoint = [Model.curPoint[0], Model.curPoint[1]]

                    # 正常点击则标记图块，若重复点击则标记消失
                    if Model.curPoint[0] == (Model.MousePoint[0] // size_width) * size_width and \
                            Model.curPoint[1] == (Model.MousePoint[1] // size_height) * size_height:
                        Model.curPoint[0] = -1
                        Model.curPoint[1] = -1
                    else:
                        Model.curPoint[0] = (Model.MousePoint[0] // size_width) * size_width
                        Model.curPoint[1] = (Model.MousePoint[1] // size_height) * size_height

                    # 如果图块被选中，则交换图块
                    if Model.lastPoint[0] != -1 and Model.lastPoint[1] != -1 and \
                            Model.curPoint[0] != -1 and Model.curPoint[1] != -1:
                        Model.swap_image(tiles,
                                         (Model.curPoint[1] // size_height) * 4 + (Model.curPoint[0] // size_width),
                                         (Model.lastPoint[1] // size_height) * 4 + (Model.lastPoint[0] // size_width))
                    Model.sound1.play()

                    # 播放胜利音效
                    Model.flag = True
                    if Model.judge(tiles):
                        Model.sound2.play()

        # 运行所有可以运行的任务
        schedule.run_pending()

        # 显示整体界面
        Model.draw(screen, tiles, size_width, size_height)

        # 重新绘制
        pygame.display.flip()


if __name__ == "__main__":
    main()
