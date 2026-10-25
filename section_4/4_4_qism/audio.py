from transformers import pipeline
from transformers.pipelines.audio_utils import ffmpeg_microphone_live
import soundfile as sf
import pygame
from kokoro import KPipeline
from utils import logger
import torch
import sys
import numpy as np

device =  "cuda:0" if torch.cuda.is_available() else "cpu"

wake_classifier = pipeline("audio-classification",
                           model="MIT/ast-finetuned-speech-commands-v2",
                           device=device)
print(wake_classifier.model.config.id2label)

transcriber = pipeline("automatic-speech-recognition",
                       model="openai/whisper-base.en",
                       device=device)

tts_pipeline = KPipeline(lang_code="a")

def detect_wake_work(wake_word="marvin",prob_threshold=0.3):
    logger.info("Listening for a wake work...")
    mic = ffmpeg_microphone_live(
        sampling_rate=wake_classifier.feature_extractor.sampling_rate,
        chunk_length_s=2.0,
        stream_chunk_s=0.25,
    )

    try:
        for prediction in wake_classifier(mic):
            pred = prediction[0]
            if pred['label'] == wake_word and pred['score'] > prob_threshold:
                logger.info("Wake word '{wake_word}' detected!")
                return True
    finally:
        mic.close()
        del mic

def transcribe():
    logger.info("Start speaking...")
    mic = ffmpeg_microphone_live(
        sampling_rate=transcriber.feature_extractor.sampling_rate,
        chunk_length_s=5.0,
        stream_chunk_s=1.0,
    )
    try:
        for item in transcriber(mic,generate_kwargs={"max_new_token":128}):
            sys.stdout.write("\033[K")
            print(item["text"],end="\r")
            if not item["partial"][0]:
                return item['text']
    finally:
        mic.close()
        del mic

def speak(text:str):
    logger.info("Generating speach...")
    generator = tts_pipeline(text,voice="am_micheal",speed=1.0)
    all_audio = []

    for _, _, audio in generator:
        audio_np = audio.numpy() if hasattr(audio,"numpy") else audio
        all_audio.append(audio_np)

    if len(all_audio) > 0:
        full_audio = np.concatenate(all_audio)
        filename = "output.wav"
        sf.write(filename,full_audio,24000)
        pygame.mixer.init(frequency=24000)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)