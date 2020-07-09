import tkinter as tk
from tkinter import messagebox

N = 3

class TicTacToe(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.your_turn = messagebox.askyesno('turn', 'you put first?')
        self.turn = True
        self.state = [0] * (N * N)
        self.buttons = []
        for i in range(N * N):
            button = tk.Button(
                self, text=str(i), command=self.change_text(i))
            button.grid(column=i%N, row=i//N)
            self.buttons.append(button)
        if self.turn != self.your_turn:
            self.cpu_turn()

    def change_text(self, i):
        def function():
            if self.your_turn != self.turn:
                messagebox.showinfo('attension', 'It is not your turn.')
            elif self.buttons[i]["text"] in ["X", "O"]:
                messagebox.showinfo('attension', 'here cannot be put.')
            else:
                self.buttons[i]["text"] = "O"
                self.state[i] = 2
                judgement = self.judge()
                if judgement == 2:
                    messagebox.showinfo('info', 'You Win')
                    self.master.destroy()
                    return
                elif judgement == 0:
                    messagebox.showinfo('info', 'Draw')
                    self.master.destroy()
                    return
                self.turn = not self.turn
                self.cpu_turn()
        return function

    def judge(self, state=None):
        if state is None:
            state = self.state
        for i in range(N):
            mark = state[i]
            if mark != 0:
                for j in range(i+N, N*N, N):
                    if mark != state[j]:
                        break
                else:
                    return mark
            mark = state[N*i]
            if mark != 0:
                for j in range(N*i+1, N*i+N):
                    if mark != state[j]:
                        break
                else:
                    return mark
        mark = state[0]
        if mark != 0:
            for j in range(N+1, N*N, N+1):
                if mark != state[j]:
                    break
            else:
                return mark
        mark = state[N-1]
        if mark != 0:
            for j in range(N*2-2, N*N-1, N-1):
                if mark != state[j]:
                    break
            else:
                return mark
        if 0 in state:
            return -1
        return 0

    def max_method(self, state, alpha=-1, beta=1):
        judgement = self.judge(state)
        if judgement == 0:
            return None, 0
        if judgement == 1:
            return None, 1
        if judgement == 2:
            return None, -1
        argmax = None
        for i in range(N*N):
            if state[i] == 0:
                next_state = state[:]
                next_state[i] = 1
                argtmp, tmp = self.min_method(next_state, alpha, beta)
                if tmp > alpha:
                    alpha = tmp
                    argmax = i
                    if alpha >= beta:
                        break
        return argmax, alpha

    def min_method(self, state, alpha=-1, beta=1):
        judgement = self.judge(state)
        if judgement == 0:
            return None, 0
        if judgement == 1:
            return None, 1
        if judgement == 2:
            return None, -1
        argmin = None
        for i in range(N*N):
            if state[i] == 0:
                next_state = state[:]
                next_state[i] = 2
                argtmp, tmp = self.max_method(next_state, alpha, beta)
                if tmp < beta:
                    beta = tmp
                    argmin = argtmp
                    if alpha >= beta:
                        break
        return argmin, beta

    def cpu_turn(self):
        argmax, value = self.max_method(self.state)
        self.buttons[argmax]["text"] = "X"
        self.state[argmax] = 1
        judgement = self.judge()
        if judgement == 1:
            messagebox.showinfo('info', 'You Lose')
            self.master.destroy()
        elif judgement == 0:
            messagebox.showinfo('info', 'Draw')
            self.master.destroy()
        self.turn = not self.turn


def main():
    root = tk.Tk()
    app = TicTacToe(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()
