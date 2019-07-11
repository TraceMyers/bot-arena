import testbot
import pygame as pg
from time import sleep
import os
import math
import random


class Arena:
    def __init__(self):
        pass


class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        

class Positions:
    def __init__(self, p_x, p_y):
        self.p1_top_x = p_x
        self.p1_top_y = p_y
        self.p1_mid_x = p_x + 60
        self.p1_mid_y = p_y + 180
        self.p1_bot_x = p_x + 50
        self.p1_bot_y = p_y + 280

        self.p2_top_x = 1000 - p_x - 140
        self.p2_top_y = p_y 
        self.p2_mid_x = 1000 - p_x - 30
        self.p2_mid_y = p_y + 180
        self.p2_bot_x = 1000 - p_x - 50
        self.p2_bot_y = p_y + 280


def main():
    bot1 = testbot.BattleBot()
    bot2 = testbot.BattleBot()
    arena = Arena()

    pg.init()
    pg.display.set_caption('BattleBot Arena')
    window = pg.display.set_mode((1200, 1200))

    positions = Positions(120, 500)
    bg = Background('arena_imgs\\sf_bg_1_1200.jpg', [-850, 0])
    font = pg.font.Font(f'raleway.ttf', 32)

    run = True
    step = 0
    sparse = get_sparse(bot1, bot2)
    bot_imgs = get_bot_imgs(bot1, bot2)

    attack_counters = [0, 0]
    build_armor = [0, 0]
    build_asp = [0, 0]
    build_att = [0, 0]
    break_down = [0, 0]

    while run:
        if step == 40:
            sparse = get_sparse(bot1, bot2)
            step = 0
        actions = update_battle(bot1, bot2, step, sparse)

        if actions[0] == 'attack':
            pg.mixer.music.load(f'{os.getcwd()}\\arena_sounds\\laser{random.randint(1,3)}.mp3'),
            pg.mixer.music.play(0)
            attack_counters[0] = 6
        elif actions[0] == 'build armor':
            build_armor[0] = 10
        elif actions[0] == 'build action speed':
            build_asp[0] = 10
        elif actions[0] == 'build attack':
            build_att[0] = 10
        elif actions[1] == 'break down':
            break_down[0] = 10

        if actions[1] == 'attack':
            pg.mixer.music.load(f'{os.getcwd()}\\arena_sounds\\laser{random.randint(1,3)}.mp3'),
            pg.mixer.music.play(0)
            attack_counters[1] = 6
        elif actions[1] == 'build armor':
            build_armor[1] = 10
        elif actions[1] == 'build action speed':
            build_asp[1] = 10
        elif actions[1] == 'build attack':
            build_att[1] = 10
        elif actions[1] == 'break down':
            break_down[1] = 10

        run = update_pg(window, positions, bg, font, 
                bot1, bot2, actions, step, bot_imgs, attack_counters,
                build_armor, build_asp, build_att, break_down)
        
        if attack_counters[0] > 0:
            attack_counters[0] -= 1
        if build_armor[0] > 0:
            build_armor[0] -= 1
        if build_asp[0] > 0:
            build_asp[0] -= 1
        if build_att[0] > 0:
            build_att[0] -= 1
        if break_down[0] > 0:
            break_down[0] -= 1

        if attack_counters[1] > 0:
            attack_counters[1] -= 1
        if build_armor[1] > 0:
            build_armor[1] -= 1
        if build_asp[1] > 0:
            build_asp[1] -= 1
        if build_att[1] > 0:
            build_att[1] -= 1
        if break_down[1] > 0:
            break_down[1] -= 1

        step += 1

        if bot1.health <= 0:
            win_text = font.render(f'{bot2.name} WINS!', True, (0, 255, 0), (0, 0, 255))
            text_rect = win_text.get_rect()
            text_rect.center = (600, 600)
            window.blit(win_text, text_rect)
            pg.display.update()
            sleep(4)
            break
        elif bot2.health <= 0:
            win_text = font.render(f'{bot1.name} WINS!', True, (0, 255, 0), (0, 0, 255))
            text_rect = win_text.get_rect()
            text_rect.center = (600, 600)
            window.blit(win_text, text_rect)
            pg.display.update()
            sleep(4)
            break

        sleep(0.05)

    pg.quit()


