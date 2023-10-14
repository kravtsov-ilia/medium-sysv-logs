import logging
import zlib

import sysv_ipc


class SysvIPCHandler(logging.Handler):
    def __init__(
        self,
        *,
        queue_name: str,
        max_message_size: int,
        mode: str = '0666',
        level: int = logging.INFO
    ):
        super().__init__(level)
        queue_key = zlib.crc32(queue_name.encode('utf-8'))
        self.messages_queue = sysv_ipc.MessageQueue(
            key=queue_key,
            flags=sysv_ipc.IPC_CREAT,
            mode=int(mode, 8),
            max_message_size=max_message_size,
        )

    def emit(self, record: logging.LogRecord) -> None:
        self.acquire()
        try:
            self.messages_queue.send(record.msg.encode('utf-8'))
        finally:
            self.release()
