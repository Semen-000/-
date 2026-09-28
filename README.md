import tkinter as tk
from tkinter import messagebox

def open_okno():
    root.withdraw()
    okno = tk.Toplevel()
    okno.title("Reg")
    okno.geometry("300x350")

    def back_to_login():
        okno.destroy()
        root.deiconify()

    okno.protocol("WM_DELETE_WINDOW", back_to_login)

    lbl_login = tk.Label(okno, text="Login")
    lbl_login.pack(pady=5)
    ent_login = tk.Entry(okno)
    ent_login.pack(pady=5)

    lbl_pass = tk.Label(okno, text="Pass")
    lbl_pass.pack(pady=5)
    ent_pass = tk.Entry(okno, show="*")
    ent_pass.pack(pady=5)

    lbl_confirm = tk.Label(okno, text="Confirm")
    lbl_confirm.pack(pady=5)
    ent_confirm = tk.Entry(okno, show="*")
    ent_confirm.pack(pady=5)

    def finish_reg():
        if ent_pass.get() != ent_confirm.get():
            messagebox.showerror("Error", "Passes not match!")
            return
        back_to_login()

    btn_finish = tk.Button(okno, text="Finish", command=finish_reg)
    btn_finish.pack(pady=20)

root = tk.Tk()
root.title("Login")
root.geometry("300x250")

lbl_l = tk.Label(root, text="Login")
lbl_l.pack(pady=5)
ent_l = tk.Entry(root)
ent_l.pack(pady=5)

lbl_p = tk.Label(root, text="Pass")
lbl_p.pack(pady=5)
ent_p = tk.Entry(root, show="*")
ent_p.pack(pady=5)

btn_enter = tk.Button(root, text="Enter")
btn_enter.pack(side="left", padx=20, pady=20)

btn_reg = tk.Button(root, text="Reg", command=open_okno)
btn_reg.pack(side="right", padx=20, pady=20)

root.mainloop()
