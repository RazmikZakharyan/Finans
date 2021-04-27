import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Добавить облигации', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.gif')
        btn_delete = tk.Button(toolbar, text='Удалить облигации', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.gif')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'amount', 'percent', 'duration'),
                                 height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=265, anchor=tk.CENTER)
        self.tree.column('amount', width=150, anchor=tk.CENTER)
        self.tree.column('percent', width=100, anchor=tk.CENTER)
        self.tree.column('duration', width=100, anchor=tk.CENTER)
        # self.tree.column('description', width=365, anchor=tk.CENTER)
        # self.tree.column('costs', width=150, anchor=tk.CENTER)
        # self.tree.column('total', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='name')
        self.tree.heading('amount', text='amount')
        self.tree.heading('percent', text='percent')
        self.tree.heading('duration', text='duration')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, title, amount, percent, duration):
        self.db.insert_data(title, amount, percent, duration)
        self.view_records()

    def update_record(self, title, amount, percent, duration):
        self.db.c.execute('''UPDATE bonds SET title=?, amount=?, percent_value=?, duration=? WHERE ID=?''',
                          (title, amount, percent, duration, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM bonds''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM bonds WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить облигации')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_name = tk.Label(self, text='Name:')
        label_name.place(x=50, y=20)
        label_amount = tk.Label(self, text='Amount:')
        label_amount.place(x=50, y=50)
        label_percent = tk.Label(self, text='Percent:')
        label_percent.place(x=50, y=80)
        label_duration = tk.Label(self, text='Duration:')
        label_duration.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=150, y=20)

        self.entry_amount = ttk.Entry(self)
        self.entry_amount.place(x=150, y=50)

        self.entry_percent = ttk.Entry(self)
        self.entry_percent.place(x=150, y=80)

        self.entry_duration = ttk.Entry(self)
        self.entry_duration.place(x=150, y=110)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(
            self.entry_name.get(),
            self.entry_amount.get(),
            self.entry_percent.get(),
            self.entry_duration.get(),
        )
                         )

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать облигации')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(
            self.entry_name.get(),
            self.entry_amount.get(),
            self.entry_percent.get(),
            self.entry_duration.get(),
        )
                      )

        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM bonds WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1]),
        self.entry_amount.insert(0, row[2]),
        self.entry_percent.insert(0, row[3]),
        self.entry_duration.insert(0, row[4]),


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('bonds.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS bonds(id integer primary key, title text, amount real, percent_value real, duration real)''')
        self.conn.commit()

    def insert_data(self, title, amount, percent, duration):
        self.c.execute('''INSERT INTO bonds(title, amount, percent_value, duration) VALUES (?, ?, ?, ?)''',
                       (title, amount, percent, duration))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Household finance")
    root.geometry("665x450+300+200")
    root.resizable(False, False)
    root.mainloop()
