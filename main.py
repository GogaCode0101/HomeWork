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

        self.create_doc_button = tk.Button(self.menu_frame, text="Создать документ", command=self.create_document)
        self.create_doc_button.pack(pady=10)

        self.view_docs_button = tk.Button(self.menu_frame, text="Просмотр документов", command=self.view_documents)
        self.view_docs_button.pack(pady=10)

        self.create_policy_button = tk.Button(self.menu_frame, text="Добавить положение", command=self.create_policy)
        self.create_policy_button.pack(pady=10)

        self.view_policies_button = tk.Button(self.menu_frame, text="Просмотр положений", command=self.view_policies)
        self.view_policies_button.pack(pady=10)

        self.create_job_desc_button = tk.Button(self.menu_frame, text="Добавить должностную инструкцию",
                                                command=self.create_job_description)
        self.create_job_desc_button.pack(pady=10)

        self.view_job_desc_button = tk.Button(self.menu_frame, text="Просмотр должностных инструкций",
                                              command=self.view_job_descriptions)
        self.view_job_desc_button.pack(pady=10)

        self.search_doc_button = tk.Button(self.menu_frame, text="Найти документ", command=self.search_document)
        self.search_doc_button.pack(pady=10)

        self.search_policy_button = tk.Button(self.menu_frame, text="Найти положение", command=self.search_policy)
        self.search_policy_button.pack(pady=10)

        self.search_job_desc_button = tk.Button(self.menu_frame, text="Найти инструкцию",
                                                command=self.search_job_description)
        self.search_job_desc_button.pack(pady=10)

        self.document_listbox = tk.Listbox(self.root, width=50)
        self.document_listbox.pack(pady=10)

        # Привязка двойного щелчка к функции просмотра документа
        self.document_listbox.bind('<Double-1>', self.view_document_content)

    def create_document(self):
        doc_title = simpledialog.askstring("Название документа", "Введите название документа:")
        doc_content = simpledialog.askstring("Содержимое документа", "Введите содержимое документа:")
        if doc_title and doc_content:
            self.documents.append({"title": doc_title, "content": doc_content})
            messagebox.showinfo("Успех", f"Документ '{doc_title}' создан!")
        else:
            messagebox.showwarning("Ошибка", "Название и содержимое документа не могут быть пустыми.")

    def view_documents(self):
        self.document_listbox.delete(0, tk.END)
        for doc in self.documents:
            self.document_listbox.insert(tk.END, doc["title"])

    def create_policy(self):
        policy_title = simpledialog.askstring("Название положения", "Введите название положения:")
        policy_content = simpledialog.askstring("Содержимое положения", "Введите содержимое положения:")
        if policy_title and policy_content:
            self.policies.append({"title": policy_title, "content": policy_content})
            messagebox.showinfo("Успех", f"Положение '{policy_title}' создано!")
        else:
            messagebox.showwarning("Ошибка", "Название и содержимое положения не могут быть пустыми.")

    def view_policies(self):
        self.document_listbox.delete(0, tk.END)
        for policy in self.policies:
            self.document_listbox.insert(tk.END, policy["title"])

    def create_job_description(self):
        job_title = simpledialog.askstring("Название должностной инструкции",
                                           "Введите название должностной инструкции:")
        job_content = simpledialog.askstring("Содержимое должностной инструкции",
                                             "Введите содержимое должностной инструкции:")
        if job_title and job_content:
            self.job_descriptions.append({"title": job_title, "content": job_content})
            messagebox.showinfo("Успех", f"Должностная инструкция '{job_title}' создана!")
        else:
            messagebox.showwarning("Ошибка", "Название и содержимое должностной инструкции не могут быть пустыми.")

    def view_job_descriptions(self):
        self.document_listbox.delete(0, tk.END)
        for job_desc in self.job_descriptions:
            self.document_listbox.insert(tk.END, job_desc["title"])

    # Поиск документа
    def search_document(self):
        search_query = simpledialog.askstring("Поиск документа", "Введите название документа для поиска:")
        if search_query:
            found = False
            for doc in self.documents:
                if search_query.lower() in doc["title"].lower():
                    found = True
                    messagebox.showinfo("Найдено", f"Документ найден: {doc['title']}\nСодержимое:\n{doc['content']}")
                    break
            if not found:
                messagebox.showwarning("Не найдено", "Документ не найден.")

    # Поиск положения
    def search_policy(self):
        search_query = simpledialog.askstring("Поиск положения", "Введите название положения для поиска:")
        if search_query:
            found = False
            for policy in self.policies:
                if search_query.lower() in policy["title"].lower():
                    found = True
                    messagebox.showinfo("Найдено",
                                        f"Положение найдено: {policy['title']}\nСодержимое:\n{policy['content']}")
                    break
            if not found:
                messagebox.showwarning("Не найдено", "Положение не найдено.")

    # Поиск должностной инструкции
    def search_job_description(self):
        search_query = simpledialog.askstring("Поиск инструкции", "Введите название инструкции для поиска:")
        if search_query:
            found = False
            for job_desc in self.job_descriptions:
                if search_query.lower() in job_desc["title"].lower():
                    found = True
                    messagebox.showinfo("Найдено",
                                        f"Инструкция найдена: {job_desc['title']}\nСодержимое:\n{job_desc['content']}")
                    break
            if not found:
                messagebox.showwarning("Не найдено", "Инструкция не найдена.")

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
