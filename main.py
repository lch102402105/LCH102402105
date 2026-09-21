import pygame
from game_core import Game
from ui import create_dot_background, draw_start_screen, draw_game_screen, draw_end_screen, draw_fail_screen, get_click_cell
from levels import LEVELS

# 初始化pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arrow Heart")
font = pygame.font.Font(r"C:\Windows\Fonts\arial.ttf", 24)
bg = create_dot_background(WIDTH, HEIGHT)

game_state = "start" # start / playing / win / lose
game = Game()
shake_timer = 0

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "start":
                    game_state = "playing"
                elif game_state == "win":
                    # 按下空格才切换关卡
                    is_all_clear = game.next_level()
                    if is_all_clear:
                        # 所有关卡打完，重置游戏回到首页
                        game = Game()
                        game_state = "start"
                    else:
                        # 还有下一关，进入游戏
                        game_state = "playing"
            if event.key == pygame.K_r:
                game = Game()
                game_state = "playing"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_state == "playing":
            row, col = get_click_cell(event.pos)
            res = game.click_arrow(row, col)
            if res == "block":
                shake_timer = 30
            if game.is_win():
                game_state = "win"
            if game.is_lose():
                game_state = "lose"

    if shake_timer > 0:
        shake_timer -= 1

    if game_state == "start":
        draw_start_screen(screen, font, WIDTH, HEIGHT, bg)
    elif game_state == "playing":
        draw_game_screen(screen, font, game, shake_timer, bg, LEVELS)
    elif game_state == "win":
        # 判断是否是最后一关，传给绘图函数
        final_clear = (game.level_idx +1 >= len(LEVELS))
        draw_end_screen(screen, font, WIDTH, HEIGHT, final_clear, bg)
    elif game_state == "lose":
        draw_fail_screen(screen, font, WIDTH, HEIGHT, bg)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
