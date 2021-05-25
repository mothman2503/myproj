from tkinter import *
import sudoku
import tkinter.font as TkFont

root = Tk()

#defining colors

colors = {'bgnd' : '#FFFFFF', 'bold_lines' : '#999999'}

print(TkFont.families())

board = Canvas(root, width = 364, height = 364, bd = 0, bg = colors['bgnd'])
board.grid(row = 0, column = 0, columnspan = 10, padx = 40, pady = 40)

g = sudoku.game()


#printing the board

def pC():
	row = g.currow
	col = g.curcol

	board.create_rectangle(col * 40 + 2, row * 40 + 2, (col+1) * 40 + 2, (row+1) * 40 + 2, fill = '#FFFF77')

def pB():

	for i in range(3):
		board.create_line(0, 120 * i + 2, 364, 120 * i + 2, fill = colors['bold_lines'], width = 3)
		board.create_line(120 * i + 2, 364, 120 * i + 2, 0, fill = colors['bold_lines'], width = 3)

	for i in range(9):
		board.create_line(0, 40 * i + 2, 364, 40 * i + 2, fill = colors['bold_lines'], width = 1)
		board.create_line(40 * i + 2, 364, 40 * i + 2, 0, fill = colors['bold_lines'], width = 1)

	board.create_rectangle(4,4,364,364, width = 3)

def pS():
	f = 0
	for row in range(9):
		for col in range(9):
			helv36 = TkFont.Font(family= TkFont.families()[f], size=28, weight='bold')
			board.create_text(40 * col + 23, 40 * row + 23, text= g.disp_col(row, col)["num"], fill = g.disp_col(row, col)["color"], font = helv36)
			fontnum = TkFont.Font(family= TkFont.families()[f], size=10, weight='bold')
			board.create_text(40 * col + 33, 40 * row + 33, text= str(f), fill = g.disp_col(row, col)["color"], font = fontnum)
			f += 1

pC()
pB()

g.newgame("easy")
g.solve()
pS()

for i in range(9):
	print(g.disp_col(0, i))


print("\n\ndone.....\n\n\n")

root.geometry("445x600")
root.resizable(width = False, height = False)
root.mainloop()