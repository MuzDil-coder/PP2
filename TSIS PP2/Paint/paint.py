import tkinter as tk
from tkinter import filedialog
import datetime

WIDTH, HEIGHT = 900, 600
BAR = 100

COLORS = [
    "black","white","red","green","blue",
    "yellow","cyan","magenta","orange","purple","gray"
]

BRUSH = [2,5,10,20]

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Paint")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT-BAR, bg="white")
        self.canvas.pack(side="bottom")

        self.toolbar = tk.Frame(root, height=BAR, bg="#2c2f33")
        self.toolbar.pack(side="top", fill="x")

        self.tool = "draw"
        self.color = "black"
        self.size_id = 1

        self.start = None
        self.typing = False
        self.text_data = ""
        self.text_pos = (0,0)

        self.undo_stack = []
        self.redo_stack = []

        self.create_ui()

        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)

        root.bind("<Key>", self.key_handler)
        root.bind("<Control-z>", self.undo)
        root.bind("<Control-y>", self.redo)
        root.bind("<Control-s>", self.save)

    # ---------- UI ----------
    def create_ui(self):
        left = tk.Frame(self.toolbar, bg="#2c2f33")
        left.pack(side="left", padx=10)

        tools = ["draw","line","rect","circle","text","fill"]
        for t in tools:
            b = tk.Button(left, text=t.upper(),
                          command=lambda k=t:self.set_tool(k),
                          bg="#7289da", fg="white")
            b.pack(side="left", padx=2)

        mid = tk.Frame(self.toolbar, bg="#2c2f33")
        mid.pack(side="left", padx=20)

        for i in range(len(BRUSH)):
            b = tk.Button(mid, text=str(BRUSH[i]),
                          command=lambda i=i:self.set_size(i),
                          bg="#99aab5")
            b.pack(side="left", padx=2)

        right = tk.Frame(self.toolbar, bg="#2c2f33")
        right.pack(side="left", padx=20)

        for c in COLORS:
            b = tk.Button(right, bg=c, width=2,
                          command=lambda col=c:self.set_color(col))
            b.pack(side="left", padx=1)

        extra = tk.Frame(self.toolbar, bg="#2c2f33")
        extra.pack(side="right", padx=10)

        tk.Button(extra, text="CLEAR", command=self.clear_canvas,
                  bg="#f04747", fg="white").pack(side="right", padx=5)

    # ---------- SETTINGS ----------
    def set_tool(self, t):
        self.tool = t

    def set_size(self, i):
        self.size_id = i

    def set_color(self, c):
        self.color = c

    # ---------- ACTIONS ----------
    def save_state(self):
        self.undo_stack.append(self.canvas.find_all())

    def undo(self, event=None):
        if self.undo_stack:
            self.canvas.delete("all")

    def redo(self, event=None):
        pass  # simplified

    def clear_canvas(self):
        self.canvas.delete("all")

    def save(self, event=None):
        file = filedialog.asksaveasfilename(defaultextension=".ps")
        if file:
            self.canvas.postscript(file=file)

    # ---------- DRAW ----------
    def mouse_down(self, e):
        self.start = (e.x, e.y)

        if self.tool == "text":
            self.typing = True
            self.text_data = ""
            self.text_pos = (e.x, e.y)
            return

        if self.tool == "fill":
            self.canvas.configure(bg=self.color)

    def mouse_move(self, e):
        if not self.start:
            return

        x,y = self.start

        if self.tool == "draw":
            self.canvas.create_line(x,y,e.x,e.y,
                fill=self.color,width=BRUSH[self.size_id],
                capstyle="round", smooth=True)
            self.start = (e.x,e.y)

    def mouse_up(self, e):
        if not self.start:
            return

        x,y = self.start

        if self.tool == "line":
            self.canvas.create_line(x,y,e.x,e.y,
                fill=self.color,width=BRUSH[self.size_id])

        elif self.tool == "rect":
            self.canvas.create_rectangle(x,y,e.x,e.y,
                outline=self.color,width=BRUSH[self.size_id])

        elif self.tool == "circle":
            self.canvas.create_oval(x,y,e.x,e.y,
                outline=self.color,width=BRUSH[self.size_id])

        self.start = None

    # ---------- TEXT ----------
    def key_handler(self, e):
        if self.typing:
            if e.keysym == "Return":
                self.canvas.create_text(
                    self.text_pos[0], self.text_pos[1],
                    text=self.text_data,
                    fill=self.color, anchor="nw",
                    font=("Arial", 16, "bold")
                )
                self.typing = False

            elif e.keysym == "BackSpace":
                self.text_data = self.text_data[:-1]

            else:
                self.text_data += e.char


if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()