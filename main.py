import tkinter as tk
import tkinter.messagebox as mb
import time
import random
import copy
import sys

root = tk.Tk()
root.title('Game board')
root.geometry('360x330')
root.resizable(width=False, height=False)
root.iconphoto(True, tk.PhotoImage(file='./icon.ico'))
root.withdraw()

welcome_window = tk.Tk()
welcome_window.resizable(width=False, height=False)
welcome_window.geometry('300x280')
welcome_window.title('Welcome to 2048 game')

color_dict = {0: 'lightgrey', 2: '#fdff9e', 4: '#fcff6d', 8: '#f9ff07', 16: '#ffd800',
              32: '#ffc300', 64: '#ffa100', 128: '#ff9400',
              256: '#ff6600', 512: '#ff4800', 1024: '#ff2600',
              2048: '#b71b00', 4096: '#c24efc', 8192: '#5b79ff'}

score_dict = {0: 0, 2: 0, 4: 1, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 256: 8, 512: 9, 1024: 10, 2048: 11,
              4096: 12, 8192: 13}
score = tk.StringVar()


def display():
    global board
    for i in range(len(board)):
        for j in range(len(board[0])):
            lb = tk.Label(root, text='' if board[i][j] == 0 else board[i][j],
                          bg=color_dict[board[i][j]],
                          width=7, height=3)
            lb.place(x=64 * (j + 1), y=64 * (i + 1), anchor='nw')


def available_dot():
    global board
    game_board = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                game_board.append([i, j])
    return game_board


def spawn_dot(number):
    global board
    sample = random.sample(available_dot(), number)
    for i in range(number):
        x, y = sample[i]
        generate_num = random.randint(1, 4)
        if generate_num == 4:
            board[x][y] = 4
        else:
            board[x][y] = 2


def can_move():
    global board
    for i in range(1, len(board) - 1):
        for j in range(1, len(board[0]) - 1):
            if board[i][j] == board[i - 1][j] or \
                    board[i][j] == board[i + 1][j] or \
                    board[i][j] == board[i][j - 1] or \
                    board[i][j] == board[i][j + 1]:
                return True
    if board[0][0] == board[0][1] or board[0][0] == board[1][0]:
        return True
    if board[3][0] == board[3][1] or board[3][0] == board[2][0]:
        return True
    if board[0][3] == board[1][3] or board[0][3] == board[0][2]:
        return True
    if board[3][3] == board[3][2] or board[3][3] == board[2][3]:
        return True
    if board[1][0] == board[2][0] or board[0][1] == board[0][2] or \
            board[3][1] == board[3][2] or board[3][1] == board[3][2]:
        return True
    return False


def left_arrow(event):
    global board
    last_board = copy.deepcopy(board)
    for i in range(len(board)):
        temp = []
        for j in range(len(board[0])):
            if board[i][j] != 0:
                temp.append(board[i][j])
            if board[i][j] == 2048:
                mb.showinfo(title='Game over', message='Score：%s\n You are winner' % score.get())
                time.sleep(0.1)
                new_game()
                return
        for k in range(len(temp) - 1):
            if temp[k] != 0 and temp[k] == temp[k + 1]:
                temp[k] *= 2
                get_score(temp[k])
                temp = temp[:k + 1] + temp[k + 2:] + [0]
        temp += [0] * (4 - len(temp))
        board[i] = temp
    if last_board != board:
        spawn_dot(1)
        display()
    elif not available_dot():
        if not can_move():
            mb.showinfo(title='Game over', message='Score：%s\n You lose' % score.get())
            time.sleep(0.1)
            new_game()


def right_arrow(event):
    global board
    last_board = copy.deepcopy(board)
    for i in range(len(board)):
        temp = []
        for j in range(len(board[0])):
            if board[i][j] != 0:
                temp.append(board[i][j])
            if board[i][j] == 2048:
                mb.showinfo(title='Game over', message='Score：%s\n You are winner' % score.get())
                time.sleep(0.1)
                new_game()
                return
        for k in range(len(temp) - 1, 0, -1):
            if temp[k] != 0 and temp[k] == temp[k - 1]:
                temp[k] *= 2
                get_score(temp[k])
                temp = [0] + temp[:k - 1] + temp[k:]
        temp = [0] * (4 - len(temp)) + temp
        board[i] = temp
    if last_board != board:
        spawn_dot(1)
        display()
    elif not available_dot():
        if not can_move():
            mb.showinfo(title='Game over', message='Score：%s\n You lose' % score.get())
            time.sleep(0.1)
            new_game()


