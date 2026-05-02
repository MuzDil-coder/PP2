import tkinter as tk
import random

WIDTH, HEIGHT = 800, 600

PLAYER_SPEED = 10
ENEMY_SPEED = 6
COIN_SPEED = 5

class Racer:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Racer X")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#111")
        self.canvas.pack()

        # ---------- IMAGES ----------
        self.player_img = tk.PhotoImage(file="yellowcar.png")
        self.enemy_img = tk.PhotoImage(file="redcar.png")

        # Player (image)
        self.player = self.canvas.create_image(400, 500, image=self.player_img)

        self.enemies = []
        self.coins = []

        self.score = 0
        self.hp = 3
        self.speed_boost = False

        self.label = tk.Label(root, text="Score: 0 | HP: 3", font=("Arial",14))
        self.label.pack()

        # Controls
        root.bind("<Left>", self.move_left)
        root.bind("<Right>", self.move_right)
        root.bind("<Up>", self.move_up)
        root.bind("<Down>", self.move_down)
        root.bind("<space>", self.activate_boost)

        self.spawn()
        self.update()

    # -------- Movement --------
    def move_left(self,e):
        self.canvas.move(self.player,-PLAYER_SPEED,0)

    def move_right(self,e):
        self.canvas.move(self.player, PLAYER_SPEED,0)

    def move_up(self,e):
        self.canvas.move(self.player,0,-PLAYER_SPEED)

    def move_down(self,e):
        self.canvas.move(self.player,0, PLAYER_SPEED)

    # -------- Boost --------
    def activate_boost(self,e):
        self.speed_boost = True
        self.root.after(2000, self.stop_boost)

    def stop_boost(self):
        self.speed_boost = False

    # -------- Spawn --------
    def spawn(self):
        if random.random() < 0.05:
            x = random.randint(100,700)
            e = self.canvas.create_image(x, 0, image=self.enemy_img)
            self.enemies.append(e)

        self.root.after(200, self.spawn)

    # -------- Update --------
    def update(self):
        speed = ENEMY_SPEED * (2 if self.speed_boost else 1)

        # Move enemies
        for e in self.enemies[:]:
            self.canvas.move(e, 0, speed)

            if self.collision(self.player, e):
                self.canvas.delete(e)
                self.enemies.remove(e)
                self.hp -= 1

        self.label.config(text=f"Score: {self.score} | HP: {self.hp}")

        # Game over
        if self.hp <= 0:
            self.canvas.create_text(400,300, text="GAME OVER",
                                    fill="white", font=("Arial",30))
            return

        self.root.after(30, self.update)

    # -------- Collision --------
    def collision(self, a, b):
        ax1, ay1, ax2, ay2 = self.canvas.bbox(a)
        bx1, by1, bx2, by2 = self.canvas.bbox(b)

        return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)


if __name__ == "__main__":
    root = tk.Tk()
    game = Racer(root)
    root.mainloop()