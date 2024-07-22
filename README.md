# Automatic subtitles in your videos

## Goal

The goal is to generate subtitles and make videos more alive. This way, they can be posted on social medias.

> This is the older version of [this project](https://github.com/newtondotcom/yogocap-back).

## Techstack

This project is based on [WhisperX](https://github.com/m-bain/whisperX) to get speech to text translations, with word level timestamp. It then uses ```.ass``` subtitles format and ```ffmpeg``` to encode subtitles onto videos. After, it removes silent segways of the video.

> This repo is not ready for Python version 12 for now, due to its depencies.
