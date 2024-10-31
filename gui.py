import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from yandex_images_parser import Parser  # Правильное название модуля
from utils import save_images, make_directory
import os
import logging

class YandexImageScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yandex Image Scraper")
        self.query_list = []
        self.setup_ui()
        self.scraper_thread = None
        self.stop_scraper = threading.Event()

    def setup_ui(self):
        self.label_title = tk.Label(self.root, text="Yandex Image Scraper", font=("Helvetica", 16), fg="white", bg="blue")
        self.label_title.pack(pady=10)

        self.query_text = tk.Text(self.root, height=10, wrap='word', bg="white", fg="black", insertbackground="black")
        self.query_text.pack(padx=10, pady=10, fill="both", expand=True)

        self.num_images_label = tk.Label(self.root, text="Количество изображений на запрос:", font=("Helvetica", 12))
        self.num_images_label.pack(pady=5)
        self.num_images_entry = tk.Entry(self.root)
        self.num_images_entry.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Начать парсинг", command=self.start_scraping, bg="blue", fg="white")
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Остановить парсинг", command=self.stop_scraping, bg="blue", fg="white")
        self.stop_button.pack(pady=5)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        self.log_text = tk.Text(self.root, height=10, wrap='word', bg="white", fg="black", state="disabled")
        self.log_text.pack(padx=10, pady=10, fill="both", expand=True)

    def log_message(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state="disabled")

    def start_scraping(self):
        queries = self.query_text.get("1.0", tk.END).strip().split("\n")
        self.query_list = [query.strip() for query in queries if query.strip()]
        try:
            num_images = int(self.num_images_entry.get())
            self.stop_scraper.clear()
            scraper = Parser()
            self.scraper_thread = threading.Thread(target=self.scrape_images, args=(scraper, queries, num_images))
            self.scraper_thread.start()
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректное количество изображений.")

    def scrape_images(self, scraper, queries, num_images):
        for query in queries:
            images = scraper.query_search(query=query, limit=num_images)
            output_dir = f"./images/{query.replace(' ', '_')}"
            make_directory(output_dir)
            save_images(images, dir_path=output_dir, prefix="img_", number_images=True)
            self.log_message(f"Сохранено изображений по запросу '{query}': {len(images)}")

        self.root.after(0, self.show_completion_message)

    def stop_scraping(self):
        self.stop_scraper.set()
        if self.scraper_thread is not None:
            self.scraper_thread.join()
        messagebox.showinfo("Готово", "Парсинг остановлен!")

    def show_completion_message(self):
        messagebox.showinfo("Готово", "Парсинг завершен!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    root.configure(bg="blue")
    app = YandexImageScraperApp(root)
    root.mainloop()
