import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                             QProgressBar, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Импорт вашего парсера
import requests
import xlsxwriter
from bs4 import BeautifulSoup
from time import sleep

class ParserThread(QThread):
    update_signal = pyqtSignal(str, int)
    finished_signal = pyqtSignal(list)
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.list_card_url = []
        self.running = True

    def run(self):
        try:
            # Сбор ссылок на карточки товаров
            for count in range(1, 8):
                if not self.running:
                    return
                
                sleep(1)  # Уменьшил задержку для демонстрации
                url = f"https://scrapingclub.com/exercise/list_basic/?page={count}"
                self.update_signal.emit(f"Обрабатываю страницу {count}: {url}", 20 * count)
                
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, "lxml")
                    data = soup.find_all("div", class_="w-full rounded border")
                    
                    if not data:
                        self.update_signal.emit(f"Не найдены карточки товаров на странице {url}", 0)
                        continue
                    
                    for i in data:
                        card_url = "https://scrapingclub.com" + i.find("a").get("href")
                        self.list_card_url.append(card_url)
                except Exception as e:
                    self.error_signal.emit(f"Ошибка при обработке страницы {url}: {str(e)}")
                    continue

            self.update_signal.emit(f"Собрано {len(self.list_card_url)} ссылок на карточки товаров.", 50)

            # Сбор данных из карточек товаров
            result = []
            total = len(self.list_card_url)
            for i, card_url in enumerate(self.list_card_url):
                if not self.running:
                    return
                
                sleep(1)  # Уменьшил задержку для демонстрации
                progress = 50 + int((i / total) * 50)
                self.update_signal.emit(f"Обрабатываю карточку {i+1}/{total}: {card_url}", progress)
                
                try:
                    response = requests.get(card_url)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, "lxml")
                    data = soup.find("div", class_="my-8 w-full rounded border")
                    
                    if not data:
                        self.error_signal.emit(f"Не удалось найти данные для URL: {card_url}")
                        continue
                    
                    name = data.find("h3", class_="card-title").text
                    price = data.find("h4", class_="my-4 card-price").text
                    text = data.find("p", class_="card-description").text
                    url_img = "https://scrapingclub.com" + data.find("img", class_="card-img-top").get("src")
                    
                    result.append((name, price, url_img, text))
                except Exception as e:
                    self.error_signal.emit(f"Ошибка при обработке карточки {card_url}: {str(e)}")
                    continue

            self.finished_signal.emit(result)
            self.update_signal.emit("Парсинг завершен успешно!", 100)
            
        except Exception as e:
            self.error_signal.emit(f"Критическая ошибка: {str(e)}")

    def stop(self):
        self.running = False
        self.wait()

class ParserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.parser_thread = None
        self.parsed_data = []

    def initUI(self):
        self.setWindowTitle("Парсер товаров")
        self.setGeometry(300, 300, 600, 400)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Заголовок
        title_label = QLabel("Парсер товаров с scrapingclub.com")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Старт")
        self.start_button.clicked.connect(self.start_parsing)
        buttons_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Стоп")
        self.stop_button.clicked.connect(self.stop_parsing)
        self.stop_button.setEnabled(False)
        buttons_layout.addWidget(self.stop_button)
        
        self.save_button = QPushButton("Сохранить в Excel")
        self.save_button.clicked.connect(self.save_to_excel)
        self.save_button.setEnabled(False)
        buttons_layout.addWidget(self.save_button)
        
        layout.addLayout(buttons_layout)

        # Прогресс бар
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Лог
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # Статус
        self.status_label = QLabel("Готов к работе")
        layout.addWidget(self.status_label)

    def start_parsing(self):
        self.log_text.clear()
        self.progress_bar.setValue(0)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.save_button.setEnabled(False)
        self.status_label.setText("Парсинг запущен...")
        
        self.parser_thread = ParserThread()
        self.parser_thread.update_signal.connect(self.update_status)
        self.parser_thread.finished_signal.connect(self.parsing_finished)
        self.parser_thread.error_signal.connect(self.show_error)
        self.parser_thread.start()

    def stop_parsing(self):
        if self.parser_thread:
            self.parser_thread.stop()
            self.status_label.setText("Парсинг остановлен")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.log_text.append("Парсинг был остановлен пользователем")

    def parsing_finished(self, result):
        self.parsed_data = result
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.save_button.setEnabled(True)
        self.status_label.setText(f"Парсинг завершен. Найдено {len(result)} товаров.")

    def update_status(self, message, progress):
        self.log_text.append(message)
        self.progress_bar.setValue(progress)

    def show_error(self, error_message):
        self.log_text.append(f"ОШИБКА: {error_message}")

    def save_to_excel(self):
        if not self.parsed_data:
            QMessageBox.warning(self, "Ошибка", "Нет данных для сохранения")
            return
        
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить файл", "", "Excel Files (*.xlsx)")
            
            if not file_path:
                return
            
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'
            
            self.status_label.setText("Сохранение файла...")
            QApplication.processEvents()  # Обновляем GUI
            
            book = xlsxwriter.Workbook(file_path)
            page = book.add_worksheet("Товары")
            
            # Заголовки
            headers = ["Название", "Цена", "URL изображения", "Описание"]
            for col, header in enumerate(headers):
                page.write(0, col, header)
            
            # Данные
            for row, item in enumerate(self.parsed_data, 1):
                if len(item) != 4:
                    continue
                for col, value in enumerate(item):
                    page.write(row, col, value)
            
            # Настройка ширины столбцов
            page.set_column("A:A", 20)
            page.set_column("B:B", 15)
            page.set_column("C:C", 40)
            page.set_column("D:D", 50)
            
            book.close()
            
            self.status_label.setText(f"Файл сохранен: {file_path}")
            QMessageBox.information(self, "Успех", "Данные успешно сохранены в Excel файл")
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")
            self.status_label.setText("Ошибка при сохранении файла")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParserApp()
    window.show()
    sys.exit(app.exec_())