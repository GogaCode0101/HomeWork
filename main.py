import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class DocumentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Система электронного делопроизводства")

        self.documents = []  # Список документов

        # Главное меню
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.create_doc_button = tk.Button(self.menu_frame, text="Создать документ", command=self.create_document)
        self.create_doc_button.pack(pady=10)

        self.view_docs_button = tk.Button(self.menu_frame, text="Просмотр документов", command=self.view_documents)
        self.view_docs_button.pack(pady=10)

        self.search_button = tk.Button(self.menu_frame, text="Поиск документа", command=self.search_document)
        self.search_button.pack(pady=10)

        self.document_listbox = tk.Listbox(self.root, width=50)
        self.document_listbox.pack(pady=10)

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

    def search_document(self):
        search_term = simpledialog.askstring("Поиск документа", "Введите ключевое слово для поиска:")
        if search_term:
            found_docs = [doc for doc in self.documents if search_term.lower() in doc["title"].lower()]
            if found_docs:
                self.document_listbox.delete(0, tk.END)
                for doc in found_docs:
                    self.document_listbox.insert(tk.END, doc["title"])
            else:
                messagebox.showinfo("Результаты поиска", "Документы не найдены.")
        else:
            messagebox.showwarning("Ошибка", "Введите ключевое слово для поиска.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentManagementSystem(root)
    root.mainloop()
