import random
from pygame import *
import pyautogui
from sys import exit



class Angel(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)

        #绘制天使形状
        self.image = image.load("img\\Angel\\Angel.png")
        self.image = transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()

        #设置天使生命值
        self.lives = 12

    def update(self):
        #处理键盘输入控制天使的移动
        tasten = key.get_pressed()
        if tasten[K_w]:
            self.rect.y -= 3
        if tasten[K_s] and self.rect.bottom < height:
            self.rect.y += 3
        if tasten[K_a] and self.rect.x > 0:
            self.rect.x -= 3
        if tasten[K_d] and self.rect.right < width:
            self.rect.x += 3

        # 处理 'l' 键和天使到达顶部的情况，开始下一关卡
        if (tasten[K_l] and self.rect.bottom < height) or self.rect.top < 25:
            startLevel(min(level + 1, len(vxRanges)))

class Monster(sprite.Sprite):
    def __init__(self,monster_type):
        sprite.Sprite.__init__(self)

        #绘制怪物形状
        if monster_type == 1:
            self.image = image.load("img\\Monster\\Monster_1.png")
        elif monster_type == 2:
            self.image = image.load("img\\Monster\\Monster_2.png")
        elif monster_type == 3:
            self.image = image.load("img\\Monster\\Monster_3.png")
        elif monster_type == 4:
            self.image = image.load("img\\Monster\\Monster_4.png")
        else:
            # 默认使用怪物1的图片
            self.image = image.load("img\\Monster\\Monster_1.png")

        self.image = transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()

        #设置怪物的下落速度
        self.vy = 1

        #将怪物添加到精灵组中
        monster.add(self)

    def update(self):

        #更新怪物的位置
        self.rect.y += self.vy
        self.rect.x = (self.rect.x + self.vx) % width

        #如果怪物到达屏幕底部则将其移除
        if self.rect.y > height - 50:
            monster.remove(self)

        #如果天使的生命值大于0且与怪物碰撞则减少天使的生命值并重新开始关卡
        if angel.lives > 0 and self.rect.colliderect(angel.rect):
            angel.lives -= 1
            collide_effect = image.load("img\\collide.png")
            collide_effect = transform.scale(collide_effect, (40, 40))
            screen.blit(collide_effect, self.rect.topleft)
            
            collision_sound.play()
            startLevel()
            


vxRanges = ((0, 0), (0, 0), (-1, 1), (1, 2), (0, 0), (-1, 1), (-1, 1), (-2, 2), (-2, 2), (-2, 2), (-2, 2), (-3, 3), (0, 0))
vyRanges = ((1, 1), (1, 2), (1, 2), (1, 2), (1, 3), (1, 2), (1, 2), (1, 2), (1, 2), (1, 3), (1, 3), (1, 3), (0, 0))
freqs = (0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.25, 0.25, 0.3, 0.3, 0.4, 0.4, 0)
clock = time.Clock()
angel = Angel()

def write(s, x, y, center=0):
    text = fnt.render(s, True, Color("white"))
    screen.blit(text, (x - center * text.get_width() / 2, y))

def introduce():
    write("你好,小天使", width / 2, height / 2 - 90, 1)
    write("现在你要返回天空", width / 2, height / 2 - 50, 1)
    write("回家吧", width / 2, height / 2, 1)
    write("记得躲避怪物哦",width / 2, height / 2 + 40, 1)
    write("WASD移动",width / 2, height / 2 + 80, 1)
    write("ESC返回",width / 2, height / 2 + 120, 1)


def updateMonster():
    if random.random() < freqs[level - 1]:
        # 根据关卡信息选择不同的怪物类型
        if 1 <= level <= 3:
            monster_type = 1
        elif 4 <= level <= 6:
            monster_type = 2
        elif 7 <= level <= 9:
            monster_type = 3
        elif 10 <= level <= 12:
            monster_type = 4
        else:
            monster_type = 1
        f = Monster(monster_type)
        f.rect.x = random.randint(0, 3 * width)
        f.rect.bottom = 0
        f.vx = random.randint(*vxRanges[level - 1])
        f.vy = random.randint(*vyRanges[level - 1])

        if difficulty == "easy":
            f.vx *= 1
            f.vy *= 1
        
        elif difficulty == "normal":
            f.vx *= 2
            f.vy *= 2

        elif difficulty == "hard":
            f.vx *= 3
            f.vy *= 3

    monster.update()