def up_arrow(event):
    global board
    last_board = copy.deepcopy(board)
    for j in range(len(board)):
        temp = []
        for i in range(len(board[0])):
            if board[i][j] != 0:
                temp.append(board[i][j])
            if board[i][j] == 2048:
                mb.showinfo(title='Game over', message='Score：%s\n You are winner' % score.get())
                time.sleep(0.1)
                new_game()
                return
        for k in range(len(temp) - 1):
            if temp[k] != 0 and temp[k] == temp[k + 1]:
                temp[k] *= 2
                get_score(temp[k])
                temp = temp[:k + 1] + temp[k + 2:] + [0]
        temp += [0] * (4 - len(temp))
        for i in range(4):
            board[i][j] = temp[i]

    if last_board != board:
        spawn_dot(1)
        display()
    elif not available_dot():
        if not can_move():
            mb.showinfo(title='Game over', message='Score：%s\n You lose' % score.get())
            time.sleep(0.1)
            new_game()


def down_arrow(event):
    global board
    last_board = copy.deepcopy(board)
    for j in range(len(board)):
        temp = []
        for i in range(len(board[0])):
            if board[i][j] != 0:
                temp.append(board[i][j])
            if board[i][j] == 2048:
                mb.showinfo(title='Game over', message='Score：%s\n You are winner' % score.get())
                time.sleep(0.1)
                new_game()
                return
        for k in range(len(temp) - 1, 0, -1):
            if temp[k] != 0 and temp[k] == temp[k - 1]:
                temp[k] *= 2
                get_score(temp[k])
                temp = [0] + temp[:k - 1] + temp[k:]
        temp = [0] * (4 - len(temp)) + temp
        for i in range(4):
            board[i][j] = temp[i]
    if last_board != board:
        spawn_dot(1)
        display()
    elif not available_dot():
        if not can_move():
            mb.showinfo(title='Game over', message='Score：%s\n You lose' % score.get())
            time.sleep(0.1)
            new_game()


def start_menu():
    global welcome_window
    global root
    welcome_window.destroy()
    root.deiconify()


def end_game(event):
    print('Thank you for playing!')
    sys.exit()


def new_game():
    global board
    board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    spawn_dot(2)
    display()
    score.set(0)


def get_score(number):
    global score_dict
    now_score = int(score.get())
    now_score += score_dict[number]
    score.set(str(now_score))


board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
spawn_dot(2)
display()
score.set(0)

board_lb = tk.Label(root)
board_lb.place(x=300, y=200, anchor='nw')
board_lb.focus_set()
board_lb.bind('<Escape>', end_game)
board_lb.bind('<Left>', left_arrow)
board_lb.bind('<Right>', right_arrow)
board_lb.bind('<Up>', up_arrow)
board_lb.bind('<Down>', down_arrow)

score_word = tk.Label(root, text='Score', width=5, height=1, bg='darkgrey', font='Corbel')
score_word.place(x=180, y=2, anchor='nw')
score_num = tk.Label(root, textvariable=score, width=8, height=1, bg='darkgrey', font='Corbel')
score_num.place(x=225, y=2, anchor='nw')

name_game = tk.Label(root, text='2048', width=4, height=1, font='Corbel 30', bg='darkgrey')
name_game.place(x=75, y=5, anchor='nw')

restart_btn = tk.Button(root, text='Restart', bg='darkgrey', width=13, height=1,
                        command=new_game, font='Corbel')
restart_btn.place(x=178, y=28, anchor='nw')

rule_word = tk.Label(welcome_window, text='To only rule of the game is that you have to\n'
                                          'merge 2 tiles with the same numerical value\n'
                                          'and then they become 1 tile with x2 of their\n'
                                          'original value then you have to merge this\n'
                                          'new x2 tile with another x2\n'
                                          'tile until you reach 2048.\n\n\n\n'
                                          'To control use arrows\n'
                                          'To escape press  <Escape>', font='Corbel')
rule_word.place(x=2, y=2)
welcome_btn = tk.Button(welcome_window, text='Start game', command=start_menu, font='Corbel', bg='darkgrey')
welcome_btn.place(x=150, y=250, anchor='center')

root.mainloop()
