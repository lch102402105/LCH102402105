import math
import random
import pygame

# ===== 暖色爱心主题配色 =====
BG_COLOR = (255, 248, 235)        # 米白背景
GRID_COLOR = (245, 224, 190)      # 网格线暖米色
GRID_CELL_COLOR = (255, 242, 219) # 格子底色
HEART_COLOR = (255, 107, 107)     # 爱心暖红
ACCENT_COLOR = (255, 186, 140)    # 箭头暖橙
TEXT_COLOR = (90, 56, 42)         # 文字暖棕
SHAKE_RED = (255, 80, 80)         # 碰撞时爱心变深红
DOT_COLOR = (255, 224, 202)       # 淡色波点
CELL_SIZE = 90
OFFSET_X = 160
OFFSET_Y = 110
FONT_PATH = r"C:\Windows\Fonts\arial.ttf"

# ===== 生成淡色波点背景（只生成一次，避免每帧重复计算）=====
def create_dot_background(width, height):
    bg = pygame.Surface((width, height))
    bg.fill(BG_COLOR)
    random.seed(42)  # 固定种子，每次背景一致
    for _ in range(120):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(3, 7)
        pygame.draw.circle(bg, DOT_COLOR, (x, y), r)
    return bg

# ===== 圆角方格 =====
def draw_rounded_rect(surface, rect, color, radius=12, width=0):
    pygame.draw.rect(surface, color, rect, border_radius=radius, width=width)

# ===== 平滑爱心绘制 =====
def _draw_smooth_heart(surface, cx, cy, size, color):
    s = size
    heart_surf = pygame.Surface((s, s), pygame.SRCALPHA)
    pts = [
        (s * 0.50, s * 0.22),
        (s * 0.38, s * 0.10),
        (s * 0.20, s * 0.12),
        (s * 0.08, s * 0.30),
        (s * 0.10, s * 0.48),
        (s * 0.24, s * 0.62),
        (s * 0.50, s * 0.92),
        (s * 0.76, s * 0.62),
        (s * 0.90, s * 0.48),
        (s * 0.92, s * 0.30),
        (s * 0.80, s * 0.12),
        (s * 0.62, s * 0.10),
    ]
    pygame.draw.polygon(heart_surf, color, pts)
    surface.blit(heart_surf, (cx - s / 2, cy - s / 2))

# ===== 箭头三角形：向外拉开距离，和爱心分离 =====
def _draw_arrow_triangle(surface, cx, cy, direction, size):
    s = size // 4
    gap = size // 2 + 10 # 增加间隔，三角形远离爱心

    if direction == 0:
        pts = [(cx, cy - gap - s),
               (cx - s, cy - gap + 2),
               (cx + s, cy - gap + 2)]
    elif direction == 1:
        pts = [(cx + gap + s, cy),
               (cx + gap - 2, cy - s),
               (cx + gap - 2, cy + s)]
    elif direction == 2:
        pts = [(cx, cy + gap + s),
               (cx - s, cy + gap - 2),
               (cx + s, cy + gap - 2)]
    else:
        pts = [(cx - gap - s, cy),
               (cx - gap + 2, cy - s),
               (cx - gap + 2, cy + s)]
    pygame.draw.polygon(surface, ACCENT_COLOR, pts)

# ===== 爱心+箭头组合，爱心缩小为28 =====
def draw_heart_arrow(surface, direction, cx, cy, shaken=False):
    color = SHAKE_RED if shaken else HEART_COLOR
    size = 28
    _draw_smooth_heart(surface, cx, cy, size, color)
    _draw_arrow_triangle(surface, cx, cy, direction, size)

# ===== 开始界面 =====
def draw_start_screen(screen, font, w, h, bg):
    screen.blit(bg, (0, 0))
    title_font = pygame.font.Font(FONT_PATH, 72)
    title = title_font.render("Arrow Heart", True, HEART_COLOR)
    tip = font.render("Press SPACE to Start", True, TEXT_COLOR)
    screen.blit(title, (w // 2 - title.get_width() // 2, 180))
    screen.blit(tip, (w // 2 - tip.get_width() // 2, 320))

# ===== 游戏主界面 =====
def draw_game_screen(screen, font, game, shake_timer, bg, LEVELS):
    screen.blit(bg, (0, 0))
    info1 = font.render(f"Level:{game.level_idx+1}", True, TEXT_COLOR)
    info2 = font.render(f"Hearts:{game.count_remaining()}", True, TEXT_COLOR)
    info3 = font.render(f"Mistakes:{game.mistake}/{game.max_mistake}", True, TEXT_COLOR)
    restart_tip = font.render("R: Restart", True, ACCENT_COLOR)
    screen.blit(info1, (30, 60))
    screen.blit(info2, (200, 60))
    screen.blit(info3, (380, 60))
    screen.blit(restart_tip, (560, 60))
    board_rows = len(LEVELS[game.level_idx])
    board_cols = len(LEVELS[game.level_idx][0])
    for r in range(board_rows):
        for c in range(board_cols):
            rect = pygame.Rect(
                OFFSET_X + c * CELL_SIZE,
                OFFSET_Y + r * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            )
            draw_rounded_rect(screen, rect, GRID_CELL_COLOR, radius=14)
            draw_rounded_rect(screen, rect, GRID_COLOR, radius=14, width=2)
    for arr in game.arrows:
        if not arr.active:
            continue
        x = OFFSET_X + arr.col * CELL_SIZE + CELL_SIZE // 2
        y = OFFSET_Y + arr.row * CELL_SIZE + CELL_SIZE // 2
        shake_offset = 0
        if arr.shake:
            shake_offset = int(math.sin(shake_timer * 0.5) * 6)
        draw_heart_arrow(screen, arr.dir, x + shake_offset, y, shaken=arr.shake)
    if shake_timer > 20:
        for arr in game.arrows:
            arr.shake = False

# ===== 通关界面 =====
def draw_end_screen(screen, font, w, h, is_win_all, bg):
    screen.blit(bg, (0, 0))
    big_font = pygame.font.Font(FONT_PATH, 60)
    if is_win_all:
        msg = big_font.render("All Clear!", True, HEART_COLOR)
        tip = font.render("Press SPACE to restart", True, TEXT_COLOR)
    else:
        msg = big_font.render("Level Clear!", True, HEART_COLOR)
        tip = font.render("Press SPACE for Next Level", True, TEXT_COLOR)
    screen.blit(msg, (w // 2 - msg.get_width() // 2, 220))
    screen.blit(tip, (w // 2 - tip.get_width() // 2, 320))

# ===== 失败界面 =====
def draw_fail_screen(screen, font, w, h, bg):
    screen.blit(bg, (0, 0))
    big_font = pygame.font.Font(FONT_PATH, 60)
    msg = big_font.render("Game Over", True, SHAKE_RED)
    tip = font.render("Press R to Retry", True, TEXT_COLOR)
    screen.blit(msg, (w // 2 - msg.get_width() // 2, 220))
    screen.blit(tip, (w // 2 - tip.get_width() // 2, 320))

# ===== 坐标转换 =====
def get_click_cell(pos):
    mx, my = pos
    c = (mx - OFFSET_X) // CELL_SIZE
    r = (my - OFFSET_Y) // CELL_SIZE
    return r, c
