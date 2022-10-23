import json
import time
import random
import socket
import threading
from datetime import datetime

from data import config
from libs.logger import get_logger

logger = get_logger(logger_name=__name__)


class ThreadedServer:
    """Класс многопоточного сервера"""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket = self.get_server_socket()
        self.elapsed_time = 0
        self.queries_count = 0
        self.endpoints = {
            '/v1/api': self.get_some_logic,
            '/health': self.get_health
        }

    def get_server_socket(self) -> socket:
        """Возвращает сконфигурированный серверный сокет с привязкой к адресу."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))

        return server_socket

    def listen(self) -> None:
        """Переводим серверный сокет в режим прослушивания на предмет входящих подключений"""
        logger.debug(f'Server started on {self.host}:{self.port}.')
        self.server_socket.listen()

        while True:
            client_socket, address = self.server_socket.accept()

            if threading.active_count() > config.THREADS_COUNT:
                logger.debug(f'Connection from {address} denied.')
                response = self.get_503_response()
                client_socket.sendall(response)
                client_socket.close()
            else:
                client_socket.settimeout(config.TIMEOUT)
                logger.debug(f'Connection from {address} successful.')
                threading.Thread(target=self.serve_client, args=(client_socket, address)).start()

    def serve_client(self, client_socket: socket, address: tuple) -> None:
        """Обрабатывает запрос клиента и возвращает ответ."""
        while True:
            try:
                request = client_socket.recv(config.BUFFER_SIZE)
                response = self.get_response(client_request=request.decode(config.CODING_FORMAT))
                client_socket.sendall(response)
                logger.debug(f'Send response to {address}.')
            except Exception as err:
                logger.error(f'Error msg: {err}')
                client_socket.close()
                break

    @staticmethod
    def get_request_headers(client_request: str, ) -> tuple:
        """Парсит запрос и возвращает кортеж с заголовками."""
        split_request = client_request.split(' ')

        method = split_request[0]
        endpoint = split_request[1]

        return method, endpoint

    def get_headers(self, method: str, endpoint: str) -> tuple:
        """Возращает кортеж с заголовками в зависимости от получаемых на вход параметров."""
        if method != 'GET':
            return 'HTTP/1.1 405 Method not allowed\n\n', 405

        if endpoint not in self.endpoints:
            return 'HTTP/1.1 404 Not found\n\n', 404

        return 'HTTP/1.1 200 OK\n\n', 200

    def get_content(self, status_code: int, endpoint: str) -> json:
        """Вовзращает тело ответа в зависимости от получаемых на вход параметров."""
        if status_code == 404:
            return json.dumps({'msg': 'Page not found', 'status_code': 404})
        elif status_code == 405:
            return json.dumps({'msg': 'Method not allowed', 'status_code': 405})

        return self.endpoints[endpoint]()

    def get_response(self, client_request: str) -> bytes:
        """Формирует и возвращает ответ на клиенский запрос."""
        request_method, request_endpoint = self.get_request_headers(client_request=client_request)
        headers, status_code = self.get_headers(method=request_method, endpoint=request_endpoint)
        content = self.get_content(status_code=status_code, endpoint=request_endpoint)

        return (headers + content).encode()

    @staticmethod
    def get_503_response() -> bytes:
        """Возвращает ответ для запросов, которые в данный момент не может обработать сервер"""
        headers = 'HTTP/1.1 503 Service temporarily unavailable\n\n'
        content = json.dumps({'msg': 'Service temporarily unavailable', 'status_code': 503})

        return (headers + content).encode()

    def get_some_logic(self) -> json:
        """Имитирует вычисления на сервере и возвращает текущие дату и время
        в формате ISO 8601 + длительность вычислений"""
        today = datetime.now()
        seconds_slept = random.randint(1, 5)

        time.sleep(seconds_slept)

        self.queries_count += 1
        self.elapsed_time += seconds_slept

        return json.dumps({'current_date': today.isoformat(), 'response_took_seconds': seconds_slept})

    def get_health(self) -> json:
        """Возвращает общие продолжительность и колличество запросов к серверу."""
        return json.dumps({'total': {'queries': self.queries_count, 'seconds': self.elapsed_time}})
