import json
import zlib
from time import sleep

import sysv_ipc

if __name__ == '__main__':
    queue_key = zlib.crc32('queue_name'.encode('utf-8'))
    messages_queue = sysv_ipc.MessageQueue(
        key=queue_key,
        flags=sysv_ipc.IPC_CREAT,
        mode=int('0666', 8),
        max_message_size=500*1024,
    )
    i = 0
    while True:
        i += 1
        data = {
            'number': i
        }
        # it is possible to use more effective data format than json, for example - msg pack
        messages_queue.send(json.dumps(data))
        print(f'publish: {i}')
        sleep(1)
