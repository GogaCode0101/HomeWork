import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json
import os
from datetime import datetime


class DocumentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Система электронного делопроизводства")

        self.documents = []  # Список документов
        self.username = None  # Имя пользователя
        self.password = None  # Пароль

        # Загрузка данных пользователя и документов
        self.load_user_data()
        self.load_documents()

        # Выбор между регистрацией и авторизацией
        self.show_initial_dialog()

        # Панель метаданных
        self.metadata_frame = tk.Frame(self.root)
        self.metadata_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.metadata_label = tk.Label(self.metadata_frame, text="Метаданные документа", font=("Arial", 12))
        self.metadata_label.pack(pady=10)

        self.metadata_text = tk.Text(self.metadata_frame, height=20, width=50)
        self.metadata_text.pack(pady=10)

    def load_user_data(self):
        """Загрузка данных пользователя из файла."""
        if os.path.exists('user_data.json'):
            with open('user_data.json', 'r', encoding='utf-8') as file:  # Указание кодировки
                data = json.load(file)
                self.username = data.get('username')
                self.password = data.get('password')

    def save_user_data(self):
        """Сохранение данных пользователя в файл."""
        with open('user_data.json', 'w', encoding='utf-8') as file:  # Указание кодировки
            json.dump({'username': self.username, 'password': self.password}, file)

    def show_initial_dialog(self):
        choice = simpledialog.askstring("Регистрация / Авторизация",
                                          "Введите '1' для регистрации или '2' для авторизации:")
        if choice == '1':
            self.register()
        elif choice == '2':
            self.authenticate()
        else:
            messagebox.showwarning("Ошибка", "Неверный выбор. Пожалуйста, попробуйте снова.")
            self.show_initial_dialog()

    def register(self):
        self.username = simpledialog.askstring("Регистрация", "Введите имя пользователя:")
        self.password = simpledialog.askstring("Регистрация", "Введите пароль:", show='*')

        if self.username and self.password:
            self.save_user_data()  # Сохранение данных пользователя
            messagebox.showinfo("Успех", "Вы успешно зарегистрировались!")
            self.setup_ui()  # Запуск основного интерфейса
        else:
            messagebox.showwarning("Ошибка", "Имя пользователя и пароль не могут быть пустыми.")
            self.show_initial_dialog()  # Повторный выбор

    def authenticate(self):
        while True:
            username = simpledialog.askstring("Авторизация", "Введите имя пользователя:")
            password = simpledialog.askstring("Авторизация", "Введите пароль:", show='*')

            if username == self.username and password == self.password:
                messagebox.showinfo("Успех", "Вы успешно авторизовались!")
                self.setup_ui()  # Запуск основного интерфейса
                break
            else:
                messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль. Попробуйте снова.")

    def setup_ui(self):
        # Главное меню
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Боковая панель навигации
        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Кнопки навигации
        self.incoming_button = tk.Button(self.navigation_frame, text="Входящие документы",
                                         command=self.show_incoming_documents)
        self.incoming_button.pack(pady=5)

        self.outgoing_button = tk.Button(self.navigation_frame, text="Исходящие документы",
                                         command=self.show_outgoing_documents)
        self.outgoing_button.pack(pady=5)

        self.archive_button = tk.Button(self.navigation_frame, text="Архив", command=self.show_archive)
        self.archive_button.pack(pady=5)

        self.tasks_button = tk.Button(self.navigation_frame, text="Задачи", command=self.show_tasks)
        self.tasks_button.pack(pady=5)

        self.admin_button = tk.Button(self.navigation_frame, text="Настройки и администрирование",
                                      command=self.show_admin_panel)
        self.admin_button.pack(pady=5)

        self.create_button = tk.Button(self.menu_frame, text="Создать", command=self.create_item)
        self.create_button.pack(pady=10)

        self.document_listbox = tk.Listbox(self.root, width=50)
        self.document_listbox.pack(pady=10)

        # Привязка двойного щелчка к функции просмотра содержимого
        self.document_listbox.bind('<Double-1>', self.view_document_content)

        # Обновляем список документов
        self.update_document_listbox()

    def load_documents(self):
        """Загрузка документов из файла."""
        if os.path.exists('documents.json'):
            with open('documents.json', 'r', encoding='utf-8') as file:  # Указание кодировки
                self.documents = json.load(file)
        else:
            self.documents = []

    def save_documents(self):
        """Сохранение документов в файл."""
        with open('documents.json', 'w', encoding='utf-8') as file:  # Указание кодировки
            json.dump(self.documents, file)

    def update_document_listbox(self):
        """Обновление списка документов в Listbox."""
        self.document_listbox.delete(0, tk.END)  # Очищаем предыдущий список
        for doc in self.documents:
            self.document_listbox.insert(tk.END, doc["title"])  # Добавляем заголовки документов

    def show_incoming_documents(self):
        incoming_docs = [doc for doc in self.documents if doc.get('recipient')]
        if not incoming_docs:
            messagebox.showinfo("Входящие документы", "Нет входящих документов.")
        else:
            documents = "\n".join([doc["title"] for doc in incoming_docs])
            messagebox.showinfo("Входящие документы", f"Список входящих документов:\n{documents}")

    def show_outgoing_documents(self):
        outgoing_docs = [doc for doc in self.documents if not doc.get('recipient')]
        if not outgoing_docs:
            messagebox.showinfo("Исходящие документы", "Нет исходящих документов.")
        else:
            documents = "\n".join([doc["title"] for doc in outgoing_docs])
            messagebox.showinfo("Исходящие документы", f"Список исходящих документов:\n{documents}")

    def show_archive(self):
        if not self.documents:
            messagebox.showinfo("Архив", "Нет архивированных документов.")
        else:
            documents = "\n".join([doc["title"] for doc in self.documents])
            messagebox.showinfo("Архив", f"Список архивированных документов:\n{documents}")

    def show_tasks(self):
        tasks = ["Задача 1: Подготовить отчет", "Задача 2: Провести встречу", "Задача 3: Обновить документацию"]
        if not tasks:
            messagebox.showinfo("Задачи", "Нет текущих задач.")
        else:
            task_list = "\n".join(tasks)
            messagebox.showinfo("Задачи", f"Список задач:\n{task_list}")

    def show_admin_panel(self):
        messagebox.showinfo("Настройки и администрирование",
                            "Здесь будут настройки и администрирование системы.")

    def create_item(self):
        item_type = simpledialog.askstring("Тип документа", "Введите тип документа (например, 'положение', 'инструкция', 'документ'):")
        title = simpledialog.askstring("Название", "Введите название документа:")
        author = simpledialog.askstring("Автор", "Введите имя автора:")
        recipient = simpledialog.askstring("Получатель (если исходящий)", "Введите получателя (оставьте пустым, если не исходящий):")
        status = simpledialog.askstring("Статус", "Введите статус документа:")
        deadline = simpledialog.askstring("Дедлайн", "Введите дедлайн для исполнения (формат: ГГГГ-ММ-ДД):")

        # Преобразуем дедлайн в объект datetime
        try:
            deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Ошибка", "Неверный формат даты для дедлайна.")
            return

        # Открываем диалог для выбора файла
        file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

        document = {
            "title": title,
            "type": item_type,
            "author": author,
            "recipient": recipient,
            "status": status,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "deadline": deadline_date.strftime("%Y-%m-%d"),
            "file_path": file_path,
        }

        self.documents.append(document)
        self.save_documents()  # Сохраняем изменения в файл
        messagebox.showinfo("Успех", "Документ успешно создан!")

        # Обновляем список документов
        self.update_document_listbox()

    def view_document_content(self, event):
        selected_title = self.document_listbox.get(self.document_listbox.curselection())
        for doc in self.documents:
            if doc["title"] == selected_title:
                self.display_document_metadata(doc)
                break

    def display_document_metadata(self, document):
        """Отображение метаданных документа и его содержимого из файла."""
        metadata = f"Тип документа: {document['type']}\n"
        metadata += f"Автор: {document['author']}\n"
        metadata += f"Получатель: {document.get('recipient', 'Нет')}\n"
        metadata += f"Статус: {document['status']}\n"
        metadata += f"Время создания: {document['created_at']}\n"
        metadata += f"Дедлайн: {document['deadline']}\n"

        # Загрузка содержимого из файла, если указано
        file_content = self.load_file_content(document.get('file_path'))
        metadata += f"\nСодержимое из файла:\n{file_content}"

        self.metadata_text.delete(1.0, tk.END)  # Очищаем предыдущее содержимое
        self.metadata_text.insert(tk.END, metadata)

    def load_file_content(self, file_path):
        """Чтение содержимого файла по указанному пути."""
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:  # Указание кодировки
                return file.read()
        return "Файл не найден или путь не указан."


if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentManagementSystem(root)
    root.mainloop()
