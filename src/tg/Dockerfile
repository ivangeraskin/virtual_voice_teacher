FROM python:3.9
RUN apt update && \
    apt install -y ffmpeg

COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python", "app.py"]