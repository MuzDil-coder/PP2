import tkinter as tk
import random
import json

WIDTH, HEIGHT = 720, 480
CELL = 20

# ---------- SETTINGS ----------
def load_settings():
    try:
        return json.load(open("settings.json"))
    except:
        return {"color":"green","grid":True}

def save_settings(s):
    json.dump(s, open("settings.json","w"))

settings = load_settings()

# ---------- GAME ----------
class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.score = 0
        self.level = 1
        self.hp = 3

        self.direction = "RIGHT"

        self.snake = [[100,100],[80,100],[60,100]]
        self.food = self.spawn()

        self.power = None
        self.power_pos = None

        root.bind("<Key>", self.key)

        self.update()

    def spawn(self):
        return [random.randrange(0,WIDTH,CELL),
                random.randrange(0,HEIGHT,CELL)]

    def key(self,e):
        d = e.keysym
        if d=="Up": self.direction="UP"
        if d=="Down": self.direction="DOWN"
        if d=="Left": self.direction="LEFT"
        if d=="Right": self.direction="RIGHT"

    def move(self):
        head = self.snake[0].copy()

        if self.direction=="UP": head[1]-=CELL
        if self.direction=="DOWN": head[1]+=CELL
        if self.direction=="LEFT": head[0]-=CELL
        if self.direction=="RIGHT": head[0]+=CELL

        self.snake.insert(0, head)

        if head == self.food:
            self.score += 10
            self.food = self.spawn()
        else:
            self.snake.pop()

    def collisions(self):
        head = self.snake[0]

        if head[0]<0 or head[0]>=WIDTH or head[1]<0 or head[1]>=HEIGHT:
            self.hp -= 1
            return

        if head in self.snake[1:]:
            self.hp -= 1

    def draw(self):
        self.canvas.delete("all")

        if settings["grid"]:
            for x in range(0,WIDTH,CELL):
                self.canvas.create_line(x,0,x,HEIGHT, fill="#222")
            for y in range(0,HEIGHT,CELL):
                self.canvas.create_line(0,y,WIDTH,y, fill="#222")

        # snake
        for x,y in self.snake:
            self.canvas.create_rectangle(x,y,x+CELL,y+CELL, fill=settings["color"])

        # food
        fx,fy = self.food
        self.canvas.create_oval(fx,fy,fx+CELL,fy+CELL, fill="white")

        # UI
        self.canvas.create_text(60,10, text=f"Score: {self.score}", fill="white")
        self.canvas.create_text(60,30, text=f"HP: {self.hp}", fill="red")
        self.canvas.create_text(650,10, text=f"Level: {self.level}", fill="yellow")

    def update(self):
        if self.hp <= 0:
            self.canvas.create_text(360,240,text="GAME OVER",fill="red",font=("Arial",30))
            return

        self.move()
        self.collisions()

        if self.score >= self.level*50:
            self.level += 1

        self.draw()
        self.root.after(120, self.update)


# ---------- MENU ----------
def main_menu(root):
    menu = tk.Frame(root, bg="black")
    menu.pack(fill="both", expand=True)

    def start():
        menu.destroy()
        SnakeGame(root)

    def toggle_grid():
        settings["grid"] = not settings["grid"]

    tk.Label(menu, text="SNAKE X", fg="white", bg="black", font=("Arial",30)).pack(pady=40)

    tk.Button(menu, text="Play", command=start).pack(pady=10)
    tk.Button(menu, text="Toggle Grid", command=toggle_grid).pack(pady=10)
    tk.Button(menu, text="Quit", command=root.quit).pack(pady=10)


# ---------- RUN ----------
root = tk.Tk()
root.title("Snake Tkinter")

main_menu(root)

root.mainloop()