def startLevel(lvl=0):
    global level
    angel.rect.x = width / 2
    angel.rect.bottom = height
    if lvl:
        level = lvl
        for i in range(800):
            updateMonster()

def chooseDifficulty():
    selected_difficulty = None

    while selected_difficulty is None:
        for ev in event.get():
            if ev.type == QUIT:
                exit(0)
            elif ev.type == KEYDOWN:
                if ev.key == K_1:
                    selected_difficulty = "easy"
                elif ev.key == K_2:
                    selected_difficulty = "normal"
                elif ev.key == K_3:
                    selected_difficulty = "hard"
            elif ev.type == MOUSEBUTTONDOWN:
                # 获取鼠标点击位置
                mouse_x, mouse_y = ev.pos

                # 调整鼠标点击的位置来选择难度
                if 300 <= mouse_x <= 600 and 220 <= mouse_y <= 250:
                    selected_difficulty = "easy"
                elif 300 <= mouse_x <= 600 and 260 <= mouse_y <= 290:
                    selected_difficulty = "normal"
                elif 300 <= mouse_x <= 600 and 300 <= mouse_y <= 330:
                    selected_difficulty = "hard"

        screen.fill((0, 0, 0))
        background_image = image.load("img\\background\\background_2.png")
        background_image = transform.scale(background_image, (width, height))
        screen.blit(background_image, (0, 0))

        write("天使和怪物", width / 2, height / 2 - 230, 1)
        write("简单", width / 2, height / 2 - 50, 1)
        write("普通", width / 2, height / 2 , 1)
        write("困难", width / 2, height / 2 + 50, 1)
        display.flip()

    return selected_difficulty


monster = sprite.RenderPlain()
init()
#音乐
mixer.init()
mixer.music.load('music\\background_music.mp3')
mixer.music.play(-1)
collision_sound = mixer.Sound('music\\collision_sound.mp3')
failure_sound = mixer.Sound('music\\failure_sound.mp3')
victory_sound = mixer.Sound('music\\victory_sound.mp3')
#窗口
width = 900
height = 540
window = display.set_mode((width,height))
screen = display.get_surface()
#背景
background_images = [
    "img\\background\\background_1.png",
    "img\\background\\background_2.png",
    "img\\background\\background_3.png",
    "img\\background\\background_4.png",
]
#字体
chinese_font = "font\\simfang.ttf"
fnt = font.Font(chinese_font,20)

difficulty = chooseDifficulty()
startLevel(1)
while True:
    for ev in event.get():
        if ev.type == QUIT:
            exit(0)
        elif ev.type == KEYDOWN:
            if ev.key == K_ESCAPE:  # 按下 ESC 键
                difficulty = chooseDifficulty()
                startLevel(1)
    
    screen.fill((0, 0, 0))

    # 根据当前关卡选择背景图片
    if level <= 3:
        background_image = image.load(background_images[0])
    elif (4<= level <=6 ):
        background_image = image.load(background_images[1])
    elif (7<= level <=9 ):
        background_image = image.load(background_images[2])
    else:
        background_image = image.load(background_images[3])

    background_image = transform.scale(background_image, (width, height))
    screen.blit(background_image, (0, 0))

    #显示天使的生命值
    write("生命: %d" % angel.lives, width - 120, 20)
    if level < len(vxRanges):
        # 显示关卡信息，更新怪物，绘制怪物
        write("关卡: %d/%d" % (level, len(vxRanges) - 1), width - 120, 40)
        updateMonster()
        monster.draw(screen)
    else:
        # 恭喜通关消息
        victory_sound.play()
        mixer.music.stop()
        write("恭喜,欢迎回家!", width / 2, height / 2 - 10, 1)
    if angel.lives > 0:
        # 更新天使位置，绘制天使
        angel.update()
        screen.blit(angel.image, angel.rect.topleft)
    else:
        # 游戏结束消息和重新开始提示
        mixer.music.stop()
        failure_sound.play()
        
        write("回家失败", width / 2, height / 2 - 40, 1)
        write("请按 'n' 重新开始.", width / 2, height / 2 + 40, 1)
    if key.get_pressed()[K_n]:
        mixer.music.play(-1)
        angel.lives = 12
        startLevel(1)

    if level == 1 and angel.lives == 12 and angel.rect.bottom == height:
        introduce()

    display.flip()

    clock.tick(40)

    