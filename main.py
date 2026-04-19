from database import engine, SessionLocal
from models import Base, Book
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

Base.metadata.create_all(engine)

class MyApp:
    def __init__(self, root):   # Настройки окна
        self.root = root
        self.root.title("Русская классика - библиотека")
        self.root.geometry("800x500")
        self.session = SessionLocal()   # Открывает соединение с БД для работы
        self.create_widgets()
        self.refresh_data()

    def create_widgets(self):
        # Рамка для кнопок
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)    # Заполнение рамки по горизонтали с отступами 10

        # Кнопки
        ttk.Button(button_frame, text="Добавить", command=self.add_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Изменить", command=self.update_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить", command=self.delete_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Обновить", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        # command - указывает, какой метод вызвать при нажатии
        # side = tk.LEFT — кнопки располагаются слева направо

        # Рамка для таблицы
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        # fill=tk.BOTH — растягивается в обе стороны
        # expand=True — занимает всё свободное пространство.

        # Таблица (Treeview)
        self.tree = ttk.Treeview(list_frame, columns=('id', 'title', 'author', 'year', 'description'), show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('title', text='Название')
        self.tree.heading('author', text='Автор')
        self.tree.heading('year', text='Год')
        self.tree.heading('description', text='Описание')

        self.tree.column('id', width=50, anchor=tk.CENTER)
        self.tree.column('title', width=200)
        self.tree.column('author', width=120)
        self.tree.column('year', width=70, anchor=tk.CENTER)
        self.tree.column('description', width=300)

        # Скроллбар (вертикальная полоса прокрутки)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_data(self):
        # Очищаем таблицу
        for row in self.tree.get_children():    # get_children() возвращает все строки
            self.tree.delete(row)
        books = self.session.query(Book).all()  # Запрашиваем все записи из таблицы books.

        for book in books:
            self.tree.insert('', tk.END, values=(book.id, book.title, book.author, book.year, book.description))

    def add_book(self):
        title = simpledialog.askstring("Добавление", "Введите название книги:", parent=self.root)
        # simpledialog.askstring - Открывает окошко для ввода текста
        if not title:   # Если пользователь ничего не ввел, то выходим
            return

        author = simpledialog.askstring("Добавление", "Введите автора:", parent=self.root)
        if not author:
            return

        year = simpledialog.askinteger("Добавление", "Введите год издания:", parent=self.root)

        description = simpledialog.askstring("Добавление", "Введите описание:", parent=self.root)

        # Создаём новую книгу
        new_book = Book(
            title=title,
            author=author,
            year=year,
            description=description
        )

        self.session.add(new_book)  # Добавляем книгу в очередь на сохранение
        self.session.commit()   # Отправляет все накопленные изменения в БД
        messagebox.showinfo("Успех", f"Книга '{title}' добавлена")
        # self.refresh_data()

    def update_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу для изменения")
            return

        book_id = self.tree.item(selected[0])['values'][0]
        book = self.session.query(Book).filter(Book.id == book_id).first()

        if not book:
            messagebox.showerror("Ошибка", "Книга не найдена")
            return

        # Окно для изменения
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменение книги")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Название:").pack(pady=(10, 0), anchor="w", padx=10)
        title_entry = tk.Entry(dialog, width=40)
        title_entry.insert(0, book.title)   # Подставляем текущее значение в поле для удобства
        title_entry.pack(pady=5, padx=10)

        tk.Label(dialog, text="Автор:").pack(pady=(10, 0), anchor="w", padx=10)
        author_entry = tk.Entry(dialog, width=40)
        author_entry.insert(0, book.author)
        author_entry.pack(pady=5, padx=10)

        tk.Label(dialog, text="Год:").pack(pady=(10, 0), anchor="w", padx=10)
        year_entry = tk.Entry(dialog, width=40)
        year_entry.insert(0, book.year if book.year else "")
        year_entry.pack(pady=5, padx=10)

        tk.Label(dialog, text="Описание:").pack(pady=(10, 0), anchor="w", padx=10)
        desc_entry = tk.Entry(dialog, width=40)
        desc_entry.insert(0, book.description if book.description else "")
        desc_entry.pack(pady=5, padx=10)

        def save():
            book.title = title_entry.get()  # Обновляем поле объекта
            book.author = author_entry.get()
            year_val = year_entry.get()
            book.year = int(year_val) if year_val.isdigit() else None
            book.description = desc_entry.get()

            self.session.commit()   # Сохраняем изменения в БД
            messagebox.showinfo("Успех", "Книга обновлена")
            dialog.destroy()
            # self.refresh_data()

        tk.Button(dialog, text="Сохранить", command=save, width=15).pack(pady=25)

    def delete_book(self):
        selected = self.tree.selection() # Получаем выбранную строку в таблице
        if not selected:    # Если ничего не выбрано - предупреждение
            messagebox.showwarning("Предупреждение", "Выберите книгу для удаления")
            return

        book_id = self.tree.item(selected[0])['values'][0] # Берёт ID из первого столбца выбранной строки
        book_title = self.tree.item(selected[0])['values'][1]

        if messagebox.askyesno("Подтверждение", f"Удалить книгу '{book_title}'?"):
            book = self.session.query(Book).filter(Book.id == book_id).first()
            if book:
                self.session.delete(book)   # Удаляем из БД
                self.session.commit()
                messagebox.showinfo("Успех", "Книга удалена")
                # self.refresh_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop() # Запускает окно приложения (бесконечный цикл)