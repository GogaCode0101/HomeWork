import tkinter as tk
from tkinter import messagebox, simpledialog


class DocumentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Система электронного делопроизводства")

        self.documents = []  # Список документов
        self.policies = []  # Список положений
        self.job_descriptions = []  # Список должностных инструкций

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
