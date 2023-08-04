import json
from math import sqrt
from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import askinteger
from tkinter import messagebox as mb
from path import find_path

CHOSEN = None
PATH = None
POINTS = []
root = Tk()

canvas = Canvas(width=700, height=700, bg='white')
canvas.pack()


def create_circle(x, y, n, r=10, outline='black', fill=None, width=1):
    return canvas.create_oval(x - r, y - r, x + r, y + r, outline=outline, fill=fill, width=width, tags=f'circ {n}')


def make_connection(v1, v2, l_new):
    exist = False
    for i, (v, l) in enumerate(data[v1][2]):
        if v == v2:
            exist = True
            answer = mb.askyesno(title="Путь уже существует", message=f"Заменить {l} на {l_new}?")
            if answer:
                data[v1][2][i][1] = l_new
                for j, (vj, _) in enumerate(data[v2][2]):
                    if vj == v1:
                        data[v2][2][j][1] = l_new
    if not exist:
        data[v1][2].append([v2, l_new])
        data[v2][2].append([v1, l_new])


def build_path(path):
    prev = -1
    for i in path:
        if prev != -1:
            draw_connect(prev, i, path=True)
        prev = i


def choose(event, obj):
    global CHOSEN, data, PATH

    if mode.get() == 'connect':
        tags = canvas.gettags("current")
        if tags[0] == 'circ':
            if CHOSEN is None:
                CHOSEN = int(tags[1])
            else:
                NEW = int(tags[1])
                if autolen.get():
                    p1, p2 = data[CHOSEN], data[NEW]
                    x1, y1, _ = p1
                    x2, y2, _ = p2
                    l = int(sqrt((x1 - x2)**2 + (y1 - y2)**2))
                else:
                    l = askinteger('', 'Введите расстояние', initialvalue=100)
                make_connection(CHOSEN, NEW, l)

                CHOSEN = None

    if mode.get() == 'path':
        tags = canvas.gettags("current")
        if tags[0] == 'circ':
            if CHOSEN is None:
                CHOSEN = int(tags[1])
            else:
                NEW = int(tags[1])
                PATH, dist = find_path(data, CHOSEN, NEW)

                CHOSEN = None



def mouse_click(event):
    global data
    x, y = event.x, event.y
    if mode.get() == 'create':
        items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if len(items) == 0:
            data.append([x, y, []])
    update()


def mouse_cancel(event):
    global CHOSEN, PATH
    CHOSEN = None
    PATH = None
    update()


data = []
# with open('data.json', 'r') as data_file:
#     data = json.load(data_file)

print(data)


def draw_point(x, y, n=None):
    fig = create_circle(x, y, n, fill='red')
    text = canvas.create_text(x, y, text=n, tags=f'circ {n}')
    canvas.tag_bind(fig, "<Button-1>", lambda event: choose(event, fig))
    canvas.tag_bind(text, "<Button-1>", lambda event: choose(event, fig))
    return fig, text


def draw_connect(i, j, l=None, path=False):
    p1, p2 = data[i], data[j]
    x1, y1, _ = p1
    x2, y2, _ = p2
    if path:
        canvas.create_line(x1, y1, x2, y2, fill='lime', width=3)
    else:
        canvas.create_line(x1, y1, x2, y2, width=2)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=l)

def update():
    global PATH
    canvas.delete('all')
    points = []
    for i, (x, y, connects) in enumerate(data):
        points += draw_point(x, y, i)
        for j, l in connects:
            if i < j:
                draw_connect(i, j, l)

    if CHOSEN is not None:
        x, y, _ = data[CHOSEN]
        create_circle(x, y, None, r=16, outline='green', width=3)
    if PATH is not None:
        build_path(PATH)

    for p in points:
        canvas.tag_raise(p)




mode = StringVar(value='create')

create_btn = ttk.Radiobutton(text='create', value='create', variable=mode)
create_btn.pack()

connect_btn = ttk.Radiobutton(text='connect', value='connect', variable=mode)
connect_btn.pack()

autolen = BooleanVar()
autolen_cbtn = ttk.Checkbutton(text="Считать расстояния", variable=autolen)
autolen_cbtn.pack()

path_btn = ttk.Radiobutton(text='path', value='path', variable=mode)
path_btn.pack()

canvas.bind("<Button-1>", mouse_click)
canvas.bind("<Button-3>", mouse_cancel)


def save():
    with open('data_tmp.json', 'w') as data_file:
        json.dump(data, data_file)


save_btn = Button(text='save', command=save)
save_btn.pack()
update()
root.mainloop()