def get_bot_imgs(bot1, bot2):
    bot1_top = pg.image.load(f'{os.getcwd()}\\arena_bots\\{bot1.color}_top.png')
    bot1_mid = pg.image.load(f'{os.getcwd()}\\arena_bots\\{bot1.color}_mid.png')
    bot1_bot = pg.image.load(f'{os.getcwd()}\\arena_bots\\{bot1.color}_bot.png')

    bot2_top = pg.image.load(f'{os.getcwd()}\\arena_bots\\{bot2.color}_top.png')
    bot2_mid = pg.image.load(f'{os.getcwd()}\\arena_bots\\{bot2.color}_mid.png')
    bot2_bot = pg.image.load(f'{os.getcwd()}\\arena_bots\\{bot2.color}_bot.png')
    bot2_top = pg.transform.flip(bot2_top, True, False)
    bot2_mid = pg.transform.flip(bot2_mid, True, False)
    bot2_bot = pg.transform.flip(bot2_bot, True, False)
    
    laser1 = pg.image.load(f'{os.getcwd()}\\arena_bots\\laser.png')
    laser2 = pg.transform.flip(laser1, True, False)

    return ((bot1_top, bot1_mid, bot1_bot), (bot2_top, bot2_mid, bot2_bot), (laser1, laser2))


def get_sparse(bot1, bot2):
    part_zero_ct_1 = 40 // bot1.action_speed
    part_zero_ct_2 = 40 // bot2.action_speed

    bot1_sparse = [0 for _ in range(part_zero_ct_1 - 1)]
    bot1_sparse.append(1)
    bot2_sparse = [0 for _ in range(part_zero_ct_2 - 1)]
    bot2_sparse.append(1)

    for _ in range(bot1.action_speed - 1):
        bot1_sparse.extend(bot1_sparse)
    for _ in range(bot2.action_speed - 1):
        bot2_sparse.extend(bot2_sparse)

    return (bot1_sparse, bot2_sparse)


def update_battle(bot1, bot2, step, sparse):
    bot1_action = None
    bot2_action = None
    # if bot1 has an action this step
    if sparse[0][step]:
        bot1_action = bot1.get_action()
    # if bot2 has an action this step
    if sparse[1][step]:
        bot2_action = bot2.get_action()

    for i in range(2):
        if i == 0 and bot1_action:
            if bot1_action == 'attack':
                bot2.take_damage(bot1.attack_damage)
            elif bot1_action == 'build armor':
                bot1.build_armor()
            elif bot1_action == 'build action speed':
                bot1.build_action_speed()
            elif bot1_action == 'build attack':
                bot1.build_attack()
            else:
                # just passing back that the bot is breaking down this turn
                pass
        if i == 1 and bot2_action:
            if bot2_action == 'attack':
                bot1.take_damage(bot2.attack_damage)
            elif bot2_action == 'build armor':
                bot2.build_armor()
            elif bot2_action == 'build action speed':
                bot2.build_action_speed()
            elif bot2_action == 'build attack':
                bot2.build_attack()
            else:
                # just passing back that the bot is breaking down this turn
                pass
    return (bot1_action, bot2_action)



