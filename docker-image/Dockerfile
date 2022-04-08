FROM python:3.10

WORKDIR /usr/src/ltt-video-notify

COPY code/* ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]