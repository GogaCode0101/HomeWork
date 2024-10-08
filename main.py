import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os


class DocumentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Система электронного делопроизводства")

        self.documents = []  # Список документов
        self.policies = []  # Список положений
        self.job_descriptions = []  # Список должностных инструкций

        # Переменные для профиля пользователя
        self.username = None  # Имя пользователя
        self.password = None  # Пароль

        # Загрузка данных пользователя
        self.load_user_data()

        # Вызов функции для выбора между регистрацией и авторизацией
        if self.username and self.password:
            self.authenticate()
        else:
            self.show_initial_dialog()

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

    # Функция для показа уведомлений
    def show_notifications(self):
        notifications = "Новые документы: {}\nТребующие действий: {}\nНапоминания: {}".format(len(self.documents), 0, 0)
        messagebox.showinfo("Уведомления", notifications)

    # Функция для пользовательского меню
    def user_menu(self):
        user_choice = simpledialog.askstring("Меню пользователя",
                                             "Введите '1' для настройки профиля или '2' для выхода:")
        if user_choice == '1':
            self.setup_profile()
        elif user_choice == '2':
            self.root.quit()
        else:
            messagebox.showwarning("Ошибка", "Неверный выбор.")

    # Настройка профиля
    def setup_profile(self):
        new_username = simpledialog.askstring("Настройка профиля", "Введите новое имя пользователя:",
                                              initialvalue=self.username)
        if new_username is not None:
            self.username = new_username

        new_password = simpledialog.askstring("Настройка профиля", "Введите новый пароль:", show='*')
        if new_password is not None:
            self.password = new_password

        self.save_user_data()  # Сохранение обновленных данных
        messagebox.showinfo("Настройка профиля",
                            f"Профиль обновлён.\nИмя пользователя: {self.username}\nПароль: {self.password}")

    # Функция для быстрого поиска по документам
    def quick_search(self):
        search_query = self.search_entry.get()
        if search_query:
            found = False
            for doc in self.documents + self.policies + self.job_descriptions:
                if search_query.lower() in doc["title"].lower() or search_query.lower() in doc["content"].lower():
                    found = True
                    messagebox.showinfo("Найдено", f"Найдено: {doc['title']}\nСодержимое:\n{doc['content']}")
                    break
            if not found:
                messagebox.showwarning("Не найдено", "Документ не найден.")
        else:
            messagebox.showwarning("Ошибка", "Введите запрос для поиска.")

    # Объединённая функция для создания
    def create_item(self):
        create_type = simpledialog.askstring("Создать",
                                             "Что вы хотите создать? (документ/положение/инструкция)").lower()

        if not create_type:
            messagebox.showwarning("Ошибка", "Вы должны ввести тип создания.")
            return

        if create_type == "документ":
            doc_title = simpledialog.askstring("Название документа", "Введите название документа:")
            doc_content = simpledialog.askstring("Содержимое документа", "Введите содержимое документа:")
            if doc_title and doc_content:
                self.documents.append({"title": doc_title, "content": doc_content})
                messagebox.showinfo("Успех", f"Документ '{doc_title}' создан!")
            else:
                messagebox.showwarning("Ошибка", "Название и содержимое документа не могут быть пустыми.")

        elif create_type == "положение":
            policy_title = simpledialog.askstring("Название положения", "Введите название положения:")
            policy_content = simpledialog.askstring("Содержимое положения", "Введите содержимое положения:")
            if policy_title and policy_content:
                self.policies.append({"title": policy_title, "content": policy_content})
                messagebox.showinfo("Успех", f"Положение '{policy_title}' создано!")
            else:
                messagebox.showwarning("Ошибка", "Название и содержимое положения не могут быть пустыми.")

        elif create_type == "инструкция":
            job_title = simpledialog.askstring("Название должностной инструкции",
                                               "Введите название должностной инструкции:")
            job_content = simpledialog.askstring("Содержимое должностной инструкции",
                                                 "Введите содержимое должностной инструкции:")
            if job_title and job_content:
                self.job_descriptions.append({"title": job_title, "content": job_content})
                messagebox.showinfo("Успех", f"Должностная инструкция '{job_title}' создана!")
            else:
                messagebox.showwarning("Ошибка", "Название и содержимое должностной инструкции не могут быть пустыми.")
        else:
            messagebox.showwarning("Ошибка", "Тип создания должен быть 'документ', 'положение' или 'инструкция'.")

    # Объединённая функция для просмотра
    def view_item(self):
        view_type = simpledialog.askstring("Просмотр",
                                           "Что вы хотите просмотреть? (документ/положение/инструкция)").lower()

        if not view_type:
            messagebox.showwarning("Ошибка", "Вы должны ввести тип просмотра.")
            return

        self.document_listbox.delete(0, tk.END)

        if view_type == "документ":
            for doc in self.documents:
                self.document_listbox.insert(tk.END, doc["title"])
        elif view_type == "положение":
            for policy in self.policies:
                self.document_listbox.insert(tk.END, policy["title"])
        elif view_type == "инструкция":
            for job_desc in self.job_descriptions:
                self.document_listbox.insert(tk.END, job_desc["title"])
        else:
            messagebox.showwarning("Ошибка", "Тип просмотра должен быть 'документ', 'положение' или 'инструкция'.")

    # Функция для объединённого поиска
    def search_item(self):
        search_type = simpledialog.askstring("Поиск", "Что вы хотите найти? (документ/положение/инструкция)").lower()
        search_query = simpledialog.askstring("Поиск", "Введите название для поиска:")

        if not search_type or not search_query:
            messagebox.showwarning("Ошибка", "Вы должны ввести тип поиска и запрос.")
            return

        found = False
        if search_type == "документ":
            for doc in self.documents:
                if search_query.lower() in doc["title"].lower():
                    found = True
                    messagebox.showinfo("Найдено", f"Документ найден: {doc['title']}\nСодержимое:\n{doc['content']}")
                    break
        elif search_type == "положение":
            for policy in self.policies:
                if search_query.lower() in policy["title"].lower():
                    found = True
                    messagebox.showinfo("Найдено",
                                        f"Положение найдено: {policy['title']}\nСодержимое:\n{policy['content']}")
                    break
        elif search_type == "инструкция":
            for job_desc in self.job_descriptions:
                if search_query.lower() in job_desc["title"].lower():
                    found = True
                    messagebox.showinfo("Найдено",
                                        f"Инструкция найдена: {job_desc['title']}\nСодержимое:\n{job_desc['content']}")
                    break
        else:
            messagebox.showwarning("Ошибка", "Тип поиска должен быть 'документ', 'положение' или 'инструкция'.")

        if not found:
            messagebox.showwarning("Не найдено", f"{search_type.capitalize()} не найден(о).")

    def view_document_content(self, event=None):
        selected_index = self.document_listbox.curselection()
        if selected_index:
            selected_doc = self.documents + self.policies + self.job_descriptions
            selected_item = selected_doc[selected_index[0]]
            content_window = tk.Toplevel(self.root)
            content_window.title(selected_item["title"])

            content_label = tk.Label(content_window, text=selected_item["content"], padx=10, pady=10)
            content_label.pack()

            close_button = tk.Button(content_window, text="Закрыть", command=content_window.destroy)
            close_button.pack(pady=5)
        else:
            messagebox.showwarning("Ошибка", "Выберите документ для просмотра.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentManagementSystem(root)
    root.mainloop()
