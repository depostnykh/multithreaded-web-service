FROM python:3.9

ARG PROJECT_DIR=/home/multithreaded-web-service

WORKDIR ${PROJECT_DIR}

ENV TZ=Europe/Moscow
ENV HOST=localhost
ENV PORT=8000
ENV THREADS_COUNT=2

COPY core ${PROJECT_DIR}/core
COPY data ${PROJECT_DIR}/data
COPY libs ${PROJECT_DIR}/libs

RUN mkdir ${PROJECT_DIR}/logs
COPY main.py ${PROJECT_DIR}/

CMD [ "python3", "main.py"]
