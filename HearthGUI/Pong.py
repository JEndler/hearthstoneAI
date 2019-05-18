import pygame
import random
 
pygame.init()
 
screen = pygame.display.set_mode([600, 480])
info = pygame.display.Info()
print(info)
pygame.display.set_caption("Pong!")
 
running = True
 
W = screen.get_width()
H = screen.get_height()
FPS = 30
 
 
ball = pygame.Surface([10, 10])
linex = pygame.Surface([10, 0])
pygame.draw.circle(ball, (0, 255, 0), (5, 5), 5)
BOARD_COLORS = [(200, 0, 0), (0, 0, 200)]
linex = pygame.Surface([10, H])
liney = pygame.Surface([10, H])
linex.fill((50, 50, 50))
liney.fill((50, 50, 50))
hit = True
lasthit = False
start = 0
 
board = [None, None]
for p in [0, 1]:
    board[p] = pygame.Surface([12, 40])
    board[p].fill(BOARD_COLORS[p])
 
font = pygame.font.SysFont("Times New Roman", 10)
scoreFont = pygame.font.SysFont("Times New Roman", 20, bold=True)
 
ball_x = W / 2
ball_y = H / 2
 
 
def randomDir():
    # return pygame.math.Vector2(random.random()+.1, random.random()+.1).normalize()
    return pygame.math.Vector2(random.randint(0, 1) * 2 - 1, 1).normalize()
 
 
ball_dir = randomDir()
ball_speed = 160  # px/s
INC = 4
 
downbally = True
opx = False
 
boardx = [20, W - 20]
boardy = [H / 2, H / 2]
score = [0, 0]
 
clock = pygame.time.Clock()
 
cur_fps = FPS
 
t = 0
 
 
def wrap(x, x_max, x_min=0):
    if x > x_max:
        return x_min
    elif x < x_min:
        return x_max
    else:
        return x
 
 
def stay(x, x_max, x_min):
    if x > x_max:
        return x_max
    elif x < x_min:
        return x_min
    else:
        return x
 
 
# Initialize keymap.
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
controls = [[pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s],
            [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]]
# controls[PLAYER][DIRECTION] is the key that PLAYER uses to move into DIRECTION.
OFFSET = 10
X_MIN = [0, 3 * W // 4 + OFFSET - 2]
X_MAX = [W // 4 - OFFSET, W - OFFSET - 2]
 
keymap = dict()
keys = controls[0] + controls[1]
for k in keys: keymap[k] = False
 
 
def collide(rect1, rect2):
    # rect = (left, top, width, height)
    return all([rect2[d] <= rect1[d] <= rect2[d] + rect2[d + 2] or rect2[d] <= rect1[d] + rect1[d + 2] <= rect2[d] +
                rect2[d + 2] for d in [0, 1]])
 
 
def goback(dir, p):
    if p == 1:
        ball_x = boardx[p] - 10
        screen.fill((0, 0, 200))
    else:
        ball_x = boardx[p] + 10
        screen.fill((200, 0, 0))
    dir *= -1
#    sndTick.play()
    return dir
 
 
while running:
    screen.fill((0, 0, 0))
    dt = clock.tick(FPS) / 1000.
    t += dt
    cur_fps = 1. / dt
 
    # if t > 5:
    #    t = 0
    #    ball_speed *= 1.1
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keymap[event.key] = True
        elif event.type == pygame.KEYUP:
            keymap[event.key] = False
 
    for p in [0, 1]:
        for dir in [0, 1, 2, 3]:
            if keymap[controls[p][dir]]:
                if dir == LEFT: boardx[p] = stay(boardx[p] - INC, X_MAX[p], X_MIN[p])
                if dir == RIGHT: boardx[p] = stay(boardx[p] + INC, X_MAX[p], X_MIN[p])
                if dir == UP: boardy[p] = stay(boardy[p] - INC, H - INC + -30, 0)
                if dir == DOWN: boardy[p] = stay(boardy[p] + INC, H - INC - 30, 0)
 
    scorePlayer = -1
    if ball_x > W - 10:
        scorePlayer = 0
    elif ball_x < 0:
        scorePlayer = 1
 
    if scorePlayer >= 0:
        ball_x = W / 2
        ball_dir = randomDir()
        ball_speed = min(200, ball_speed * 1.1)
        score[scorePlayer] += 1
#        sndScore.play()
 
    if ball_y > H - 10:
        downbally = True
    elif ball_y < 0:
        downbally = False
    if downbally:
        ball_y -= ball_dir[1] * ball_speed * dt
    else:
        ball_y += ball_dir[1] * ball_speed * dt
 
    ball_x += ball_dir[0] * ball_speed * dt
 
    '''collision = [False]*2
    for p in [0,1]:
        if ball_y>boardy[p] and boardy[p]+12>ball_y+10:
            if ball_x>boardx[p] and boardx[p]+40>ball_x+10 or boardx[p]<ball_x+10 and ball_x+10<boardx[p]+40:
                collision[p] = True
    '''
    collision = [False] * 2
 
    if ball_x < W / 2 + 20 and ball_x > W / 2 - 20:
        hit = False
 
    if not hit:
        for p in [0, 1]:
            collision[p] = collide((ball_x, ball_y, ball.get_width(), ball.get_height()),
                                   (boardx[p], boardy[p], board[p].get_width(), board[p].get_height()))
            if collision[p]:
                hit = True
                ball_dir[0] = goback(ball_dir[0], p)
 
    for p in [0, 1]:
        screen.blit(board[p], (boardx[p], boardy[p]))
    screen.blit(linex, (3 * W // 4 + OFFSET - 12, 0))
    screen.blit(liney, (W // 4 - OFFSET + 12, 0))
    screen.blit(ball, (int(ball_x), int(ball_y)))
 
    screen.blit(font.render("FPS: %.2f" % cur_fps, False, (127, 127, 127)), (10, H - 30))
    for p in [0, 1]:
        screen.blit(scoreFont.render("%d" % score[p], False, (230 * (1 - p), 0, 230 * p)),
                    (10 * (1 - p) + (W - 20) * p, 10))
 
    pygame.display.update()
 
pygame.quit()