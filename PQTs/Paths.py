# -*- coding: utf-8 -*-

import os

dirnamePath = os.path.dirname(__file__)

pathDescargas = os.path.join(dirnamePath,'..','Almacenamiento','Descargas')
pathAudioMp3 = f"{pathDescargas}/audioCaptcha.mp3"
pathAudioWav = f"{pathDescargas}/audioCaptcha.wav"

pathImg = os.path.join(dirnamePath,'..','Almacenamiento','img')