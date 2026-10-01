import psycopg2
from tkinter import *
from tkinter import ttk

main = Tk()
main.geometry("400x400")
main.minsize(width=400, height=400)

lable1 = ttk.Label(text="Введите логин")
lable1.pack(pady=10)

entry_login = ttk.Entry()
entry_login.pack(pady=10)

lable2 = ttk.Label(text="Введите пароль")
lable2.pack(pady=10)

entry_password = ttk.Entry(show="*")
entry_password.pack(pady=10)

def reg():
    login = entry_login.get()
    password = entry_password.get()
    conn = psycopg2.connect(dbname="postgres", host="localhost", user="postgres", password="12345", port="5432")
    cursor = conn.cursor()
    spisok = (login, password)
    cursor.execute("INSERT INTO people (name, age) VALUES (%s, %s)", spisok)
    conn.commit()
    conn.close()

def pol():
    conn = psycopg2.connect(dbname="postgres", host="localhost", user="postgres", password="12345", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM people WHERE name = 'Tom' or name = 'bob'")
    ghashgd = cursor.fetchall()
    print(ghashgd)

btn_reg = ttk.Button(text="Зарегестрироваться", command=reg)
btn_reg.pack(pady=10)

btn_reg = ttk.Button(text="получить", command=pol)
btn_reg.pack(pady=10)

main.mainloop()
