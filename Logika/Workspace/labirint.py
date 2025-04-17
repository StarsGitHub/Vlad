from pygame import *

mixer.init()
mixer.music.load('RustMusic.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.3)
shot = mixer.Sound('shot.wav')
losee = mixer.Sound('losee.wav')
wins = mixer.Sound('wins.wav')

#Клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    #Конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        #Викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
    
        #Кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        #Кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    #Метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Клас головного гравця
class Player(GameSprite):
    #Метод, у якому реалізовано управління спрайтом за кнопками стрілочкам клавіатури
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        #Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    ''' переміщає персонажа, застосовуючи поточну горизонтальну та вертикальну швидкість'''
    def update(self):  
        #Спершу рух по горизонталі
        if player.rect.x <= win_width-80 and player.x_speed > 0 or player.rect.x >= 1 and player.x_speed < 0:
            self.rect.x += self.x_speed
        #Якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False) + sprite.spritecollide(self, barriers_wood, False)
        if self.x_speed > 0: #Йдемо праворуч, правий край персонажа - впритул до лівого краю стіни
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # якщо торкнулися відразу кількох, то правий край - мінімальний із можливих
        elif self.x_speed < 0: #Йдемо ліворуч, ставимо лівий край персонажа впритул до правого краю стіни
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # якщо торкнулися кількох стін, то лівий край - максимальний
        if player.rect.y <= win_height-80 and player.y_speed > 0 or player.rect.y >= 1 and player.y_speed < 0:
            self.rect.y += self.y_speed
        #Якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False) + sprite.spritecollide(self, barriers_wood, False)
        if self.y_speed > 0: #Йдемо вниз
            for p in platforms_touched:
                #Перевіряємо, яка з платформ знизу найвища, вирівнюємося по ній, запам'ятовуємо її як свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: #Йдемо вгору
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) # вирівнюємо верхній край по нижніх краях стінок, на які наїхали
    #Метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self, direction):
        shot.play()
        bullet = Bullet('patron.png', self.rect.centerx-20, self.rect.centery-35, 45, 45, 15, direction)
        bullets.add(bullet)

#Клас спрайту-ворога
class Enemy_h(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, x1, x2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.x1 = x1
        self.x2 = x2

   #рух ворога
    def update(self):
        if self.rect.x <= self.x1:
            self.side = "right"
        if self.rect.x >= self.x2:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy_v(GameSprite):
    side = "up"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, y1, y2):
        #Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.y1 = y1
        self.y2 = y2

   #Рух ворога
    def update(self):
        if self.rect.y <= self.y1: #w1.wall_x + w1.wall_width
            self.side = "down"
        if self.rect.y >= self.y2:
            self.side = "up"
        if self.side == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

#Клас спрайту-кулі
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, direction):
        #Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.direction = direction
    
    #Рух ворога
    def update(self):
        if self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        #Зникає, якщо дійде до краю екрана
        if self.rect.x > win_width+10:
            self.kill()

#Вікно
win_width = 1920
win_height = 1020
window = display.set_mode((win_width, win_height))
display.set_caption("Surv-In-Labirint")
back = transform.scale(image.load("rust.jpg"), (win_width, win_height))

#Група для стін
barriers = sprite.Group()
barriers_wood = sprite.Group()
#Група для ворогів
monsters = sprite.Group()
#Група для куль
bullets = sprite.Group()
#Група для бонусів
bonus = sprite.Group()

