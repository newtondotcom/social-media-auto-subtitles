FROM python:3.9.18-slim-bullseye

WORKDIR /app

RUN apt update
RUN apt install git -y
RUN apt install ffmpeg -y
RUN pip install moviepy
RUN pip install ffmpeg-python
RUN pip install opencv-python
RUN pip install git+https://github.com/m-bain/whisperx.git

RUN useradd -ms /bin/bash whisperx
USER whisperx
COPY --chown=whisperx:whisperx . /app

# RUN mkdir temp
# RUN mkdir output

CMD ["python", "main.py"]

