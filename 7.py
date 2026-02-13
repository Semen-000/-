def dekorator(func):
    def a():
        print("Функция запустилась")
        func()
        print("Функция закончила работу")
    return a

@dekorator
def b():
    print("Начало работы")
b()