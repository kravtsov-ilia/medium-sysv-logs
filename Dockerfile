FROM python:3.10-alpine
RUN apk add build-base
RUN pip install sysv_ipc msgpack ujson simplejson redis

WORKDIR /code
COPY log_handlers/ ./log_handlers/
COPY test_sync.py .

CMD ["python", "test_handlers.py"]
