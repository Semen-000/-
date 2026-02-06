import tkinter as tk
from tkinter import ttk, simpledialog
import time

class Pitomets:
    def __init__(self, imya, vid):
        self.imya = imya
        self.vid = vid
        self.vozrast = 0
        self.vremya_rozhdeniya = time.time()
        self.posledneye_obnovleniye = time.time()
        self.zhiv = True
        self.prichina_smerti = ""
        self.pokazateli = {
            "golod": 70,
            "zhazhda": 70,
            "energiya": 80,
            "radost": 75,
            "chistota": 85
        }

    def obnovit(self):
        if not self.zhiv:
            return False

        proshlo_sekund = time.time() - self.posledneye_obnovleniye
        if proshlo_sekund < 1:
            return True

        self.posledneye_obnovleniye = time.time()
        self.vozrast = int((time.time() - self.vremya_rozhdeniya) / 60)

        skorost_ukhudsheniya = {
            "golod": 0.22,
            "zhazhda": 0.3,
            "energiya": 0.12,
            "radost": 0.08,
            "chistota": 0.15
        }

        for pokazatel, skorost in skorost_ukhudsheniya.items():
            self.pokazateli[pokazatel] -= proshlo_sekund * skorost

            if self.pokazateli[pokazatel] <= 0 and pokazatel in ["golod", "zhazhda", "energiya", "radost"]:
                self.zhiv = False
                slovar_smerti = {
                    "golod": "голода",
                    "zhazhda": "жажды",
                    "energiya": "усталости",
                    "radost": "скуки"
                }
                self.prichina_smerti = slovar_smerti[pokazatel]
                return False

        for klyuch in self.pokazateli:
            self.pokazateli[klyuch] = max(0, min(100, self.pokazateli[klyuch]))

        return True

    def pokormit(self):
        self.pokazateli["golod"] = min(100, self.pokazateli["golod"] + 35)

    def napoit(self):
        self.pokazateli["zhazhda"] = min(100, self.pokazateli["zhazhda"] + 40)

    def poigrat(self):
        self.pokazateli["radost"] = min(100, self.pokazateli["radost"] + 30)
        self.pokazateli["energiya"] = max(0, self.pokazateli["energiya"] - 15)

    def pospat(self):
        self.pokazateli["energiya"] = min(100, self.pokazateli["energiya"] + 45)

    def umyt(self):
        self.pokazateli["chistota"] = min(100, self.pokazateli["chistota"] + 50)

    def vyrazheniye_lica(self):
        radost = self.pokazateli["radost"]
        if radost >= 85:
            return "😄"
        elif radost >= 65:
            return "😊"
        elif radost >= 40:
            return "😐"
        elif radost >= 20:
            return "😢"
        else:
            return "😭"

class TamagochiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тамагочи")
        self.geometry("400x450")
        self.configure(bg="#2b2b2b")
        self.pitomets = None
        self.pokazat_menu()

    def pokazat_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="ТАМАГОЧИ", font=("Arial", 28, "bold"),
                 fg="#4A90E2", bg="#2b2b2b").pack(pady=30)

        for tekst, vid in [("🐱 Кошка", "кошка"), ("🐶 Собака", "собака"), ("🦜 Попугай", "попугай")]:
            tk.Button(self, text=tekst,
                      command=lambda v=vid: self.sozdat_pitomtsa(v),
                      bg="#3a3a3a", fg="white", width=25, height=2,
                      font=("Arial", 11, "bold"),
                      activebackground="#4a4a4a", bd=0).pack(pady=8)

    def sozdat_pitomtsa(self, vid):
        imya = simpledialog.askstring("Новый питомец", f"Введите имя для {vid}:") or f"Мой {vid}"
        self.pitomets = Pitomets(imya.strip(), vid)
        self.pokazat_igru()

    def pokazat_igru(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.metka_imya = tk.Label(self, font=("Arial", 20, "bold"),
                                   fg="white", bg="#2b2b2b")
        self.metka_imya.pack(pady=10)

        self.metka_vozrast = tk.Label(self, font=("Arial", 12),
                                      fg="#aaaaaa", bg="#2b2b2b")
        self.metka_vozrast.pack()

        self.metka_lico = tk.Label(self, font=("Arial", 50),
                                   fg="white", bg="#2b2b2b")
        self.metka_lico.pack(pady=5)

        self.metka_status = tk.Label(self, font=("Arial", 14),
                                     fg="#2ecc71", bg="#2b2b2b")
        self.metka_status.pack()

        self.paneli = {}
        tsveta = {
            "golod": "#e74c3c",
            "zhazhda": "#3498db",
            "energiya": "#f39812",
            "radost": "#2ecc71",
            "chistota": "#9b59b6"
        }
        ikonki = {
            "golod": "🍗",
            "zhazhda": "💧",
            "energiya": "⚡",
            "radost": "😊",
            "chistota": "🛁"
        }

        for pokazatel in ["golod", "zhazhda", "energiya", "radost", "chistota"]:
            ramka = tk.Frame(self, bg="#2b2b2b")
            ramka.pack(fill="x", padx=20, pady=2)

            tk.Label(ramka, text=ikonki[pokazatel], width=3, fg="white",
                     bg="#2b2b2b", font=("Arial", 14)).pack(side="left")

            panel = ttk.Progressbar(ramka, length=200, mode='determinate')
            panel.pack(side="left", padx=5)

            metka_znacheniya = tk.Label(ramka, text="70", width=3, fg="white",
                                        bg="#2b2b2b", font=("Arial", 10))
            metka_znacheniya.pack(side="left")

            self.paneli[pokazatel] = (panel, metka_znacheniya)

            stil = ttk.Style()
            stil.theme_use('default')
            stil.configure(f"{pokazatel}.Horizontal.TProgressbar",
                           background=tsveta[pokazatel],
                           troughcolor="#3a3a3a",
                           borderwidth=0)
            panel.config(style=f"{pokazatel}.Horizontal.TProgressbar")

        ramka_knopok = tk.Frame(self, bg="#2b2b2b")
        ramka_knopok.pack(pady=15)

        deystviya = [
            ("🍗", "#e74c3c", self.pokormit),
            ("💧", "#3498db", self.napoit),
            ("🎮", "#2ecc71", self.poigrat),
            ("😴", "#f39812", self.pospat),
            ("🛁", "#9b59b6", self.umyt)
        ]

        for i, (tekst, tsvet, komanda) in enumerate(deystviya):
            tk.Button(ramka_knopok, text=tekst, width=4, height=2,
                      bg=tsvet, fg="white", font=("Arial", 12, "bold"),
                      command=komanda, bd=0).grid(row=0, column=i, padx=3)

        self.metka_soobshcheniye = tk.Label(self,
                                            text="Питомец живёт сам по себе 😊",
                                            wraplength=350, fg="#aaaaaa", bg="#2b2b2b", font=("Arial", 11))
        self.metka_soobshcheniye.pack(pady=15)

        tk.Button(self, text="🚪 Выйти", command=self.pokazat_menu,
                  bg="#e74c3c", fg="white", width=12, height=1,
                  font=("Arial", 11, "bold"), bd=0,
                  activebackground="#c0392b").pack(pady=10)

        self.igrovoy_tsikl()

    def pokormit(self):
        if self.pitomets.zhiv:
            self.pitomets.pokormit()
            self.metka_soobshcheniye.config(text=f"🍗 {self.pitomets.imya} поел!", fg="#2ecc71")
            self.obnovit_interfeis()

    def napoit(self):
        if self.pitomets.zhiv:
            self.pitomets.napoit()
            self.metka_soobshcheniye.config(text=f"💧 {self.pitomets.imya} попил!", fg="#3498db")
            self.obnovit_interfeis()

    def poigrat(self):
        if self.pitomets.zhiv:
            self.pitomets.poigrat()
            self.metka_soobshcheniye.config(text=f"🎮 {self.pitomets.imya} играл с тобой!", fg="#2ecc71")
            self.obnovit_interfeis()

    def pospat(self):
        if self.pitomets.zhiv:
            self.pitomets.pospat()
            self.metka_soobshcheniye.config(text=f"😴 {self.pitomets.imya} выспался!", fg="#f39812")
            self.obnovit_interfeis()

    def umyt(self):
        if self.pitomets.zhiv:
            self.pitomets.umyt()
            self.metka_soobshcheniye.config(text=f"🛁 {self.pitomets.imya} чистый!", fg="#9b59b6")
            self.obnovit_interfeis()

    def obnovit_interfeis(self):
        if not self.pitomets or not self.pitomets.zhiv:
            return

        self.metka_imya.config(text=f"{self.pitomets.imya} • {self.pitomets.vid}")
        self.metka_vozrast.config(text=f"Возраст: {self.pitomets.vozrast} мин")
        self.metka_lico.config(text=self.pitomets.vyrazheniye_lica())

        srednee = sum(self.pitomets.pokazateli.values()) / 5
        if srednee >= 80:
            status = "Отлично ✨"
            tsvet = "#2ecc71"
        elif srednee >= 60:
            status = "Норм 🙂"
            tsvet = "#f39812"
        elif srednee >= 40:
            status = "Плохо 😐"
            tsvet = "#e67e22"
        else:
            status = "Критично ⚠️"
            tsvet = "#e74c3c"
        self.metka_status.config(text=f"Статус: {status}", fg=tsvet)

        for pokazatel, (panel, metka) in self.paneli.items():
            znachenie = self.pitomets.pokazateli[pokazatel]
            panel['value'] = znachenie
            metka.config(text=str(int(znachenie)))

        nizkiye = [k for k, v in self.pitomets.pokazateli.items() if v < 15]
        if nizkiye:
            slovar_preduprezhdeniy = {
                "golod": "голоден",
                "zhazhda": "хочет пить",
                "energiya": "устал",
                "radost": "грустит",
                "chistota": "грязный"
            }
            tekst = f"⚠️ {self.pitomets.imya}: {', '.join([slovar_preduprezhdeniy[k] for k in nizkiye[:2]])}"
            self.metka_soobshcheniye.config(text=tekst, fg="#e74c3c")

    def igrovoy_tsikl(self):
        if self.pitomets and self.pitomets.obnovit():
            self.obnovit_interfeis()
            self.after(2000, self.igrovoy_tsikl)
        else:
            self.pokazat_konec_igry()

    def pokazat_konec_igry(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text=self.pitomets.imya,
                 font=("Arial", 28, "bold"), fg="#e74c3c", bg="#2b2b2b").pack(pady=30)
        tk.Label(self, text=f"🕯️ Умер от {self.pitomets.prichina_smerti} 🕯️",
                 font=("Arial", 20), fg="white", bg="#2b2b2b").pack(pady=15)
        tk.Label(self, text=f"Прожил: {self.pitomets.vozrast} мин",
                 font=("Arial", 16), fg="#f39812", bg="#2b2b2b").pack(pady=10)

        tk.Button(self, text="🔄 Новая игра", command=self.pokazat_menu,
                  bg="#2ecc71", fg="white", width=15, height=1,
                  font=("Arial", 11, "bold"), bd=0,
                  activebackground="#27ae60").pack(pady=15)
        tk.Button(self, text="🚪 Выйти", command=self.quit,
                  bg="#e74c3c", fg="white", width=15, height=1,
                  font=("Arial", 11, "bold"), bd=0,
                  activebackground="#c0392b").pack()

if __name__ == "__main__":
    prilozheniye = TamagochiApp()
    prilozheniye.mainloop()