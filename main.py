import tkinter as tk
import mysql.connector
from tkinter import ttk
from tkinter import *
from functools import partial
from tkcalendar import Calendar

def base_window():
    root = tk.Tk()
    root.geometry("625x280")
    root.title("Меню")

    headl = tk.Label(root, text="Доступные таблицы", font='10')
    headl.place(x=220, y=20)

    z = 0
    z_list = ["Товары", "Цеха", "Расписание", "Заказчики", "Сборщики", "Декораторы", "Заказы", "Содержание заказов",
              "Контракты"]
    head_list = ["products", "shops", "timetable", "customers", "workers", "decorators", "orders", "orderscontent",
                 "designcontracts"]
    for i in range(3):
        for j in range(3):
            action = partial(table_window, head_list[z])
            btn = tk.Button(root, text=z_list[z], bg='lightblue', command=action)
            btn.place(x=100 + i * 150, y=70 + j * 50, width=125)
            z += 1

    selbtn = tk.Button(root, text="Запросы", bg='lightblue', command=routine_window)
    selbtn.place(x=250, y=220, width=125)
    root.mainloop()

def table_window(t):
    roott = tk.Tk()
    roott.title(f"Меню таблицы {t}")
    height = 0
    if t in ['decorators', 'products', 'orders']:
        height = 50
        updatebtn = tk.Button(roott, text="Обновить", bg='lightblue', command=lambda: update_window(t))
        updatebtn.place(x=100, y=220, width=125)

    roott.geometry(f"325x{220 + height}")
    headl = tk.Label(roott, text=f"Таблица {t}", font='10')
    headl.place(x=80, y=20)

    selectbtn = tk.Button(roott, text="Вывести", bg='lightblue', command=lambda: select_window(t))
    selectbtn.place(x=100, y=70, width=125)
    insertbtn = tk.Button(roott, text="Добавить", bg='lightblue', command=lambda: insert_window(t))
    insertbtn.place(x=100, y=120, width=125)
    deletebtn = tk.Button(roott, text="Удалить", bg='lightblue', command=lambda: delete_window(t))
    deletebtn.place(x=100, y=170, width=125)
    roott.mainloop()

def routine_window():
    rootr = tk.Tk()
    rootr.geometry("1300x280")
    rootr.title("Меню запросов по варианту")
    headl = tk.Label(rootr, text="Доступные запросы", font='10')
    headl.place(x=195, y=20)

    z = 1
    for i in range(3):
        for j in range(3):
            action = partial(mini_routine_window, z)
            btn = tk.Button(rootr, text=z, bg='lightblue', command=action)
            btn.place(x=75 + i * 150, y=70 + j * 50, width=125)
            z += 1
    action = partial(mini_routine_window, 10)
    selbtn = tk.Button(rootr, text="10", bg='lightblue', command=action)
    selbtn.place(x=225, y=220, width=125)

    l_list = ["1. Отразить список изделий, собранных одним из сборщиков",
              "2. Отразить сведения о получателях и получаемых ими изделиях",
              "3. Рассчитать стоимость одного из заказов",
              "4. Выяснить дату первого посещения декоратора для каждого покупателя, который вызывал декоратора",
              "5. Показать максимальную сумму предоплаты, внесенную покупателем в Гуапландии за последние 2 года",
              "6. Показать количество произведенных типов мебели за последние 3 года по категориям, отсортировав покупки по убыванию",
              "7. Выяснить, какой стиль в дизайне предпочитает житель, сделавший последний запрос на декоратора в мастерской",
              "8. Вывести стоимость изготовленных изделий по сотрудникам за определенный месяц работы",
              "9. Показать список изготовленных изделий по проектам определенного декоратора",
              "10. Вывести в порядке убывания список изделий по количеству заказов"]
    for i in range(10):
        l_i = tk.Label(rootr, text=l_list[i], anchor='w')
        l_i.place(x=575, y=20 + i * 25, width=710)

    rootr.mainloop()

