import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta


class DocumentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Система электронного делопроизводства")

        self.documents = []  # Список документов
        self.policies = []  # Список положений
        self.job_descriptions = []  # Список должностных инструкций
        self.incoming_documents = []  # Список входящих документов
        self.outgoing_documents = []  # Список исходящих документов

        # Переменные для профиля пользователя
        self.username = None  # Имя пользователя
        self.password = None  # Пароль

        # Загрузка данных пользователя
        self.load_user_data()

        # Вызов функции для выбора между регистрацией и авторизацией
        self.show_initial_dialog()

        # Создание панели метаданных
        self.metadata_frame = tk.Frame(self.root)
        self.metadata_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.metadata_label = tk.Label(self.metadata_frame, text="Метаданные документа", font=("Arial", 12))
        self.metadata_label.pack(pady=10)

        self.metadata_text = tk.Text(self.metadata_frame, height=20, width=50)
        self.metadata_text.pack(pady=10)

    def load_user_data(self):
        """Загрузка данных пользователя из файла."""
        if os.path.exists('user_data.json'):
            with open('user_data.json', 'r') as file:
                data = json.load(file)
                self.username = data.get('username')
                self.password = data.get('password')

    def save_user_data(self):
        """Сохранение данных пользователя в файл."""
        with open('user_data.json', 'w') as file:
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

        self.view_button = tk.Button(self.menu_frame, text="Просмотр", command=self.view_item)
        self.view_button.pack(pady=10)

        self.search_button = tk.Button(self.menu_frame, text="Найти", command=self.search_item)
        self.search_button.pack(pady=10)

        self.document_listbox = tk.Listbox(self.root, width=50)
        self.document_listbox.pack(pady=10)

        # Привязка двойного щелчка к функции просмотра содержимого
        self.document_listbox.bind('<Double-1>', self.view_document_content)

        # Панель управления (Dashboard)
        self.dashboard_frame = tk.Frame(self.root)
        self.dashboard_frame.pack(side=tk.TOP, fill=tk.X)

        # Кнопка быстрого создания нового документа
        self.quick_create_button = tk.Button(self.dashboard_frame, text="Быстрое создание документа",
                                             command=self.create_item)
        self.quick_create_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Поле для поиска
        self.search_entry = tk.Entry(self.dashboard_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.search_entry.bind('<Return>', lambda event: self.quick_search())

        self.search_label = tk.Label(self.dashboard_frame, text="Поиск:")
        self.search_label.pack(side=tk.LEFT, padx=5)

        # Кнопка для поиска по документам
        self.quick_search_button = tk.Button(self.dashboard_frame, text="Поиск по документам",
                                             command=self.quick_search)
        self.quick_search_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Уведомления
        self.notifications_button = tk.Button(self.dashboard_frame, text="Уведомления", command=self.show_notifications)
        self.notifications_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Меню пользователя
        self.user_menu_button = tk.Button(self.dashboard_frame, text="Меню пользователя", command=self.user_menu)
        self.user_menu_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Функции для отображения различных разделов
    def show_incoming_documents(self):
        if not self.incoming_documents:
            messagebox.showinfo("Входящие документы", "Нет входящих документов.")
        else:
            documents = "\n".join([doc["title"] for doc in self.incoming_documents])
            messagebox.showinfo("Входящие документы", f"Список входящих документов:\n{documents}")

    def show_outgoing_documents(self):
        if not self.outgoing_documents:
            messagebox.showinfo("Исходящие документы", "Нет исходящих документов.")
        else:
            documents = "\n".join([doc["title"] for doc in self.outgoing_documents])
            messagebox.showinfo("Исходящие документы", f"Список исходящих документов:\n{documents}")

    def show_archive(self):
        archived_documents = self.documents  # Для примера используем все документы как архивированные
        if not archived_documents:
            messagebox.showinfo("Архив", "Нет архивированных документов.")
        else:
            documents = "\n".join([doc["title"] for doc in archived_documents])
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
        recipient = simpledialog.askstring("Получатель (если исходящий)", "Введите получателя:")
        status = simpledialog.askstring("Статус", "Введите статус документа (черновик, на согласовании, подписан и т.д.):")
        deadline = simpledialog.askstring("Дедлайн", "Введите дедлайн для исполнения (формат: ГГГГ-ММ-ДД):")

        # Преобразуем дедлайн в объект datetime
        try:
            deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Ошибка", "Неверный формат даты для дедлайна.")
            return

        document = {
            "title": title,
            "type": item_type,
            "author": author,
            "recipient": recipient,
            "status": status,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "deadline": deadline_date.strftime("%Y-%m-%d"),
        }

        self.documents.append(document)
        messagebox.showinfo("Успех", "Документ успешно создан!")

    def view_item(self):
        if not self.documents:
            messagebox.showinfo("Просмотр", "Нет доступных документов для просмотра.")
            return

        document_titles = "\n".join([doc["title"] for doc in self.documents])
        title = simpledialog.askstring("Выбор документа", f"Выберите документ:\n{document_titles}")

        for doc in self.documents:
            if doc["title"] == title:
                self.display_document_metadata(doc)
                break
        else:
            messagebox.showwarning("Ошибка", "Документ не найден.")

    def display_document_metadata(self, document):
        """Отображение метаданных документа."""
        metadata = f"Тип документа: {document['type']}\n"
        metadata += f"Автор: {document['author']}\n"
        metadata += f"Получатель: {document.get('recipient', 'Нет')}\n"
        metadata += f"Статус: {document['status']}\n"
        metadata += f"Время создания: {document['created_at']}\n"
        metadata += f"Дедлайн: {document['deadline']}\n"

        self.metadata_text.delete(1.0, tk.END)  # Очищаем предыдущее содержимое
        self.metadata_text.insert(tk.END, metadata)

    def view_document_content(self, event):
        selected_title = self.document_listbox.get(self.document_listbox.curselection())
        for doc in self.documents:
            if doc["title"] == selected_title:
                self.display_document_metadata(doc)
                break

    def search_item(self):
        query = simpledialog.askstring("Поиск", "Введите ключевое слово для поиска:")
        if not query:
            messagebox.showwarning("Ошибка", "Введите ключевое слово для поиска.")
            return

        results = [doc for doc in self.documents if query.lower() in doc["title"].lower()]
        if results:
            result_titles = "\n".join([doc["title"] for doc in results])
            messagebox.showinfo("Результаты поиска", f"Найденные документы:\n{result_titles}")
        else:
            messagebox.showinfo("Результаты поиска", "Документы не найдены.")

    def quick_search(self):
        query = self.search_entry.get()
        if query:
            self.search_item()
        else:
            messagebox.showwarning("Ошибка", "Введите ключевое слово для поиска.")

    def show_notifications(self):
        messagebox.showinfo("Уведомления", "Здесь будут ваши уведомления.")

    def user_menu(self):
        messagebox.showinfo("Меню пользователя", "Здесь можно изменить настройки профиля.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentManagementSystem(root)
    root.mainloop()
