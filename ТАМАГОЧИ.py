import customtkinter as ctk
from tkinter import simpledialog
import time


class Tamagotchi:
    def __init__(self, name, species):
        self.name, self.species = name, species
        self.age, self.birth_time = 0, time.time()
        self.last_update = time.time()
        self.alive, self.death_reason = True, ""
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
                self.death_reason = {"hunger": "голода", "thirst": "жажды", "energy": "усталости", "happiness": "скуки"}[stat]
                return False
        for k in self.stats:
            self.stats[k] = max(0, min(100, self.stats[k]))
        return True

    def get_mood(self):
        h = self.stats["happiness"]
        return "😄" if h >= 85 else "😊" if h >= 65 else "😐" if h >= 40 else "😢" if h >= 20 else "😭"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("Тамагочи")
        self.geometry("400x480")
        self.pet = None
        self.last_action = 0
        self.cooldown = 2.0
        self.start_screen()

    def start_screen(self):
        for w in self.winfo_children():
            w.destroy()
        ctk.CTkLabel(self, text="Последние минуты", font=("Arial", 28, "bold")).pack(pady=30)
        for text, sp in [("🐱 Кошка", "кошка"), ("🐶 Собака", "собака"), ("🦜 Попугай", "попугай")]:
            ctk.CTkButton(self, text=text, command=lambda s=sp: self.new_pet(s),
                          width=200, height=45, font=("Arial", 12, "bold")).pack(pady=8)

    def new_pet(self, species):
        name = simpledialog.askstring("Новый питомец", f"Имя {species}?") or f"Мой {species}"
        self.pet = Tamagotchi(name.strip(), species)
        self.game_screen()

    def game_screen(self):
        for w in self.winfo_children():
            w.destroy()
        self.name_label = ctk.CTkLabel(self, font=("Arial", 20, "bold"))
        self.name_label.pack(pady=10)
        self.age_label = ctk.CTkLabel(self, font=("Arial", 12), text_color="#aaaaaa")
        self.age_label.pack()
        self.mood_label = ctk.CTkLabel(self, font=("Arial", 50))
        self.mood_label.pack(pady=5)
        self.status_label = ctk.CTkLabel(self, font=("Arial", 14))
        self.status_label.pack()
        self.bars = {}
        colors = {"hunger": "#e74c3c", "thirst": "#3498db", "energy": "#f39812", "happiness": "#2ecc71", "hygiene": "#9b59b6"}
        labels = {"hunger": "🍗", "thirst": "💧", "energy": "⚡", "happiness": "😊", "hygiene": "🛁"}
        for stat in self.stats:
            f = ctk.CTkFrame(self, fg_color="transparent")
            f.pack(fill="x", padx=20, pady=2)
            ctk.CTkLabel(f, text=labels[stat], width=20, font=("Arial", 14)).pack(side="left", padx=(0, 5))
            bar = ctk.CTkProgressBar(f, width=200, height=12)
            bar.pack(side="left", padx=5)
            bar.set(0.7)
            val = ctk.CTkLabel(f, text="70", width=30, font=("Arial", 10))
            val.pack(side="left")
            self.bars[stat] = (bar, val)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15)
        actions = [("🍗", "#e74c3c", self.feed), ("💧", "#3498db", self.water), ("🎮", "#2ecc71", self.play),
                   ("😴", "#f39812", self.sleep), ("🛁", "#9b59b6", self.bathe)]
        for i, (txt, col, cmd) in enumerate(actions):
            ctk.CTkButton(btn_frame, text=txt, width=50, height=45, fg_color=col, hover_color=col,
                          font=("Arial", 14, "bold"), command=cmd).grid(row=0, column=i, padx=3)
        self.msg_label = ctk.CTkLabel(self, text="Питомец живёт сам по себе 😊", wraplength=350,
                                      text_color="#aaaaaa", font=("Arial", 11))
        self.msg_label.pack(pady=15)
        ctk.CTkButton(self, text="🚪 Выйти", command=self.start_screen, fg_color="#e74c3c",
                      hover_color="#c0392b", width=120, height=35, font=("Arial", 11, "bold")).pack(pady=10)
        self.game_loop()

    def update_ui(self):
        if not self.pet or not self.pet.alive:
            return
        self.name_label.configure(text=f"{self.pet.name} • {self.pet.species}")
        self.age_label.configure(text=f"Возраст: {self.pet.age} мин")
        self.mood_label.configure(text=self.pet.get_mood())
        avg = sum(self.pet.stats.values()) / 5
        status = "Отлично ✨" if avg >= 80 else "Норм 🙂" if avg >= 60 else "Плохо 😐" if avg >= 40 else "Критично ⚠️"
        color = "#2ecc71" if avg >= 80 else "#f39812" if avg >= 60 else "#e67e22" if avg >= 40 else "#e74c3c"
        self.status_label.configure(text=f"Статус: {status}", text_color=color)
        for stat, (bar, label) in self.bars.items():
            v = self.pet.stats[stat] / 100
            bar.set(v)
            label.configure(text=str(int(self.pet.stats[stat])))
        lows = [k for k, v in self.pet.stats.items() if v < 15]
        if lows:
            warns = {"hunger": "голоден", "thirst": "хочет пить", "energy": "устал", "happiness": "грустит", "hygiene": "грязный"}
            self.msg_label.configure(text=f"⚠️ {self.pet.name}: {', '.join([warns[k] for k in lows[:2]])}", text_color="#e74c3c")

    def game_loop(self):
        if self.pet and self.pet.update():
            self.update_ui()
            self.after(2000, self.game_loop)
        else:
            self.game_over()

    def game_over(self):
        for w in self.winfo_children():
            w.destroy()
        ctk.CTkLabel(self, text=self.pet.name, font=("Arial", 28, "bold"), text_color="#e74c3c").pack(pady=30)
        ctk.CTkLabel(self, text=f"🕯️ Умер от {self.pet.death_reason} 🕯️", font=("Arial", 20)).pack(pady=15)
        ctk.CTkLabel(self, text=f"Прожил: {self.pet.age} мин", font=("Arial", 16), text_color="#f39812").pack(pady=10)
        ctk.CTkButton(self, text="🔄 Новая игра", command=self.start_screen, fg_color="#2ecc71",
                      hover_color="#27ae60", width=180, height=35, font=("Arial", 11, "bold")).pack(pady=15)
        ctk.CTkButton(self, text="🚪 Выйти", command=self.quit, fg_color="#e74c3c",
                      hover_color="#c0392b", width=180, height=35, font=("Arial", 11, "bold")).pack()

    def _can_act(self):
        if not self.pet or not self.pet.alive or time.time() - self.last_action < self.cooldown:
            if self.pet and self.pet.alive:
                self.msg_label.configure(text="⏳ Подождите немного...", text_color="#f39812")
            return False
        self.last_action = time.time()
        return True

    def feed(self):
        if not self._can_act():
            return
        self.pet.stats["hunger"] = min(100, self.pet.stats["hunger"] + 35)
        self.pet.stats["hygiene"] = max(0, self.pet.stats["hygiene"] - 8)
        self.msg_label.configure(text=f"🍗 {self.pet.name} вкусно поел(а)!", text_color="#2ecc71")
        self.update_ui()

    def water(self):
        if not self._can_act():
            return
        self.pet.stats["thirst"] = min(100, self.pet.stats["thirst"] + 45)
        self.msg_label.configure(text=f"💧 {self.pet.name} утолил(а) жажду!", text_color="#3498db")
        self.update_ui()

    def play(self):
        if not self._can_act() or self.pet.stats["energy"] < 20:
            if self.pet and self.pet.alive and self.pet.stats["energy"] < 20:
                self.msg_label.configure(text=f"😴 {self.pet.name} слишком устал(а) для игр!", text_color="#e74c3c")
            return
        self.pet.stats["happiness"] = min(100, self.pet.stats["happiness"] + 30)
        self.pet.stats["energy"] = max(0, self.pet.stats["energy"] - 20)
        self.pet.stats["hygiene"] = max(0, self.pet.stats["hygiene"] - 12)
        self.msg_label.configure(text=f"🎮 {self.pet.name} весело поиграл(а)!", text_color="#2ecc71")
        self.update_ui()

    def sleep(self):
        if not self._can_act() or self.pet.stats["energy"] > 80:
            if self.pet and self.pet.alive and self.pet.stats["energy"] > 80:
                self.msg_label.configure(text=f"😴 {self.pet.name} ещё не хочет спать!", text_color="#f39812")
            return
        self.pet.stats["energy"] = min(100, self.pet.stats["energy"] + 50)
        self.pet.stats["happiness"] = min(100, self.pet.stats["happiness"] + 10)
        self.msg_label.configure(text=f"😴 {self.pet.name} выспался(ась)!", text_color="#f39812")
        self.update_ui()

    def bathe(self):
        if not self._can_act() or self.pet.stats["energy"] < 15:
            if self.pet and self.pet.alive and self.pet.stats["energy"] < 15:
                self.msg_label.configure(text=f"🛁 {self.pet.name} слишком устал(а) для купания!", text_color="#e74c3c")
            return
        self.pet.stats["hygiene"] = min(100, self.pet.stats["hygiene"] + 65)
        self.pet.stats["energy"] = max(0, self.pet.stats["energy"] - 15)
        self.pet.stats["happiness"] = min(100, self.pet.stats["happiness"] + 5)
        self.msg_label.configure(text=f"🛁 {self.pet.name} чистый и свежий!", text_color="#9b59b6")
        self.update_ui()

    @property
    def stats(self):
        return ["hunger", "thirst", "energy", "happiness", "hygiene"]


if __name__ == "__main__":
    App().mainloop()