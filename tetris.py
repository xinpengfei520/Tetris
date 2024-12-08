import pygame
import random

# 初始化pygame
pygame.init()

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('俄罗斯方块')

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# 定义颜色
COLORS = [
    (0, 255, 255),  # 青色
    (255, 255, 0),  # 黄色
    (128, 0, 128),  # 紫色
    (255, 165, 0),  # 橙色
    (0, 0, 255),    # 蓝色
    (0, 255, 0),    # 绿色
    (255, 0, 0)     # 红色
]

# 创建游戏网格
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid():
    # 绘制网格线
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pygame.draw.rect(screen, WHITE, 
                           (x * BLOCK_SIZE + (WINDOW_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2, 
                            y * BLOCK_SIZE, 
                            BLOCK_SIZE, BLOCK_SIZE), 1)
            
            # 如果网格中有方块，绘制方块
            if grid[y][x] != 0:
                pygame.draw.rect(screen, COLORS[grid[y][x] - 1],
                               (x * BLOCK_SIZE + (WINDOW_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2,
                                y * BLOCK_SIZE,
                                BLOCK_SIZE - 1, BLOCK_SIZE - 1))

class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.randint(1, len(COLORS))
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def draw(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        COLORS[self.color - 1],
                        (
                            (self.x + x) * BLOCK_SIZE + (WINDOW_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2,
                            (self.y + y) * BLOCK_SIZE,
                            BLOCK_SIZE - 1,
                            BLOCK_SIZE - 1
                        )
                    )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def can_move(self, dx, dy):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and grid[new_y][new_x] != 0:
                        return False
        return True

    def rotate(self):
        # 矩阵旋转
        self.shape = list(zip(*reversed(self.shape)))
        self.shape = [list(row) for row in self.shape]

    def can_rotate(self):
        # 保存当前形状
        original_shape = self.shape
        # 尝试旋转
        self.rotate()
        # 检查是否可以旋转
        can_rotate = True
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    if (self.x + x < 0 or self.x + x >= GRID_WIDTH or 
                        self.y + y >= GRID_HEIGHT or 
                        (self.y + y >= 0 and grid[self.y + y][self.x + x] != 0)):
                        can_rotate = False
                        break
        # 如果不能旋转，恢复原来的形状
        if not can_rotate:
            self.shape = original_shape
        return can_rotate

# 添加 check_lines 函数到这里（在 Piece 类之后，主游戏循环之前）
def check_lines():
    lines_to_clear = []
    for y in range(GRID_HEIGHT):
        if all(grid[y]):  # 如果一行都是非0（已填充）
            lines_to_clear.append(y)
    
    for line in lines_to_clear:
        # 删除已完成的行
        del grid[line]
        # 在顶部添加新的空行
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    
    return len(lines_to_clear)

def draw_preview_box():
    # ... draw_preview_box 函数的代码保持不变 ...
    pass

def show_pause_screen():
    # ... show_pause_screen 函数的代码保持不变 ...
    pass

# 添加时钟控制
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 1000  # 下落速度（毫秒）

# 创建当前方块和下一个方块
current_piece = Piece()
next_piece = Piece()

# 添加分数系统
score = 0
level = 1
lines_cleared = 0

# 修改主游戏循环
running = True
while running:
    # 控制方块下落速度
    fall_time += clock.get_rawtime()
    clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and current_piece.can_move(-1, 0):
                current_piece.move(-1, 0)
            if event.key == pygame.K_RIGHT and current_piece.can_move(1, 0):
                current_piece.move(1, 0)
            if event.key == pygame.K_DOWN and current_piece.can_move(0, 1):
                current_piece.move(0, 1)
            if event.key == pygame.K_UP:  # 添加旋转功能
                current_piece.can_rotate()

    if fall_time >= fall_speed:
        if current_piece.can_move(0, 1):
            current_piece.move(0, 1)
        else:
            # 将方块固定到网格中
            for y, row in enumerate(current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        grid[current_piece.y + y][current_piece.x + x] = current_piece.color
            
            # 检查并清除完整的行
            cleared_lines = check_lines()
            if cleared_lines > 0:
                lines_cleared += cleared_lines
                score += cleared_lines * 100 * level
                # 每清除10行提高一个等级
                level = lines_cleared // 10 + 1
                # 随着等级提高，下落速度加快
                fall_speed = max(1000 - (level - 1) * 100, 100)
            
            # 创建新方块
            current_piece = Piece()
            
            # 检查游戏是否结束
            if not current_piece.can_move(0, 0):
                running = False
        fall_time = 0

    # 绘制游戏界面
    screen.fill(BLACK)
    draw_grid()
    current_piece.draw()
    
    # 显示分数和等级
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'分数: {score}', True, WHITE)
    level_text = font.render(f'等级: {level}', True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 60))
    
    pygame.display.flip()

# 游戏结束显示
font = pygame.font.Font(None, 48)
game_over_text = font.render('游戏结束!', True, WHITE)
screen.blit(game_over_text, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2))
pygame.display.flip()
pygame.time.wait(2000)  # 等待2秒后关闭

# 退出游戏
pygame.quit()