def exec_sql_t(d, n):
    windowt = tk.Tk()
    windowt.title('Результат запроса')
    db = mysql.connector.connect(host="localhost", user="root", password="root", db="factories")
    cur = db.cursor()
    cur.execute(d(n))
    p = cur.fetchall()
    cur.close()
    db.close()
    if len(p) == 0:
        headl = tk.Label(windowt, text=f"пустой результат")
        headl.pack()
    else:
        for i in range(len(p)):
            for j in range(len(p[0])):
                e = Entry(windowt, width=25, fg='blue')
                e.grid(row=i, column=j)
                try:
                    e.insert(END, p[i][j])
                except TclError:
                    e.insert(END, '')
    windowt.mainloop()

def mini_routine_window(n):

    data_dict = {1: ["WorkerID"], 3: ["OrderID"], 8: ["Month", "Year"], 9: ["DecoratorID"]}

    def diction(n):
        r_dict = {
            1: f'CALL ViewCompletedByWorker1({int(v_list[0].get().split()[0]) if v_list[0].get().split()[0].isdigit() else 0})',
            3: f'CALL CalculateOrder3({int(v_list[0].get().split()[0]) if v_list[0].get().split()[0].isdigit() else 0})',
            9: f'CALL ViewListByDecorator9({int(v_list[0].get().split()[0]) if v_list[0].get().split()[0].isdigit() else 0})',
            8: f'CALL ViewSumPriceByWorkers8("{v_list[0].get()}", "{v_list[1].get()}")'}
        return r_dict[n]

    def diction_zero(n):
        r_dict = {2: f'CALL ViewCustomersAndContents2', 4: f'CALL ViewFirstContract4', 5: f'CALL ViewMaxDeposit5', 6: f'CALL CalculateTypeCount6', 7: f'CALL FindLastStyle7', 10: f'CALL ViewPopularProducts10'}
        return r_dict[n]

    if n in data_dict:
        windowr = tk.Tk()
        windowr.title('Параметры запроса')
        data = data_dict[n]
        v_list = []
        windowr.geometry(f"400x{150 + len(data) * 50}")
        for i in range(len(data)):
            l = tk.Label(windowr, text=data[i], anchor='e')
            l.place(x=50, y=70 + i * 50, width=90)
            if 'ID' in data[i]:
                db = mysql.connector.connect(host="localhost", user="root", password="root", db="factories")
                cur = db.cursor()
                cur.execute(f'SELECT * from {id_dict[data[i]]}')
                p = cur.fetchall()
                cur.close()
                db.close()
                cbox = ttk.Combobox(windowr, state='readonly')
                cbox['values'] = [i[:2] for i in p]
                cbox.place(x=160, y=70 + i * 50, width=200)
                cbox.current(0)
                v_list.append(cbox)
            else:
                e = Entry(windowr, fg='blue')
                e.place(x=160, y=70 + i * 50, width=200)
                v_list.append(e)
        addbtn = tk.Button(windowr, text="Применить", bg='lightblue', command=lambda: exec_sql_t(diction, n))
        addbtn.place(x=140, y=90 + len(data) * 50, width=125)
        while len(v_list) != 2:
            e0 = Entry(windowr, fg='blue')
            v_list.append(e0)
            e0.place(x=0, y=0, width=0)
            e0.insert(0, ".")
        windowr.mainloop()
    else:
        exec_sql_t(diction_zero, n)

def select_window(t):
    db = mysql.connector.connect(host="localhost", user="root", password="root", db="factories")
    cur = db.cursor()
    cur2 = db.cursor()
    windows = tk.Tk()
    windows.title('Содержимое таблицы')

    cur2.execute(f'SHOW COLUMNS FROM {t}')
    i = 0
    w = []
    for s in cur2:
        if 'varchar' in s[1]:
            w.append(30)
        else:
            w.append(10)
        e = Entry(windows, width=w[i], fg='blue')
        e.grid(row=0, column=i)
        e.insert(END, s[0])
        i += 1

    cur.execute(f'SELECT * FROM {t}')
    i = 1
    for s in cur:
        for j in range(len(s)):
            e = Entry(windows, width=w[j], fg='blue')
            e.grid(row=i, column=j)
            try:
                e.insert(END, s[j])
            except TclError:
                e.insert(END, '')
        i += 1
    windows.mainloop()

