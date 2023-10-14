import json
import zlib
from time import sleep

import sysv_ipc

if __name__ == '__main__':
    queue_key = zlib.crc32('queue_name'.encode('utf-8'))
    messages_queue = sysv_ipc.MessageQueue(key=queue_key)
    while True:
        message, msg_type = messages_queue.receive()
        data = json.loads(message)
        print(f'subscriber message receive: {data}')
        sleep(1)