#Додаємо стіни(з картинкой і координатами) до групи (barriers)
barriers.add(GameSprite('stenka.png', 220, 650, 35, 265))
barriers.add(GameSprite('stenka.png', 100, 650, 35, 450))
barriers.add(GameSprite('stenka.png', 100, 510, 400, 50))
barriers.add(GameSprite('stenka.png', 600, 510, 375, 50))
barriers.add(GameSprite('stenka.png', 375, 650, 400, 50))
barriers.add(GameSprite('stenka.png', 515, 780, 75, 250))
barriers.add(GameSprite('stenka.png', 220, 780, 200, 50))
barriers.add(GameSprite('stenka.png', 375, 780, 50, 300))
barriers.add(GameSprite('stenka.png', 675, 700, 50, 225))
barriers.add(GameSprite('stenka.png', 775, 510, 50, 190))
barriers.add(GameSprite('stenka.png', 825, 825, 50, 200))
barriers.add(GameSprite('stenka.png', 925, 675, 50, 200))
barriers.add(GameSprite('stenka.png', 825, 825, 150, 50))
barriers.add(GameSprite('stenka.png', 1400, 650, 50, 275))
barriers.add(GameSprite('stenka.png', 1400, 650, 400, 50))
barriers.add(GameSprite('stenka.png', 975, 510, 200, 50))
barriers.add(GameSprite('stenka.png', 975, 675, 100, 50))
barriers.add(GameSprite('stenka.png', 1175, 510, 50, 315))
barriers.add(GameSprite('stenka.png', 1075, 825, 150, 50))
barriers.add(GameSprite('stenka.png', 1075, 825, 50, 85))
barriers.add(GameSprite('stenka.png', 1305, 655, 15, 505))
barriers.add(GameSprite('stenka.png', 1215, 975, 100, 200))
barriers.add(GameSprite('stenka.png', 1215, 510, 175, 50))
barriers.add(GameSprite('stenka.png', 1550, 800, 50, 275))
barriers.add(GameSprite('stenka.png', 1700, 650, 50, 275))
barriers.add(GameSprite('stenka.png', 1500, 450, 50, 200))
barriers.add(GameSprite('stenka.png', 1500, 450, 200, 50))
barriers.add(GameSprite('stenka.png', 100, 335, 35, 175))
barriers.add(GameSprite('stenka.png', 0, 200, 225, 35))
barriers.add(GameSprite('stenka.png', 225, 200, 50, 200))
barriers.add(GameSprite('stenka.png', 375, 200, 50, 310))
barriers.add(GameSprite('stenka.png', 375, 100, 50, 100))
barriers.add(GameSprite('stenka.png', 100, 100, 350, 20))
barriers.add(GameSprite('stenka.png', 425, 100, 300, 20))
barriers.add(GameSprite('stenka.png', 575, 235, 50, 150))
barriers.add(GameSprite('stenka.png', 425, 375, 200, 50))
barriers.add(GameSprite('stenka.png', 575, 225, 275, 50))
barriers.add(GameSprite('stenka.png', 715, 360, 50, 150))
barriers.add(GameSprite('stenka.png', 850, 225, 50, 200))
barriers.add(GameSprite('stenka.png', 1000, 360, 50, 150))
barriers.add(GameSprite('stenka.png', 900, 225, 275, 50))
barriers.add(GameSprite('stenka.png', 1150, 225, 50, 200))
barriers.add(GameSprite('stenka.png', 1325, 100, 65, 410))
barriers.add(GameSprite('stenka.png', 1000, 100, 325, 20))
barriers.add(GameSprite('stenka.png', 810, 0, 100, 125))
barriers.add(GameSprite('stenka.png', 1500, 0, 50, 200))
barriers.add(GameSprite('stenka.png', 1550, 150, 200, 50))
barriers.add(GameSprite('stenka.png', 1500, 200, 50, 150))
barriers.add(GameSprite('stenka.png', 1675, 300, 50, 200))
barriers.add(GameSprite('stenka.png', 1850, 800, 75, 300))
barriers.add(GameSprite('stenka.png', 1850, 450, 100, 50))

#Зовнішній бар'єр
#Зверху
barriers.add(GameSprite('stenka.png', 0, 0, 500, 15))
barriers.add(GameSprite('stenka.png', 500, 0, 500, 15))
barriers.add(GameSprite('stenka.png', 1000, 0, 500, 15))
barriers.add(GameSprite('stenka.png', 1500, 0, 500, 15))
#Внизу
barriers.add(GameSprite('stenka.png', 0, 1010, 500, 15))
barriers.add(GameSprite('stenka.png', 500, 1010, 500, 15))
barriers.add(GameSprite('stenka.png', 1000, 1010, 500, 15))
barriers.add(GameSprite('stenka.png', 1500, 1010, 500, 15))
#Ліворуч
barriers.add(GameSprite('stenka.png', 0, 0, 15, 500))
barriers.add(GameSprite('stenka.png', 0, 500, 15, 500))
barriers.add(GameSprite('stenka.png', 0, 1000, 15, 500))
#Праворуч
barriers.add(GameSprite('stenka.png', 1905, 0, 15, 500))
barriers.add(GameSprite('stenka.png', 1905, 500, 15, 500))
barriers.add(GameSprite('stenka.png', 1905, 1000, 15, 500))

#Спрайти
player = Player('players.png', 15, 925, 80, 80, 0, 0)
monsters.add(Enemy_h('kaban.png', 850, 125, 80, 80, 10, 850, 1235))
monsters.add(Enemy_h('kaban.png', 1735, 525, 80, 80, 10, 1735, 1815))
monsters.add(Enemy_v('kaban.png', 1610, 700, 80, 80, 10, 695, 925))
monsters.add(Enemy_h('kaban.png', 940, 940, 80, 80, 10, 940, 1130))
monsters.add(Enemy_h('kaban.png', 20, 565, 80, 80, 10, 20, 685))
monsters.add(Enemy_h('kaban.png', 425, 125, 80, 80, 10, 425, 850))
monsters.add(Enemy_v('kaban.png', 590, 690, 80, 80, 10, 690, 940))
monsters.add(Enemy_h('kaban.png', 900, 435, 80, 80, 10, 770, 912))
monsters.add(Enemy_h('kaban.png', 830, 565, 80, 80, 10, 830, 1085))
monsters.add(Enemy_v('kaban.png', 1410, 15, 80, 80, 10, 15, 575))
monsters.add(Enemy_h('kaban.png', 1055, 435, 80, 80, 10, 1055, 1245))
monsters.add(Enemy_v('kaban.png', 1455, 700, 80, 80, 10, 695, 925))

