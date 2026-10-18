from transformers import pipeline
from transformers.pipelines.audio_utils import ffmpeg_microphone_live
import soundfile as sf
import pygame
from kokoro import KPipeline
from utils import logger
import psutil
import torch
import sys
import numpy as np

device =  "cuda:0" if torch.cuda.is_available() else "cpu"