def exec_sql(win, d, t):
    db = mysql.connector.connect(host="localhost", user="root", password="root", db="factories")
    cur = db.cursor()
    cur.execute(d(t))
    db.commit()
    cur.close()
    db.close()
    win.destroy()

def insert_window(t):
    db = mysql.connector.connect(host="localhost", user="root", password="root", db="factories")
    cur = db.cursor()
    windowi = tk.Tk()
    windowi.title('Добавление записи')
    cur.execute(f'SHOW COLUMNS FROM {t}')
    data = cur.fetchall()
    data_l = len(data) - 1
    cur.close()
    headl = tk.Label(windowi, text="Добавление записи", font='10')
    headl.place(x=110, y=20)

    def date_window():
        mini_window = tk.Tk()
        mini_window.geometry(f"250x250")
        cal = Calendar(mini_window, selectmode='day', year=2023, month=5, day=1)
        cal.place(x=0, y=0)

        def take_date():
            ent.delete(0, END)
            ent.insert(0, cal.get_date())
            mini_window.destroy()

        btn = Button(mini_window, text="ОК", command=take_date)
        btn.place(x=100, y=200, width=50)
        mini_window.mainloop()

    v_list = []
    for i in range(data_l):
        if 'DateR' in data[i + 1][0]:
            data_l -= 1
        else:
            l = tk.Label(windowi, text=data[i + 1][0], anchor='e')
            l.place(x=50, y=70 + i * 50, width=90)
            if 'ID' in data[i + 1][0]:
                cur = db.cursor()
                cur.execute(f'SELECT * from {id_dict[data[i + 1][0]]}')
                p = cur.fetchall()
                cbox = ttk.Combobox(windowi, state='readonly')
                cbox['values'] = [i[:2] for i in p]
                cbox.place(x=160, y=70 + i * 50, width=200)
                cbox.current(0)
                v_list.append(cbox)
            elif 'Date' in data[i + 1][0]:
                ent = Entry(windowi, fg='blue')
                ent.insert(0, "01/01/2023")
                ent.place(x=160, y=70 + i * 50, width=90)
                dbtn = tk.Button(windowi, text="Выбрать дату", bg='lightblue', command=date_window)
                dbtn.place(x=260, y=68 + i * 50, width=100)
                v_list.append(ent)
            else:
                e = Entry(windowi, fg='blue')
                e.place(x=160, y=70 + i * 50, width=200)
                v_list.append(e)
    cur.close()
    db.close()
    while len(v_list) != 5:
        e0 = Entry(windowi, fg='blue')
        v_list.append(e0)
        e0.place(x=0, y=0, width=0)
        e0.insert(0, ".")

    def diction(t):
        ins_dict = {
            'products': f'CALL AddNewProduct("{v_list[0].get()}", {int(v_list[1].get().split()[0]) if v_list[1].get().split()[0].isdigit() else 0}, {int(v_list[2].get().split()[0]) if v_list[2].get().split()[0].isdigit() else 0})',
            'shops': f'CALL AddNewShop("{v_list[0].get()}", "{v_list[1].get()}", "{v_list[2].get()}")',
            'timetable': f'CALL AddDayFor({int(v_list[1].get().split()[0]) if v_list[1].get().split()[0].isdigit() else 0}, STR_TO_DATE("{v_list[0].get()}", "%m/%d/%y"))',
            'customers': f'CALL AddNewCustomer("{v_list[0].get()}", "{v_list[1].get()}", "{v_list[2].get()}", "{v_list[3].get()}")',
            'workers': f'CALL AddNewWorker("{v_list[0].get()}", "{v_list[1].get()}", {int(v_list[2].get().split()[0]) if v_list[2].get().split()[0].isdigit() else 0})',
            'decorators': f'CALL AddNewDecorator("{v_list[0].get()}", "{v_list[1].get()}", "{v_list[2].get()}", {int(v_list[3].get().split()[0]) if v_list[3].get().split()[0].isdigit() else 0})',
            'orders': f'CALL AddNewOrder({int(v_list[0].get().split()[0]) if v_list[0].get().split()[0].isdigit() else 0}, STR_TO_DATE("{v_list[1].get()}", "%m/%d/%y"), {int(v_list[2].get().split()[0]) if v_list[2].get().split()[0].isdigit() else 0}, "{v_list[3].get()}", "{v_list[4].get()}")',
            'orderscontent': f'CALL AddNewContent({int(v_list[0].get().split()[0]) if v_list[0].get().split()[0].isdigit() else 0}, {int(v_list[1].get().split()[0]) if v_list[1].get().split()[0].isdigit() else 0}, {int(v_list[2].get().split()[0]) if v_list[2].get().split()[0].isdigit() else 0}, {int(v_list[3].get().split()[0]) if v_list[3].get().split()[0].isdigit() else 0})',
            'designcontracts': f'CALL AddNewContract({int(v_list[0].get().split()[0]) if v_list[0].get().split()[0].isdigit() else 0}, STR_TO_DATE("{v_list[1].get()}", "%m/%d/%y"), {int(v_list[2].get().split()[0]) if v_list[2].get().split()[0].isdigit() else 0})'}
        return ins_dict[t]

    windowi.geometry(f"400x{150 + data_l * 50}")
    addbtn = tk.Button(windowi, text="Добавить", bg='lightblue', command=lambda: exec_sql(windowi, diction, t))
    addbtn.place(x=140, y=90 + data_l * 50, width=125)
    windowi.mainloop()

