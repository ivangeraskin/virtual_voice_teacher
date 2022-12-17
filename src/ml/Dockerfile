FROM python:3.9
#RUN apt-get install ffmpeg libavcodec-extra

COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt


CMD ["python", "app.py"]