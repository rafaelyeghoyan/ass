import pygame

pygame.init()

WIDTH = 580
HEIGHT = 290

screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Mario")
clock = pygame.time.Clock()

current_size = screen.get_size()
info = pygame.display.Info()
fullscreen_size = (info.current_w,info.current_h)
is_fullscreen = False
last_size = current_size

bg = pygame.image.load('images/bg.png').convert_alpha()
walk_left = [
    pygame.image.load('images/player_left/ply-l-1.png').convert_alpha(),
    pygame.image.load('images/player_left/ply-l-2.png').convert_alpha(),
    pygame.image.load('images/player_left/ply-l-3.png').convert_alpha(),
    pygame.image.load('images/player_left/ply-l-4.png').convert_alpha()
]
walk_right = [
    pygame.image.load('images/player_right/ply-r-1.png').convert_alpha(),
    pygame.image.load('images/player_right/ply-r-2.png').convert_alpha(),
    pygame.image.load('images/player_right/ply-r-3.png').convert_alpha(),
    pygame.image.load('images/player_right/ply-r-4.png').convert_alpha()
]


goomba = pygame.image.load('images/Goomba.png').convert_alpha()
goomba_list_in_game = []
player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 5
player_y = 200

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound('sounds/bg-s.mp3')
game_over = pygame.mixer.Sound('sounds/game_over.mp3')

bool_sound = True
def Sound():
    if bool_sound:
        bg_sound.play()


goomba_timer = pygame.USEREVENT + 1
pygame.time.set_timer(goomba_timer,3000)

ovr = pygame.image.load('images/overcharch.png')
ovr_list = []
ovr_x = 0
ovr_timer = pygame.USEREVENT
pygame.time.set_timer(ovr_timer,61000)

label = pygame.font.Font('fonts/Roboto-Black.ttf',40)
lose_label = label.render('Game over',False,'Red')
restart_label = label.render('Play again',False,(255,255,255))
restart_label_rect = restart_label.get_rect(topleft=(180,120))
back_menu = label.render('Back to menu',False,(255,255,255))
back_menu_rect = back_menu.get_rect(topleft=(160,185))

menu_font_size = pygame.font.Font('fonts/Roboto-Regular.ttf',50)
mein_menu = menu_font_size.render('MENU',False,'Red')
play_game = label.render("New Play",False,(255,255,255))
exit_game = label.render('Quit',False,(255,255,255))
play_game_rect = play_game.get_rect(topleft=(200,95))
exit_game_rect = exit_game.get_rect(topleft=(250,150))

menu_bg = pygame.image.load('images/menu_bg.jpg')

bullets_left = 5
magazine = pygame.font.Font('fonts/Roboto-Black.ttf',16)
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []

play_score = 0

gameplay = None

running = True

while running:
    bool_sound = False
    Sound()
    mouse = pygame.mouse.get_pos()
    if gameplay == None:
        screen.blit(menu_bg,(0,-10))
        screen.blit(mein_menu,(220,30))
        screen.blit(play_game,play_game_rect)
        screen.blit(exit_game,exit_game_rect)

        if play_game_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True

        if exit_game_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            running = False
            pygame.quit()

    if gameplay:
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 580, 0))
        play_score += 0.1
        screen_score = magazine.render("Очки:" + str(int(play_score)),False,'Black')
        if play_score == 10:
            play_score += 0.4
            clock.tick(18)
        if play_score == 15:
            play_score += 0.6
            clock.tick(20)
        if play_score == 20:
            play_score += 1
            clock.tick(25)

        screen.blit(screen_score,(500,10))
        bullets_magazine = magazine.render("Патроны: " + str(bullets_left), False, "Black")
        player_rect = walk_left[0].get_rect(topleft=(player_x,player_y))
        screen.blit(bullets_magazine,(30, 10))
        if goomba_list_in_game:
            for (i,el) in enumerate(goomba_list_in_game):
                screen.blit(goomba,el)
                el.x -= 10

                if el.x < -10:
                    goomba_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
            if player_anim_count == 3:
                player_anim_count = 0
            else:
                player_anim_count += 1
            bg_x += 2
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 580:
            player_x += player_speed
            if player_anim_count == 3:
                player_anim_count = 0
            else:
                player_anim_count += 1
            bg_x -= 2
        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8
        if bg_x == -580:
            bg_x = 0
        if ovr_list:
            for (i, el) in enumerate(ovr_list):
                screen.blit(ovr, el)
                el.x -= 10
                if el.x < -10:
                    ovr_list.pop(i)
                if player_rect.colliderect(el):
                    bullets_left += 3
                    ovr_list.pop(i)
        if bullets:
            for (i,el) in enumerate(bullets):
                screen.blit(bullet,(el.x,el.y))
                el.x += 4
                if el.x > 590:
                    bullets.pop(i)
                if goomba_list_in_game:
                    for (index,goomba_el) in enumerate(goomba_list_in_game):
                        if el.colliderect(goomba_el):
                            goomba_list_in_game.pop(index)
                            bullets.pop(i)
    if gameplay == False:
        bool_sound = False
        screen.blit(bg, (bg_x, 0))
        screen.blit(lose_label,(180,50))
        screen.blit(restart_label,restart_label_rect)
        screen.blit(back_menu,back_menu_rect)
        play_score = 0
        is_jump = False
        jump_count = 8
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 0
            goomba_list_in_game.clear()
            bullets.clear()
        if back_menu_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = None
            player_x = 0
            goomba_list_in_game.clear()
            bullets.clear()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.VIDEORESIZE:
            current_size = event.size
        if event.type == goomba_timer:
            goomba_list_in_game.append(goomba.get_rect(topleft=(582,220)))
        if event.type == ovr_timer:
            ovr_list.append(ovr.get_rect(topleft=(582,220)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30,player_y + 25)))
            bullets_left = bullets_left - 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    current_size = fullscreen_size
                    screen = pygame.display.set_mode(current_size,pygame.FULLSCREEN)
                else:
                    current_size = last_size
                    screen = pygame.display.set_mode(current_size,pygame.RESIZABLE)
    clock.tick(15)