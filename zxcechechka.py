import pygame
from pygame import *
import os
import sys
import pyganim

always_x = 0
always_y = 0
pygame.init()
WIN_WIDTH = 1600  # Ширина создаваемого окна
WIN_HEIGHT = 896  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
pygame.display.set_caption("Adskaya rubilnya")  # Пишем в шапку
FILE_DIR = os.path.dirname(__file__)
PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 64
JUMP_POWER = 25
GRAVITY = 1.4
WIDTH = 192
HEIGHT = 192
MINION_WIDTH = 128
MINION_HEIGHT = 128
MONSTER_WIDTH = 192
MONSTER_HEIGHT = 192
SPRITE_WIDTH = 192
SPRITE_HEIGHT = 192
PLATFORM_COLOR = "#000000"
MINION_COLOR = "#000000"
MONSTER_COLOR = '#000001'
MOVE_EXTRA_SPEED = 4 # Ускорение
JUMP_EXTRA_POWER = 1 # дополнительная сила прыжка
ANIMATION_SUPER_SPEED_DELAY = 0.05
platforms = [] # то, во что мы будем врезаться или опираться
timer = pygame.time.Clock()
COLOR = "#888888"
FPS = 60
clock = pygame.time.Clock()
MOVE_SPEED = 8
ANIMATION_DELAY = 0.1
ANIMATION_DELAY_HIT = 0.15
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами
level = []
pygame.mixer.music.load("music/fonk.mp3")
pygame.mixer.music.play(-1)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image