monsters.add(Enemy_v('medved.png', 140, 200, 70, 70, 10, 230, 440))
monsters.add(Enemy_v('medved.png', 140, 200, 70, 70, 10, 230, 440))
monsters.add(Enemy_v('medved.png', 140, 200, 70, 70, 10, 230, 440))

monsters.add(Enemy_h('medved.png', 140, 25, 70, 70, 10, 140, 675))
monsters.add(Enemy_h('medved.png', 140, 25, 70, 70, 10, 140, 675))
monsters.add(Enemy_h('medved.png', 140, 25, 70, 70, 10, 140, 675))

monsters.add(Enemy_h('medved.png', 1550, 210, 80, 80, 10, 1550, 1815))
monsters.add(Enemy_h('medved.png', 1550, 210, 80, 80, 10, 1550, 1815))
monsters.add(Enemy_h('medved.png', 1550, 210, 80, 80, 10, 1550, 1815))

#Дерев'яні стіни 
barriers_wood.add(GameSprite('derevo.png', 515, 700, 75, 80))
barriers_wood.add(GameSprite('derevo.png', 100, 235, 35, 100))
barriers_wood.add(GameSprite('derevo.png', 425, 225, 150, 25))
barriers_wood.add(GameSprite('derevo.png', 1725, 450, 125, 50))
barriers_wood.add(GameSprite('derevo.png', 1675, 500, 50, 150))
barriers_wood.add(GameSprite('derevo.png', 715, 275, 50, 85))
barriers_wood.add(GameSprite('derevo.png', 1000, 275, 50, 85))
barriers_wood.add(GameSprite('derevo.png', 220, 910, 35, 100))
barriers_wood.add(GameSprite('derevo.png', 1225, 650, 90, 15))
barriers_wood.add(GameSprite('derevo.png', 1315, 650, 85, 15))

#Бонус
bonus.add(GameSprite('monetka.png', 275, 850, 65, 65))
bonus.add(GameSprite('monetka.png', 465, 275, 65, 65))
bonus.add(GameSprite('monetka.png', 885, 910, 65, 65))
bonus.add(GameSprite('monetka.png', 1575, 550, 65, 65))
num = 0 
#Фінальний спрайт(вихід з лабіринта)
final_sprite = GameSprite('exit.png', 1575, 45, 100, 100)

#Рахування монстрів та
monsters_all = 21
moneta = 0

#Змінна, що відповідає за те, як закінчилася гра
finish = False
#Ігровий цикл
run = True
while run:
    #Цикл спрацьовує кожну 0.05 секунд
    time.delay(50)
        #Перебираємо всі події, які могли статися
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                player.x_speed = -10
                player.image = transform.scale(image.load('players.png'),(80, 80))
            elif e.key == K_RIGHT:
                player.x_speed = 10
                player.image = transform.scale(image.load('players2.png'), (80, 80))
            elif e.key == K_UP:
                player.y_speed = -10
            elif e.key == K_DOWN:
                player.y_speed = 10
            elif e.key == K_d:
                player.fire('right')
            elif e.key == K_a:
                player.fire('left')
            elif e.key == K_s:
                player.fire('down')
            elif e.key == K_w:
                player.fire('up')

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                player.x_speed = 0
            elif e.key == K_RIGHT:
                player.x_speed = 0 
            elif e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_DOWN:
                player.y_speed = 0

#Перевірка, що гра ще не завершена
    if not finish:
        #Оновлюємо фон кожну ітерацію
        window.blit(back, (0, 0)) #зафарбовуємо вікно кольором
        
        #Запускаємо рухи спрайтів
        player.update()
        bullets.update()
        monsters.update()
        #Оновлюємо їх у новому місці при кожній ітерації циклу
        player.reset()
        #Рисуємо стіни
        barriers.draw(window)
        barriers_wood.draw(window)
        #Рисуємо постріл
        bullets.draw(window)
        #Рисуємо монетки
        bonus.draw(window)
        #Рисуємо монстрів
        monsters.draw(window)
        #Зіткнення пуль з стінами та монстрами
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, barriers_wood, True, True)
        
        if sprite.groupcollide(monsters, bullets, True, True):
            moneta += 1

        if moneta == 21:
            bonus.add(GameSprite('monetka.png', 840, 435, 65, 65))
            moneta = 0

        if sprite.spritecollide(player, bonus, True):
            num += 1

        bonus.draw(window)
        #Перевірка зіткнення героя з ворогом та фінальним спрайтом
        if sprite.spritecollide(player, monsters, False):
            finish = True
            mixer.music.stop()
            losee.play()
            img = image.load('lose.png')
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
        #Рахування бонусів(якщо 5, то можна вийти з лабіринта)
        if num == 5:
            final_sprite.reset()        
            if sprite.collide_rect(player, final_sprite):
                finish = True
                mixer.music.stop()
                wins.play()
                img = image.load('wins.png')
                window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

    display.update()