# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, unquote_plus

# Для начала определим настройки запуска
hostName = "localhost" # Адрес для доступа по сети
serverPort = 8080 # Порт для доступа по сети

class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """
    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        with open("contacts.html", "r", encoding="utf-8") as file:
            content = file.read()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def do_POST(self):
        """Метод для обработки входящих POST-запросов"""
        content_length = int(self.headers["Content-Length"])  # Получаем длину данных
        body = self.rfile.read(content_length)  # Читаем данные из потока
        body_str = body.decode("utf-8")
        params = parse_qs(body_str) # Парсим параметры из URL-кодированной строки
        answer_post = f"Имя: {params.get("name", ["no data"])[0]}\nEmail: {params.get("email", ["no data"])[0]}\nСообщение: {params.get("message", ["no data"])[0]}"
        print("Полученные данные от пользователя:")
        print(answer_post)
        self.send_response(303)  # HTTP 303 See Other
        self.send_header("Location", "/")  # Перенаправление на главную страницу
        self.end_headers()


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу,
    # который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через
        # сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес
    # и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")