def delete_window(t):
    db = mysql.connector.connect(host="localhost", user="root", password="root", db="factories")
    cur = db.cursor()
    windowd = tk.Tk()
    windowd.title('Удаление записи')
    cur.execute(f'SHOW COLUMNS FROM {t}')
    data = cur.fetchall()
    data_l = len(data)
    headl = tk.Label(windowd, text="Удаление записи", font='10')
    headl.place(x=110, y=20)

    cur.execute(f'SELECT * FROM {t}')
    p = cur.fetchall()

    p_id = [i[0] for i in p]
    v_list = []

    def callback():
        for k in range(data_l - 1):
            v_list[k].config(text=p[p_id.index(int(cbox.get().split()[0]))][k + 1], width=100)

    for i in range(data_l):
        l = tk.Label(windowd, text=data[i][0], anchor='e')
        l.place(x=50, y=70 + i * 50, width=90)
        if i == 0:
            cur.execute(f'SELECT * from {id_dict[data[i][0]]}')
            p_new = cur.fetchall()
            cbox = ttk.Combobox(windowd, state='readonly')
            cbox['values'] = [i[:2] for i in p_new]
            cbox.place(x=160, y=70 + i * 50, width=150)
            cbox.current(0)
            dbtn = tk.Button(windowd, text="Просмотр", bg='lightblue', command=callback)
            dbtn.place(x=320, y=68 + i * 50, width=70)
        else:
            l_i = tk.Label(windowd, text=p[p_id.index(int(cbox.get().split()[0]))][i], anchor='w')
            l_i.place(x=160, y=70 + i * 50, width=200)
            v_list.append(l_i)
    cur.close()
    db.close()

    def diction(t):
        del_dict = {
            'products': f'DELETE FROM products WHERE ProductID={int(cbox.get().split()[0])}',
            'shops': f'DELETE FROM shops WHERE ShopID={int(cbox.get().split()[0])}',
            'timetable': f'DELETE FROM timetable WHERE TimetableID={int(cbox.get().split()[0])}',
            'customers': f'DELETE FROM customers WHERE CustomerID={int(cbox.get().split()[0])}',
            'workers': f'DELETE FROM workers WHERE WorkerID={int(cbox.get().split()[0])}',
            'decorators': f'DELETE FROM decorators WHERE DecoratorID={int(cbox.get().split()[0])}',
            'orders': f'DELETE FROM orders WHERE OrderID={int(cbox.get().split()[0])}',
            'orderscontent': f'DELETE FROM orderscontent WHERE ContentID={int(cbox.get().split()[0])}',
            'designcontracts': f'DELETE FROM designcontracts WHERE ContractID={int(cbox.get().split()[0])}'}
        return del_dict[t]

    windowd.geometry(f"400x{150 + data_l * 50}")
    addbtn = tk.Button(windowd, text="Удалить", bg='lightblue', command=lambda: exec_sql(windowd, diction, t))
    addbtn.place(x=140, y=90 + data_l * 50, width=125)
    windowd.mainloop()

