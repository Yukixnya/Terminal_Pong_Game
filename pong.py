import curses
import random

# Game board
def draw_border(win, sh, sw):
    win.clear()
    win.border(0)
    for i in range(1, sh - 1):  # drawing center line
        if i % 2 == 0:
            win.addch(i, sw // 2, '|')

def main(stdscr):
    curses.curs_set(0)
    sh, sw = 20, 60
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(1)
    win.timeout(100) # Gamepaly speed

    # Paddles
    p1_y, p2_y = sh // 2, sh // 2
    paddle_size = 3
    
    # Ball
    ball_x, ball_y = sw // 2, sh // 2
    ball_dx, ball_dy = random.choice([-1, 1]), random.choice([-1, 1])
    
    score1, score2 = 0, 0

    while True:
        draw_border(win, sh, sw)
        
        # Draw paddles
        for i in range(paddle_size):
            win.addch(p1_y + i, 2, '#')
            win.addch(p2_y + i, sw - 3, '#')
        
        # Draw ball
        win.addch(ball_y, ball_x, 'O')
        
        # Display score
        win.addstr(0, sw // 4, f'P1: {score1}')
        win.addstr(0, 3 * sw // 4, f'P2: {score2}')
        
        win.refresh()
        key = win.getch()

        # Player 1 controls (W, S)
        if key == ord('w') and p1_y > 1:
            p1_y -= 2
        elif key == ord('s') and p1_y < sh - paddle_size - 1:
            p1_y += 2
        
        # Player 2 controls (Up, Down)
        elif key == curses.KEY_UP and p2_y > 1:
            p2_y -= 2
        elif key == curses.KEY_DOWN and p2_y < sh - paddle_size - 1:
            p2_y += 2
        
        # Ball Movement
        ball_x += ball_dx
        ball_y += ball_dy
        
        # Ball collision (Top and Bottom)
        if ball_y <= 1 or ball_y >= sh - 2:
            ball_dy *= -1
        
        # Ball collision with Paddles
        if ball_x == 3 and p1_y <= ball_y <= p1_y + paddle_size:
            ball_dx *= -1
        elif ball_x == sw - 4 and p2_y <= ball_y <= p2_y + paddle_size:
            ball_dx *= -1
        
        # Score update
        if ball_x <= 1:
            score2 += 1
            ball_x, ball_y = sw // 2, sh // 2
            ball_dx = 1
        elif ball_x >= sw - 1:
            score1 += 1
            ball_x, ball_y = sw // 2, sh // 2
            ball_dx = -1
        
        # Game over
        if score1 == 5 or score2 == 5:
            win.addstr(sh // 2, sw // 2 - 5, f'PLAYER {1 if score1 == 5 else 2} WINS!')
            win.refresh()
            curses.napms(5000)  #Screen Out Time
            break

curses.wrapper(main)
