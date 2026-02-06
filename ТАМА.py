import tkinter as tk
from tkinter import ttk, simpledialog
import time

class Tamagotchi:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.age = 0
        self.birth_time = time.time()
        self.last_update = time.time()
        self.alive = True
        self.death_reason = ""
        self.stats = {"hunger": 70, "thirst": 70, "energy": 80, "happiness": 75, "hygiene": 85}

    def update(self):
        if not self.alive:
            return False
        elapsed = time.time() - self.last_update
        if elapsed < 1:
            return True
        self.last_update = time.time()
        self.age = int((time.time() - self.birth_time) / 60)
        rates = {"hunger": 0.22, "thirst": 0.3, "energy": 0.12, "happiness": 0.08, "hygiene": 0.15}
        for stat, rate in rates.items():
            self.stats[stat] -= elapsed * rate
            if self.stats[stat] <= 0 and stat in ["hunger", "thirst", "energy", "happiness"]:
                self.alive = False
                self.death_reason = \
                {"hunger": "голода", "thirst": "жажды", "energy": "усталости", "happiness": "скуки"}[stat]
                return False
        for key in self.stats:
            self.stats[key] = max(0, min(100, self.stats[key]))
        return True

    def feed(self): self.stats["hunger"] = min(100, self.stats["hunger"] + 35)
    def drink(self): self.stats["thirst"] = min(100, self.stats["thirst"] + 40)
    def play(self):
        self.stats["happiness"] = min(100, self.stats["happiness"] + 30)
        self.stats["energy"] = max(0, self.stats["energy"] - 15)
    def sleep(self): self.stats["energy"] = min(100, self.stats["energy"] + 45)
    def wash(self): self.stats["hygiene"] = min(100, self.stats["hygiene"] + 50)

    def get_mood(self):
        h = self.stats["happiness"]
        return "😄" if h >= 85 else "😊" if h >= 65 else "😐" if h >= 40 else "😢" if h >= 20 else "😭"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тамагочи")
        self.geometry("400x450")
        self.configure(bg="#2b2b2b")
        self.pet = None
        self.start_screen()

    def start_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="ТАМАГОЧИ", font=("Arial", 28, "bold"), fg="#4A90E2", bg="#2b2b2b").pack(pady=30)
        for text, species in [("🐱 Кошка", "кошка"), ("🐶 Собака", "собака"), ("🦜 Попугай", "попугай")]:
            tk.Button(self, text=text, command=lambda sp=species: self.new_pet(sp),
                      bg="#3a3a3a", fg="white", width=25, height=2, font=("Arial", 11, "bold"),
                      activebackground="#4a4a4a", bd=0).pack(pady=8)

    def new_pet(self, species):
        name = simpledialog.askstring("Новый питомец", f"Имя {species}?") or f"Мой {species}"
        self.pet = Tamagotchi(name.strip(), species)
        self.game_screen()

    def game_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.name_label = tk.Label(self, font=("Arial", 20, "bold"), fg="white", bg="#2b2b2b")
        self.name_label.pack(pady=10)
        self.age_label = tk.Label(self, font=("Arial", 12), fg="#aaaaaa", bg="#2b2b2b")
        self.age_label.pack()
        self.mood_label = tk.Label(self, font=("Arial", 50), fg="white", bg="#2b2b2b")
        self.mood_label.pack(pady=5)
        self.status_label = tk.Label(self, font=("Arial", 14), fg="#2ecc71", bg="#2b2b2b")
        self.status_label.pack()
        self.bars = {}
        colors = {"hunger": "#e74c3c", "thirst": "#3498db", "energy": "#f39812", "happiness": "#2ecc71",
                  "hygiene": "#9b59b6"}
        labels = {"hunger": "🍗", "thirst": "💧", "energy": "⚡", "happiness": "😊", "hygiene": "🛁"}
        for stat in ["hunger", "thirst", "energy", "happiness", "hygiene"]:
            frame = tk.Frame(self, bg="#2b2b2b")
            frame.pack(fill="x", padx=20, pady=2)
            tk.Label(frame, text=labels[stat], width=3, fg="white", bg="#2b2b2b", font=("Arial", 14)).pack(side="left")
            bar = ttk.Progressbar(frame, length=200, mode='determinate')
            bar.pack(side="left", padx=5)
            val_label = tk.Label(frame, text="70", width=3, fg="white", bg="#2b2b2b", font=("Arial", 10))
            val_label.pack(side="left")
            self.bars[stat] = (bar, val_label)
            style = ttk.Style()
            style.theme_use('default')
            style.configure(f"{stat}.Horizontal.TProgressbar", background=colors[stat], troughcolor="#3a3a3a",
                            borderwidth=0)
            bar.config(style=f"{stat}.Horizontal.TProgressbar")
        btn_frame = tk.Frame(self, bg="#2b2b2b")
        btn_frame.pack(pady=15)
        actions = [
            ("🍗", "#e74c3c", self.feed),
            ("💧", "#3498db", self.drink),
            ("🎮", "#2ecc71", self.play),
            ("😴", "#f39812", self.sleep),
            ("🛁", "#9b59b6", self.wash)
        ]
        for i, (text, color, cmd) in enumerate(actions):
            tk.Button(btn_frame, text=text, width=4, height=2, bg=color, fg="white", font=("Arial", 12, "bold"),
                      command=cmd, bd=0).grid(row=0, column=i, padx=3)
        self.msg_label = tk.Label(self, text="Питомец живёт сам по себе 😊", wraplength=350,
                                  fg="#aaaaaa", bg="#2b2b2b", font=("Arial", 11))
        self.msg_label.pack(pady=15)
        tk.Button(self, text="🚪 Выйти", command=self.start_screen, bg="#e74c3c", fg="white",
                  width=12, height=1, font=("Arial", 11, "bold"), bd=0,
                  activebackground="#c0392b").pack(pady=10)
        self.game_loop()

    def feed(self):
        if self.pet.alive:
            self.pet.feed()
            self.msg_label.config(text=f"🍗 {self.pet.name} поел!", fg="#2ecc71")
            self.update_ui()
    def drink(self):
        if self.pet.alive:
            self.pet.drink()
            self.msg_label.config(text=f"💧 {self.pet.name} попил!", fg="#3498db")
            self.update_ui()
    def play(self):
        if self.pet.alive:
            self.pet.play()
            self.msg_label.config(text=f"🎮 {self.pet.name} играл с тобой!", fg="#2ecc71")
            self.update_ui()
    def sleep(self):
        if self.pet.alive:
            self.pet.sleep()
            self.msg_label.config(text=f"😴 {self.pet.name} выспался!", fg="#f39812")
            self.update_ui()
    def wash(self):
        if self.pet.alive:
            self.pet.wash()
            self.msg_label.config(text=f"🛁 {self.pet.name} чистый!", fg="#9b59b6")
            self.update_ui()

    def update_ui(self):
        if not self.pet or not self.pet.alive:
            return
        self.name_label.config(text=f"{self.pet.name} • {self.pet.species}")
        self.age_label.config(text=f"Возраст: {self.pet.age} мин")
        self.mood_label.config(text=self.pet.get_mood())
        avg = sum(self.pet.stats.values()) / 5
        status = "Отлично ✨" if avg >= 80 else "Норм 🙂" if avg >= 60 else "Плохо 😐" if avg >= 40 else "Критично ⚠️"
        color = "#2ecc71" if avg >= 80 else "#f39812" if avg >= 60 else "#e67e22" if avg >= 40 else "#e74c3c"
        self.status_label.config(text=f"Статус: {status}", fg=color)
        for stat, (bar, label) in self.bars.items():
            value = self.pet.stats[stat]
            bar['value'] = value
            label.config(text=str(int(value)))
        lows = [k for k, v in self.pet.stats.items() if v < 15]
        if lows:
            warns = {"hunger": "голоден", "thirst": "хочет пить", "energy": "устал", "happiness": "грустит",
                     "hygiene": "грязный"}
            self.msg_label.config(text=f"⚠️ {self.pet.name}: {', '.join([warns[k] for k in lows[:2]])}", fg="#e74c3c")

    def game_loop(self):
        if self.pet and self.pet.update():
            self.update_ui()
            self.after(2000, self.game_loop)
        else:
            self.game_over()

    def game_over(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text=self.pet.name, font=("Arial", 28, "bold"), fg="#e74c3c", bg="#2b2b2b").pack(pady=30)
        tk.Label(self, text=f"🕯️ Умер от {self.pet.death_reason} 🕯️", font=("Arial", 20), fg="white",
                 bg="#2b2b2b").pack(pady=15)
        tk.Label(self, text=f"Прожил: {self.pet.age} мин", font=("Arial", 16), fg="#f39812", bg="#2b2b2b").pack(pady=10)
        tk.Button(self, text="🔄 Новая игра", command=self.start_screen, bg="#2ecc71", fg="white",
                  width=15, height=1, font=("Arial", 11, "bold"), bd=0,
                  activebackground="#27ae60").pack(pady=15)
        tk.Button(self, text="🚪 Выйти", command=self.quit, bg="#e74c3c", fg="white",
                  width=15, height=1, font=("Arial", 11, "bold"), bd=0,
                  activebackground="#c0392b").pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()