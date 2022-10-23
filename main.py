from data import config
from libs.logger import get_logger
from core.server import ThreadedServer

logger = get_logger(logger_name=__name__)


def run_server() -> None:
    """Запускает многопоточный сервер."""
    logger.info('App is running.')
    server = ThreadedServer(host=config.HOST, port=config.PORT)
    server.listen()
    logger.info('App has completed.')


if __name__ == '__main__':
    run_server()