def update_window(t):
    db = mysql.connector.connect(host="localhost", user="root", password="root", db="factories")
    cur = db.cursor()
    windowu = tk.Tk()
    windowu.title('Обновление записи')
    cur.execute(f'SHOW COLUMNS FROM {t}')
    data = cur.fetchall()
    data_l = len(data)
    headl = tk.Label(windowu, text="Обновление записи", font='10')
    headl.place(x=110, y=20)

    cur.execute(f'SELECT * FROM {t}')
    p = cur.fetchall()

    p_id = [i[0] for i in p]
    v_list = []
    upd_id = 0

    def callback():
        for k in range(data_l - 1):
            if k == upd_id - 1 and t == 'products':
                v_list[k].config(text=p[p_id.index(int(cbox.get().split()[0]))][k + 2], width=100)

            else:
                v_list[k].config(text=p[p_id.index(int(cbox.get().split()[0]))][k + 1], width=100)
        en.delete(0, 'end')
        en.insert(1, p[p_id.index(int(cbox.get().split()[0]))][upd_id])

    for i in range(data_l):
        l = tk.Label(windowu, text=data[i][0], anchor='e')
        l.place(x=50, y=70 + i * 50, width=90)
        if i == 0:
            cur.execute(f'SELECT * from {id_dict[data[i][0]]}')
            p_new = cur.fetchall()
            cbox = ttk.Combobox(windowu, state='readonly')
            cbox['values'] = [i[:2] for i in p_new]
            cbox.place(x=160, y=70 + i * 50, width=150)
            cbox.current(0)
            dbtn = tk.Button(windowu, text="Просмотр", bg='lightblue', command=callback)
            dbtn.place(x=320, y=68 + i * 50, width=70)
        elif 'Price' in data[i][0] or 'Deposit' in data[i][0]:
            en = Entry(windowu, fg='blue')
            en.insert(1, p[p_id.index(int(cbox.get().split()[0]))][i])
            en.place(x=168, y=70 + i * 50, width=90)
            upd_id = i
        else:
            l_i = tk.Label(windowu, text=p[p_id.index(int(cbox.get().split()[0]))][i], anchor='w')
            l_i.place(x=160, y=70 + i * 50, width=200)
            v_list.append(l_i)
    cur.close()
    db.close()
    while len(v_list) != 5:
        e0 = Entry(windowu, fg='blue')
        v_list.append(e0)
        e0.place(x=0, y=0, width=0)
        e0.insert(0, ".")

    def diction(t):
        upd_dict = {
            'products': f'CALL UpdatePrice({int(cbox.get().split()[0])}, {int(en.get())})',
            'decorators': f'CALL UpdatePriceD({int(cbox.get().split()[0])}, {int(en.get())})',
            'orders': f'CALL UpdatePriceD({int(cbox.get().split()[0])}, {int(en.get())})'}
        return upd_dict[t]

    windowu.geometry(f"400x{150 + data_l * 50}")
    addbtn = tk.Button(windowu, text="Изменить", bg='lightblue', command=lambda: exec_sql(windowu, diction, t))
    addbtn.place(x=140, y=90 + data_l * 50, width=125)
    windowu.mainloop()

id_dict = {'ProductID': 'products', 'ShopID': 'shops', 'CustomerID': 'customers', 'WorkerID': 'workers', 'timetableID': 'timetable', 
           'DecoratorID': 'decorators', 'OrderID': 'orders', 'ContentID': 'orderscontent', 'ContractID': 'designcontracts'}
base_window()