def update_pg(window, pos, bg, font, bot1, bot2, actions, 
        step, bot_imgs, attack_counters, 
        build_armor, build_asp, build_att, break_down):
    run = True
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break

    window.fill(white)
    window.blit(bg.image, bg.rect)

    #pg.draw.rect(window, red, (pos.p1_x, pos.p1_y, pos.w, pos.h))
    #pg.draw.rect(window, green, (pos.p2_x, pos.p2_y, pos.w, pos.h))

    #here
    anim_top_1 = animate_top(step)
    anim_mid_1 = animate_mid(step)
    anim_top_2 = animate_top(step + 4)
    anim_mid_2 = animate_mid(step + 4)
    
    if actions[0] != 'attack':
        window.blit(bot_imgs[0][2], (pos.p1_bot_x, pos.p1_bot_y))
        window.blit(bot_imgs[0][1], (pos.p1_mid_x, pos.p1_mid_y + anim_mid_1))
        window.blit(bot_imgs[0][0], (pos.p1_top_x + anim_top_1[0], pos.p1_top_y + anim_top_1[1]))
    else:
        window.blit(bot_imgs[0][2], (pos.p1_bot_x, pos.p1_bot_y))
        window.blit(bot_imgs[0][1], (pos.p1_mid_x, pos.p1_mid_y))
        window.blit(bot_imgs[0][0], (pos.p1_top_x, pos.p1_top_y))

    if actions[1] != 'attack':
        window.blit(bot_imgs[1][2], (pos.p2_bot_x, pos.p2_bot_y))
        window.blit(bot_imgs[1][1], (pos.p2_mid_x, pos.p2_mid_y + anim_mid_2))
        window.blit(bot_imgs[1][0], (pos.p2_top_x + anim_top_2[0], pos.p2_top_y + anim_top_2[1]))
    else:
        window.blit(bot_imgs[1][2], (pos.p2_bot_x, pos.p2_bot_y))
        window.blit(bot_imgs[1][1], (pos.p2_mid_x, pos.p2_mid_y))
        window.blit(bot_imgs[1][0], (pos.p2_top_x, pos.p2_top_y))

    upgrade_text_1 = None
    if attack_counters[0] > 0:
        window.blit(bot_imgs[2][0], (pos.p1_bot_x + 230, pos.p1_bot_y - 190))
    if build_armor[0] > 0:
        upgrade_text_1 = font.render('ARMOR UP!', True, green, blue)
    if build_asp[0] > 0:
        upgrade_text_1 = font.render('ACTION UP!', True, green, blue)
    if build_att[0] > 0:
        upgrade_text_1 = font.render('ATTACK UP!', True, green, blue)
    if break_down[0] > 0:
        upgrade_text_1 = font.render('BREAK DOWN!', True, green, blue)
    if upgrade_text_1 is not None:
        text_rect_1 = upgrade_text_1.get_rect()
        text_rect_1.center = (pos.p1_mid_x + 130, pos.p1_mid_y - 80)
        window.blit(upgrade_text_1, text_rect_1)


    upgrade_text_2 = None
    if attack_counters[1] > 0:
        window.blit(bot_imgs[2][1], (pos.p1_bot_x - 480, pos.p1_bot_y - 190))
    if build_armor[1] > 0:
        upgrade_text_2 = font.render('ARMOR UP!', True, green, blue)
    if build_asp[1] > 0:
        upgrade_text_2 = font.render('ACTION UP!', True, green, blue)
    if build_att[1] > 0:
        upgrade_text_2 = font.render('ATTACK UP!', True, green, blue)
    if break_down[1] > 0:
        upgrade_text_2 = font.render('BREAK DOWN!', True, green, blue)
    if upgrade_text_2 is not None:
        text_rect_2 = upgrade_text_2.get_rect()
        text_rect_2.center = (pos.p1_mid_x + 770, pos.p1_mid_y - 80)
        window.blit(upgrade_text_2, text_rect_2)



    health_text_1 = font.render(f'{round(bot1.health)}%', True, green, blue)
    health_text_2 = font.render(f'{round(bot2.health)}%', True, green, blue)
    text_rect_1 = health_text_1.get_rect()
    text_rect_1.center = (300, 1100)
    text_rect_2 = health_text_2.get_rect()
    text_rect_2.center = (900, 1100)
    window.blit(health_text_1, text_rect_1)
    window.blit(health_text_2, text_rect_2)

    name_1 = font.render(bot1.name, True, white, black)
    name_rect_1 = name_1.get_rect()
    name_rect_1.center = (300, 1150)
    name_2 = font.render(bot2.name, True, white, black)
    name_rect_2 = name_2.get_rect()
    name_rect_2.center= (900, 1150)
    window.blit(name_1, name_rect_1)
    window.blit(name_2, name_rect_2)

    pg.display.update()
    
    return run

def animate_top(step):
    radius = 8

    x_step = step / 40 * (2 * math.pi)
    x_val = math.sin(x_step) * radius
    y_step = step / 40 * math.pi
    y_val = math.sin(y_step) * radius

    return (x_val, y_val)


def animate_mid(step):
    radius = 4

    y_step = step / 40 * (2 * math.pi)
    y_val = math.sin(y_step) * radius
    
    return y_val


if __name__ == '__main__':
    main()
