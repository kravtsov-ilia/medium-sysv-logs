import hashlib
import logging
import os
import queue
import random
import sys
import time
from contextlib import contextmanager
from logging.handlers import QueueHandler, QueueListener

from log_handlers.sysv_log_handler import SysvIPCHandler

USED_LOGGER = os.getenv('USED_LOGGER')

logger = logging.getLogger(__name__)
que = queue.Queue(-1)  # no limit on size

handlers = {
    'stdout': logging.StreamHandler(stream=sys.stdout),
    'file': logging.FileHandler('file_handler.log'),
    'sysv': SysvIPCHandler(queue_name='example', max_message_size=500*1024),
    'queue': QueueHandler(que),
}

handler = logging.FileHandler('queue_file_handler.log')
listener = QueueListener(que, handler)


@contextmanager
def log_context():
    if USED_LOGGER == 'queue':
        listener.start()
        yield
        listener.stop()
    else:
        yield


def get_handler():
    return handlers[USED_LOGGER]


def main():
    current_handler = get_handler()
    current_handler.setLevel(logging.INFO)
    logger.handlers = [current_handler]
    logger.setLevel(logging.INFO)
    logger.propagate = False

    results = {}
    for iterations_count in (10**4, 10**5, 10**6):
        results[iterations_count] = []
        start_time = time.time()
        for _ in range(iterations_count):
            hashes = []
            for _ in range(10):
                val = random.randint(0, 100)
                hashes.append(hashlib.sha256(f'{val}'.encode('utf-8')).hexdigest()[:10])

            logger.info(f'log record - {"-".join(hashes)}')
        spent_time = time.time() - start_time
        results[iterations_count].append((f'{current_handler}', f'{spent_time:.6f}'))
    print(results)


if __name__ == '__main__':
    with log_context():
        main()