player_image = load_image('samurai.png')
ANIMATION_STAY = [('%s/data/samurai.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_LEFT = [('%s/data/samurai_left_jump.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/data/samurai_right_jump.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/data/samurai_right_jump.png' % ICON_DIR, 0.1)]
ANIMATION_RIGHT = [load_image('samurai_right_move_1.png'),
                   load_image('samurai_right_move_2.png'),
                   load_image('samurai_right_move_3.png'),
                   load_image('samurai_right_move_4.png'),
                   load_image('samurai_right_move_5.png'),
                   # load_image('samurai_right_move_4.png'),
                   # load_image('samurai_right_move_3.png'),
                   # load_image('samurai_right_move_2.png')
                   ]
ANIMATION_LEFT = [load_image('samurai_left_move_1.png'),
                  load_image('samurai_left_move_2.png'),
                  load_image('samurai_left_move_3.png'),
                  load_image('samurai_left_move_4.png'),
                  load_image('samurai_left_move_5.png'),
                  # load_image('samurai_left_move_4.png'),
                  # load_image('samurai_left_move_3.png'),
                  # load_image('samurai_left_move_2.png')
                  ]
ANIMATION_MINION_MOVE_RIGHT = [load_image('minion_right_1.png'),
                               load_image('minion_right_2.png'),
                               load_image('minion_right_3.png')]
ANIMATION_MINION_MOVE_LEFT = [load_image('minion_left_1.png'),
                              load_image('minion_left_2.png'),
                              load_image('minion_left_3.png')]
ANIMATION_MONSTER_MOVE_RIGHT = [load_image('monster_right_1.png'),
                                load_image('monster_right_2.png'),
                                load_image('monster_right_3.png')]
ANIMATION_MONSTER_MOVE_LEFT = [load_image('monster_left_1.png'),
                               load_image('monster_left_2.png'),
                               load_image('monster_left_3.png')]
ANIMATION_HIT_RIGHT = [load_image('samurai_right_hit_1.png'),
                       load_image('samurai_right_hit_2.png'),
                       load_image('samurai_right_hit_3.png'),
                       load_image('samurai_right_hit_4.png')]
ANIMATION_HIT_LEFT = [load_image('samurai_left_hit_1.png'),
                      load_image('samurai_left_hit_2.png'),
                      load_image('samurai_left_hit_3.png'),
                      load_image('samurai_left_hit_4.png')]
ANIMATION_BLOCKTELEPORT = [load_image('portal_urod_3.png'),
                           load_image('portal_urod_2.png'),
                           load_image('portal_urod_1.png')]
ANIMATION_FIRE = [load_image('fire_1.png'),
                  load_image('fire_2.png'),
                  load_image('fire_3.png')]


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('hello_background_adskaya.png'), (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill([255, 255, 255])
                screen.blit(BackGround.image, BackGround.rect)
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def win_screen():
    fon = pygame.transform.scale(load_image('results.png'), (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)

    string_rendered = font.render(tr.get_tryes(), True, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 400
    intro_rect.x = 575
    screen.blit(string_rendered, intro_rect)

    string_rendered1 = font.render('Вы убили 12 врагов', True, pygame.Color('red'))
    intro_rect1 = string_rendered1.get_rect()
    intro_rect1.top = 600
    intro_rect1.x = 600
    screen.blit(string_rendered1, intro_rect1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                win_screen2()
        pygame.display.flip()
        clock.tick(FPS)


def win_screen2():
    fon = pygame.transform.scale(load_image('you_win.png'), (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def die_screen():
    fon = pygame.transform.scale(load_image('you_died.png'), (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                restart()
        pygame.display.flip()
        clock.tick(FPS)


def restart():
    tr.update()
    hero.teleporting(100, 800)
    for monstric in Monsters_Dict.keys():
        monstric.teleporting(Monsters_Dict[monstric][0], Monsters_Dict[monstric][1])
    main()


class Tryes():
    def __init__(self):
        self.tryes_count = 1

    def update(self):
        self.tryes_count += 1

    def get_tryes(self):
        return f'Попыток потрачено: {self.tryes_count}'


tr = Tryes()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, 140, HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        #        Анимация движения вправо
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()
        #        Анимация движения влево
        boltAnim = []
        boltAnimSuperSpeed = []

        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()

        boltAnim = []
        for anim in ANIMATION_HIT_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY_HIT))
        self.boltAnimHitRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimHitRight.play()

        boltAnim = []
        for anim in ANIMATION_HIT_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY_HIT))
        self.boltAnimHitLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimHitLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def update(self, left, right, up, hit_left, hit_right, running, platforms):
        if hit_right:
            self.image.fill(Color(COLOR))
            self.boltAnimHitRight.blit(self.image, (0, 0))

        if hit_left:
            self.image.fill(Color(COLOR))
            self.boltAnimHitLeft.blit(self.image, (0, 0))

        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                if running and (left or right):  # если есть ускорение и мы движемся
                    self.yvel -= JUMP_EXTRA_POWER  # то прыгаем выше
                self.image.fill(Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(Color(COLOR))
            if running:  # если ускорение
                self.xvel -= MOVE_EXTRA_SPEED  # то передвигаемся быстрее
                if not up:  # и если не прыгаем
                    self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0))  # то отображаем быструю анимацию
            else:  # если не бежим
                if not up:  # и не прыгаем
                    self.boltAnimLeft.blit(self.image, (0, 0))  # отображаем анимацию движения
            if up:  # если же прыгаем
                self.boltAnimJumpLeft.blit(self.image, (0, 0))  # отображаем анимацию прыжка

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(COLOR))
            if running:
                self.xvel += MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimRight.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))

        if not (left or right or hit_right or hit_left):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                x_range = 5000
                for i in range(len(monsters_list)):
                    if abs(self.rect.x - monsters_list[i].cord_check()) < x_range:
                        x_range = abs(self.rect.x - monsters_list[i].cord_check())
                        ans = i
                if (isinstance(p, Minion) or isinstance(p, Monster)) and ((hit_right == True) or (hit_left == True)):
                    monsters_list[ans].monster_die()
                elif isinstance(p, Minion) or isinstance(p, Monster):  # если пересакаемый Monster
                    self.die()  # умираем
                elif isinstance(p, Fire): # если пересакаемый блок - blocks.BlockDie
                    self.die()# умираем
                elif isinstance(p, BlockTeleport):
                    self.teleporting(p.goX, p.goY)
                elif isinstance(p, Finish):
                    win_screen()
                else:
                    if xvel > 0:  # если движется вправо
                        self.rect.right = p.rect.left  # то не движется вправо

                    if xvel < 0:  # если движется влево
                        self.rect.left = p.rect.right  # то не движется влево

                    if yvel > 0:  # если падает вниз
                        self.rect.bottom = p.rect.top  # то не падает вниз
                        self.onGround = True  # и становится на что-то твердое
                        self.yvel = 0  # и энергия падения пропадает

                    if yvel < 0:  # если движется вверх
                        self.rect.top = p.rect.bottom  # то не движется вверх
                        self.yvel = 0  # и энергия прыжка пропадает

    def die(self):
        die_screen()

    def teleporting(self, goX, goY):
        # if self.yvel < 1344:
            self.rect.x = goX
            self.rect.y = goY

    def cord_check(self):
        return self.rect.x, self.rect.y


class Minion(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((MINION_WIDTH, MINION_HEIGHT))
        self.image.fill(Color(MINION_COLOR))
        self.rect = Rect(x, y, MINION_WIDTH, MINION_HEIGHT)
        self.image.set_colorkey(Color(MINION_COLOR))
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = maxLengthUp  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # скорость движения по вертикали, 0 - не двигается
        self.count = 0
        boltAnim = []
        for anim in ANIMATION_MINION_MOVE_RIGHT:
           boltAnim.append((anim, 0.3))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        boltAnim = []
        for anim in ANIMATION_MINION_MOVE_LEFT:
            boltAnim.append((anim, 0.3))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

    def update(self, platforms):  # по принципу героя
        if self.count % 2 == 0:
            self.image.fill(Color(MINION_COLOR))
            self.boltAnimRight.blit(self.image, (0, 0))
        if self.count % 2 == 1:
            self.image.fill(Color(MINION_COLOR))
            self.boltAnimLeft.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
            self.count += 1
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                self.yvel = - self.yvel

    def start_coord(self):
        return self.startX, self.startY

    def cord_check(self):
         return self.rect.x

    def monster_die(self):
        # self.live = False
        self.teleporting(2000, 5000)

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY


class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = maxLengthUp  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # скорость движения по вертикали, 0 - не двигается
        self.count = 0
        boltAnim = []
        for anim in ANIMATION_MONSTER_MOVE_LEFT:
           boltAnim.append((anim, 0.3))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        boltAnim = []
        for anim in ANIMATION_MONSTER_MOVE_RIGHT:
            boltAnim.append((anim, 0.3))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

    def update(self, platforms):  # по принципу героя
        if self.count % 2 == 0:
            self.image.fill(Color(MONSTER_COLOR))
            self.boltAnimRight.blit(self.image, (0, 0))
        if self.count % 2 == 1:
            self.image.fill(Color(MONSTER_COLOR))
            self.boltAnimLeft.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
            self.count += 1
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                self.yvel = - self.yvel

    def cord_check(self):
         return self.rect.x

    def start_coord(self):
        return self.startX, self.startY

    def monster_die(self):
        self.teleporting(2000, 5000)

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


class Platform(sprite.Sprite):
    def __init__(self, tile_type, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = tile_images[tile_type]
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Fire(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/fire.png" % ICON_DIR)
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        boltAnim = []
        for anim in ANIMATION_FIRE:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))


class BlockTeleport(sprite.Sprite):
    def __init__(self, x, y, goX, goY):
        sprite.Sprite.__init__(self)
        self.goX = goX  # координаты назначения перемещения
        self.goY = goY  # координаты назначения перемещения
        self.rect = Rect(x, y, SPRITE_WIDTH, SPRITE_HEIGHT)
        self.image = Surface((SPRITE_WIDTH, SPRITE_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/portal_urod_1.png" % ICON_DIR)
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        boltAnim = []
        for anim in ANIMATION_BLOCKTELEPORT:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))


class Finish(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((SPRITE_WIDTH, SPRITE_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/flag.png" % ICON_DIR)
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, SPRITE_WIDTH, SPRITE_HEIGHT)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l - 50)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def loadLevel():
    global playerX, playerY  # объявляем глобальные переменные, это координаты героя
    levelFile = open('%s/levels/0.txt' % FILE_DIR)
    line = " "
    while line[0] != "/":  # пока не нашли символ завершения файла
        line = levelFile.readline()  # считываем построчно
        if line[0] == "[":  # если нашли символ начала уровня
            while line[0] != "]":  # то, пока не нашли символ конца уровня
                line = levelFile.readline()  # считываем построчно уровень
                if line[0] != "]":  # и если нет символа конца уровня
                    endLine = line.find("|")  # то ищем символ конца строки
                    level.append(line[0: endLine])  # и добавляем в уровень строку от начала до символа "|"


tile_images = {
    'under_floor': load_image('floar_sprite.png'),
    'floor': load_image('floar_upper_sprite.png'),
    'flag': load_image('flag.png')
}
loadLevel()
BackGround = Background('data/hell.png', [0, 0])
animatedEntities = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
monsters = pygame.sprite.Group()
entities = pygame.sprite.Group() # Все объекты
left = right = False    # по умолчанию — стоим
up = False
running = False
hit_right = False
hit_left = False
x = y = 0  # координаты
monstr_count = 0
start_screen()
hero = Player(100, 800)  # создаем героя по (x,y) координатам
entities.add(hero)
tp = BlockTeleport(500, 200, 64, 1920)
entities.add(tp)
platforms.append(tp)
animatedEntities.add(tp)
fl = Finish(6300, 2064)
entities.add(fl)
platforms.append(fl)
mn1 = Minion(2024, 954, 2, 1, 150, 3)
entities.add(mn1)
platforms.append(mn1)
monsters.add(mn1)
mn2 = Minion(2440, 954, 2, 1, 100, 3)
entities.add(mn2)
platforms.append(mn2)
monsters.add(mn2)
mn3 = Minion(4468, 954, 2, 1, 100, 3)
entities.add(mn3)
platforms.append(mn3)
monsters.add(mn3)
mn4 = Minion(5950, 953, 2, 1, 100, 3)
entities.add(mn4)
platforms.append(mn4)
monsters.add(mn4)
mn5 = Minion(1330, 378, 2, 1, 80, 3)
entities.add(mn5)
platforms.append(mn5)
monsters.add(mn5)
mr1 = Monster(1510, 893, 2, 2, 100, 8)
entities.add(mr1)
platforms.append(mr1)
monsters.add(mr1)
mr2 = Monster(3900, 2048, 2, 2, 100, 8)
entities.add(mr2)
platforms.append(mr2)
monsters.add(mr2)
mr3 = Monster(5000, 893, 2, 2, 100, 8)
entities.add(mr3)
platforms.append(mr3)
monsters.add(mr3)
mr4 = Monster(3900, 123, 2, 2, 100, 8)
entities.add(mr4)
platforms.append(mr4)
monsters.add(mr4)
mr5 = Monster(2000, 187, 2, 2, 100, 8)
entities.add(mr5)
platforms.append(mr5)
monsters.add(mr5)
mr6 = Monster(2800, 187, 2, 2, 100, 8)
entities.add(mr6)
platforms.append(mr6)
monsters.add(mr6)
mr7 = Monster(5772, 2043, 2, 2, 100, 8)
entities.add(mr7)
platforms.append(mr7)
monsters.add(mr7)

monsters_list = [mn1, mn2, mn3, mn4, mn5,
                 mr1, mr2, mr3, mr4, mr5, mr6, mr7]
Monsters_Dict = {
    mn1: (mn1.start_coord()), mn2: (mn2.start_coord()), mn3: (mn3.start_coord()), mn4: (mn4.start_coord()),
    mn5: (mn5.start_coord()),
    mr1: (mr1.start_coord()), mr2: (mr2.start_coord()), mr3: (mr3.start_coord()), mr4: (mr4.start_coord()),
    mr5: (mr5.start_coord()), mr6: (mr6.start_coord()), mr7: (mr7.start_coord())
}
count_fon = 0
z = 0


for row in level:  # вся строка
    for col in row:  # каждый символ
        if col == "-":
            pf = Platform('under_floor', x, y)
            entities.add(pf)
            platforms.append(pf)
        if col == "P":
            pr = Platform('flag', x, y)
            entities.add(pr)
            platforms.append(pr)
        elif col == "=":
            pf = Platform('floor', x, y)
            entities.add(pf)
            platforms.append(pf)
        if col == '+':
            fire = Fire(x, y)
            entities.add(fire)
            platforms.append(fire)
            animatedEntities.add(fire)

        x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
    y += PLATFORM_HEIGHT  # то же самое и с высотой
    x = 0
for i in range(14):
    pf = Platform('under_floor', -64, (i + 1) * 64)
    entities.add(pf)
    platforms.append(pf)

total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

camera = Camera(camera_configure, total_level_width, total_level_height)


def main():
    runn = True
    global up, left, right, running, hit_left, hit_right
    left = right = False  # по умолчанию — стоим
    up = False
    running = False
    hit_right = False
    hit_left = False
    while runn:  # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                runn = False
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True
            if e.type == KEYDOWN and e.key == K_x:
                hit_right = True
            if e.type == KEYDOWN and e.key == K_z:
                hit_left = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False
            if e.type == KEYUP and e.key == K_x:
                hit_right = False
            if e.type == KEYUP and e.key == K_z:
                hit_left = False

        screen.blit(BackGround.image, BackGround.rect)  # Каждую итерацию необходимо всё перерисовывать
        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, hit_left, hit_right, running, platforms)  # передвижение
        animatedEntities.update()
        monsters.update(platforms)
        # print(hero.cord_check())
        # entities.draw(screen) # отображение
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()


if __name__ == "__main__":
    main()